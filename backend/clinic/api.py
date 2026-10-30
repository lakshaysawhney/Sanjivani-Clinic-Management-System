import hashlib
import json
import secrets
import uuid
from datetime import date, timedelta
from django.conf import settings
from django.db import transaction
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from accounts.models import User, Provider
from accounts.views import user_data
from accounts.services import issue_token
from .models import (
    Patient,
    FrequencyPlan,
    Therapy,
    Session,
    DailySchedule,
    Notification,
    AuditLog,
    EmailOutbox,
    IdempotencyRecord,
    Participation,
)
from .time_rules import STARTS, now, month_floor, history_scope
from .scheduling import reconcile, save_session, publish, publication_reminder, therapist_visible
from .billing import balance, post_entry, reverse_payment
from .api_errors import Conflict


def staff_only(user):
    if user.role not in ["ADMIN", "RECEPTIONIST"]:
        raise PermissionDenied("This page is available to clinic administration.")


def admin_only(user):
    if user.role != "ADMIN":
        raise PermissionDenied("Administrator access is required.")


def parse_day(value):
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        raise ValidationError("Enter a valid date.")


def selected_month(request):
    day = parse_day(request.query_params.get("month", str(now().date())[:7]) + "-01")
    history_scope(request.user, day)
    return day, month_floor(day, -1)


def patient_data(patient, on=None):
    plan = (
        patient.plans.filter(effective_date__lte=on or now().date())
        .order_by("-effective_date", "-created_at")
        .first()
    )
    return {
        "id": patient.pk,
        "name": patient.name,
        "active": patient.active,
        "special_fee": patient.special_fee,
        "weekly": plan.weekly if plan else 0,
        "monthly": plan.monthly if plan else 0,
        "balance_paise": balance(patient),
    }


def session_data(session, user):
    parts = []
    for part in session.participations.filter(removed=False).select_related("patient"):
        item = {
            "id": part.pk,
            "patient_id": part.patient_id,
            "name": part.patient.name,
            "status": part.status,
        }
        if user.role != "THERAPIST":
            item["special_fee"] = part.patient.special_fee
        parts.append(item)
    return {
        "id": str(session.pk),
        "date": str(session.schedule.date),
        "slot": session.slot,
        "therapy": session.therapy_id,
        "therapy_name": session.therapy.name,
        "version": session.version,
        "providers": list(session.assignments.values_list("provider_id", flat=True)),
        "participants": parts,
        "ends_at": session.ends_at.isoformat(),
    }


def participation_history(part, user):
    """Cancellation reporting uses frozen context, never the edited session shell."""
    data = session_data(part.session, user)
    if part.status == "Cancelled" and part.cancelled_context:
        data.update(part.cancelled_context)
    data["participants"] = [
        {"id": part.pk, "patient_id": part.patient_id, "name": part.patient.name, "status": part.status}
    ]
    data["patient_status"] = part.status
    return data


def ledger_data(entry):
    return {
        "id": str(entry.pk),
        "kind": entry.kind,
        "amount_paise": entry.amount_paise,
        "description": entry.description,
        "effective_at": entry.effective_at.isoformat(),
        "created_at": entry.created_at.isoformat(),
        "actor": entry.actor.full_name if entry.actor else "System",
        "reverses": str(entry.reverses_id) if entry.reverses_id else None,
        "reversed": hasattr(entry, "reversal"),
    }


@transaction.atomic
def idempotent(request, fn):
    try:
        key = uuid.UUID(request.headers.get("Idempotency-Key", ""))
    except ValueError:
        raise ValidationError("A valid Idempotency-Key is required for changes.")
    digest = hashlib.sha256((request.path + json.dumps(request.data, sort_keys=True)).encode()).hexdigest()
    # Serialize same-user writes, so duplicate requests cannot both execute.
    User.objects.select_for_update().get(pk=request.user.pk)
    record, _ = IdempotencyRecord.objects.get_or_create(
        actor=request.user, key=key, defaults={"digest": digest}
    )
    if record.digest != digest:
        raise Conflict("This request identifier was already used with different content.")
    if record.response is not None:
        return Response(record.response)
    result = fn(str(key))
    record.response = result
    record.save()
    return Response(result)


class ClinicView(APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.pending_activation:
            raise PermissionDenied("Complete account activation first.")
        for _ in range(10):
            if reconcile() < 200:
                break
        else:
            from rest_framework.exceptions import APIException

            raise APIException("Catching up on clinic records. Please retry shortly.")
        publication_reminder()


class CatalogView(ClinicView):
    def get(self, request):
        providers = Provider.objects.select_related("user").all()
        if request.user.role == "THERAPIST":
            providers = providers.filter(user=request.user)
        return Response(
            {
                "therapies": list(
                    Therapy.objects.values(
                        *(
                            ["code", "name", "group"]
                            if request.user.role == "THERAPIST"
                            else ["code", "name", "fee_paise", "group"]
                        )
                    )
                ),
                "slots": STARTS,
                "providers": [
                    {
                        "id": p.pk,
                        "name": p.display_name,
                        "full_name": p.user.full_name,
                        "active": p.user.is_active,
                        "order": p.display_order,
                    }
                    for p in providers
                ],
                "today": str(now().date()),
                "operating_days": settings.OPERATING_DAYS,
            }
        )


class ScheduleView(ClinicView):
    def get(self, request):
        day = parse_day(request.query_params.get("date", str(now().date())))
        schedule = DailySchedule.objects.filter(date=day).first()
        sessions = Session.objects.filter(schedule=schedule).select_related("schedule", "therapy")
        if request.user.role == "THERAPIST":
            if not schedule or not therapist_visible(day, schedule.published_at):
                raise PermissionDenied("This published schedule is not currently visible.")
            sessions = sessions.filter(assignments__provider__user=request.user)
        else:
            history_scope(request.user, day)
        data = {
            "date": str(day),
            "published": bool(schedule and schedule.published_at),
            "sessions": [session_data(s, request.user) for s in sessions],
        }
        if request.user.role != "THERAPIST":
            data["cancelled_history"] = [
                participation_history(p, request.user)
                for p in Participation.objects.filter(status="Cancelled", attendance_date=day)
                .select_related("session__schedule", "session__therapy", "patient")
                .order_by("pk")
            ]
        return Response(data)


class MySchedulesView(ClinicView):
    def get(self, request):
        days = DailySchedule.objects.filter(
            date__gte=now().date() - timedelta(days=1), published_at__isnull=False
        )
        return Response(
            [
                {
                    "date": str(d.date),
                    "sessions": [
                        session_data(s, request.user)
                        for s in d.sessions.filter(assignments__provider__user=request.user)
                    ],
                }
                for d in days
                if therapist_visible(d.date, d.published_at)
            ]
        )


class SessionView(ClinicView):
    def get(self, request, session_id):
        session = get_object_or_404(Session, pk=session_id)
        if request.user.role == "THERAPIST":
            if not session.assignments.filter(provider__user=request.user).exists() or not therapist_visible(
                session.schedule.date, session.schedule.published_at
            ):
                raise PermissionDenied()
        else:
            history_scope(request.user, session.schedule.date)
        return Response(session_data(session, request.user))

    def post(self, request, session_id=None):
        staff_only(request.user)
        return idempotent(
            request,
            lambda _: session_data(save_session(request.user, request.data, session_id), request.user),
        )


class PublishView(ClinicView):
    def post(self, request):
        staff_only(request.user)
        day = parse_day(request.data.get("date"))
        return idempotent(
            request, lambda _: {"date": str(publish(request.user, day).date), "published": True}
        )


def save_patient(request, patient=None):
    from rest_framework import serializers

    class Input(serializers.Serializer):
        name = serializers.CharField(max_length=160)
        active = serializers.BooleanField(default=True)
        special_fee = serializers.BooleanField(default=False)
        weekly = serializers.IntegerField(min_value=0, max_value=70, default=0)
        monthly = serializers.IntegerField(min_value=0, max_value=310, default=0)
        effective_date = serializers.DateField(required=False)

    form = Input(data=request.data)
    form.is_valid(raise_exception=True)
    data = form.validated_data
    before = patient_data(patient) if patient else {}
    if patient:
        patient = Patient.objects.select_for_update().get(pk=patient.pk)
    else:
        patient = Patient()
    patient.name = data["name"]
    patient.active = data["active"]
    patient.special_fee = data["special_fee"]
    patient.save()
    effective = data.get("effective_date", now().date())
    history_scope(request.user, effective)
    plan = (
        patient.plans.filter(effective_date__lte=effective).order_by("-effective_date", "-created_at").first()
    )
    if not plan or (plan.weekly, plan.monthly) != (data["weekly"], data["monthly"]):
        FrequencyPlan.objects.create(
            patient=patient,
            weekly=data["weekly"],
            monthly=data["monthly"],
            effective_date=effective,
            actor=request.user,
        )
    after = patient_data(patient)
    AuditLog.objects.create(
        actor=request.user, action="patient.save", reference=str(patient.pk), before=before, after=after
    )
    return after


class PatientsView(ClinicView):
    def get(self, request):
        staff_only(request.user)
        patients = Patient.objects.filter(name__icontains=request.query_params.get("q", "")).order_by(
            "name", "pk"
        )
        page = max(1, min(10000, int(request.query_params.get("page", 1))))
        return Response(
            {
                "count": patients.count(),
                "results": [patient_data(p) for p in patients[(page - 1) * 50 : page * 50]],
            }
        )

    def post(self, request):
        staff_only(request.user)
        return idempotent(request, lambda _: save_patient(request))


class PatientView(ClinicView):
    def get(self, request, patient_id):
        staff_only(request.user)
        patient = get_object_or_404(Patient, pk=patient_id)
        start, end = selected_month(request)
        parts = patient.participations.filter(
            attendance_date__gte=start, attendance_date__lt=end
        ).select_related("session__therapy", "session__schedule")
        done = parts.filter(status="Completed")
        categories = {t.code: 0 for t in Therapy.objects.all()}
        providers = {}
        for part in done:
            categories[part.session.therapy_id] += 1
            for assignment in part.session.assignments.select_related("provider"):
                name = assignment.provider.display_name
                providers[name] = providers.get(name, 0) + 1
        sums = patient.ledger.values("kind").annotate(total=Sum("amount_paise"))
        totals = {x["kind"]: x["total"] for x in sums}
        return Response(
            {
                **patient_data(patient, end - timedelta(days=1)),
                "completed": done.count(),
                "cancelled": parts.filter(status="Cancelled").count(),
                "categories": categories,
                "providers": providers,
                "total_payments_paise": totals.get("payment", 0),
                "total_charges_paise": -totals.get("charge", 0),
                "plans": list(
                    patient.plans.order_by("-effective_date").values("weekly", "monthly", "effective_date")
                ),
                # Cancellation slots come from frozen context, so ordering by
                # the mutable session slot would put moved records out of order.
                "history": sorted(
                    (participation_history(p, request.user) for p in parts.order_by("pk")),
                    key=lambda item: (item["date"], item["slot"]),
                ),
            }
        )

    def post(self, request, patient_id):
        staff_only(request.user)
        patient = get_object_or_404(Patient, pk=patient_id)
        return idempotent(request, lambda _: save_patient(request, patient))


class LedgerView(ClinicView):
    def get(self, request, patient_id):
        staff_only(request.user)
        patient = get_object_or_404(Patient, pk=patient_id)
        running = 0
        entries = []
        for entry in patient.ledger.select_related("actor"):
            running += entry.amount_paise
            entries.append({**ledger_data(entry), "running_balance_paise": running})
        return Response({"balance_paise": running, "entries": entries})

    def post(self, request, patient_id):
        staff_only(request.user)
        return idempotent(
            request,
            lambda key: ledger_data(post_entry(patient_id, request.user, request.data, "manual:" + key)),
        )


class ReverseView(ClinicView):
    def post(self, request, entry_id):
        staff_only(request.user)
        return idempotent(
            request,
            lambda key: ledger_data(
                reverse_payment(entry_id, request.user, str(request.data.get("reason", "")), "reverse:" + key)
            ),
        )


class FinanceView(ClinicView):
    def get(self, request):
        staff_only(request.user)
        patients = [
            patient_data(p)
            for p in Patient.objects.filter(name__icontains=request.query_params.get("q", "")).order_by(
                "name"
            )
        ]
        return Response([p for p in patients if p["balance_paise"] < 0 or p["special_fee"]])


class FrequencyView(ClinicView):
    def get(self, request):
        staff_only(request.user)
        start, end = selected_month(request)
        selected = parse_day(request.query_params.get("week", str(now().date())))
        week = selected - timedelta(days=selected.weekday())
        history_scope(request.user, week)
        rows = []
        for patient in Patient.objects.filter(name__icontains=request.query_params.get("q", "")).order_by(
            "name"
        ):
            parts = patient.participations
            monthly = parts.filter(attendance_date__gte=start, attendance_date__lt=end)
            rows.append(
                {
                    **patient_data(patient, end - timedelta(days=1)),
                    "actual_weekly": parts.filter(
                        status="Completed",
                        session__schedule__date__gte=week,
                        session__schedule__date__lt=week + timedelta(days=7),
                    ).count(),
                    "actual_monthly": monthly.filter(status="Completed").count(),
                    "cancelled": monthly.filter(status="Cancelled").count(),
                }
            )
        return Response(rows)


class HistoryView(ClinicView):
    def get(self, request):
        start, end = selected_month(request)
        sessions = Session.objects.filter(
            schedule__date__gte=start, schedule__date__lt=end, participations__status="Completed"
        ).distinct()
        if request.user.role == "THERAPIST":
            sessions = sessions.filter(assignments__provider__user=request.user)
        else:
            provider = request.query_params.get("provider")
            if provider:
                sessions = sessions.filter(assignments__provider_id=provider)
        return Response(
            {
                "total": sessions.count(),
                "sessions": [
                    session_data(s, request.user) for s in sessions.order_by("schedule__date", "slot")
                ],
            }
        )


class NotificationsView(ClinicView):
    def get(self, request):
        staff_only(request.user)
        items = list(
            Notification.objects.filter(resolved=False).values(
                "id", "kind", "patient_id", "date", "created_at"
            )
        )
        return Response(
            {
                "items": items,
                "delivery": list(
                    EmailOutbox.objects.exclude(state__in=["sent", "cancelled"])
                    .values("state")
                    .annotate(count=Count("id"))
                ),
                "inactive_bookings": Session.objects.filter(
                    ends_at__gt=timezone.now(), assignments__provider__user__is_active=False
                )
                .distinct()
                .count(),
            }
        )


def staff_data(user):
    provider = getattr(user, "provider", None)
    return {
        **user_data(user),
        "email": user.email,
        "active": user.is_active,
        "pending_activation": user.pending_activation,
        "specialization": provider.specialization if provider else "",
        "display_name": provider.display_name if provider else "",
        "display_order": provider.display_order if provider else 100,
    }


class StaffView(ClinicView):
    def get(self, request):
        admin_only(request.user)
        return Response([staff_data(u) for u in User.objects.order_by("id")])

    def post(self, request, user_id=None):
        admin_only(request.user)

        def save(_):
            from rest_framework import serializers

            class Input(serializers.Serializer):
                username = serializers.CharField(max_length=150)
                full_name = serializers.CharField(max_length=120)
                email = serializers.EmailField()
                active = serializers.BooleanField(default=True)
                display_name = serializers.CharField(max_length=60)
                specialization = serializers.CharField(max_length=60, allow_blank=True)
                display_order = serializers.IntegerField(min_value=0, max_value=1000)

            form = Input(data=request.data)
            form.is_valid(raise_exception=True)
            data = form.validated_data
            user = (
                get_object_or_404(User.objects.select_for_update(), pk=user_id)
                if user_id
                else User(role="THERAPIST", pending_activation=True)
            )
            before = staff_data(user) if user_id else {}
            if (
                not data["active"]
                and user.role == "ADMIN"
                and not User.objects.filter(role="ADMIN", is_active=True).exclude(pk=user.pk).exists()
            ):
                raise ValidationError("The last active administrator cannot be deactivated.")
            user.username = data["username"]
            user.full_name = data["full_name"]
            user.email = data["email"].lower()
            user.is_active = data["active"]
            if not user_id:
                user.set_unusable_password()
            user.save()
            if user.role != "RECEPTIONIST":
                Provider.objects.update_or_create(
                    user=user,
                    defaults={k: data[k] for k in ["display_name", "specialization", "display_order"]},
                )
            AuditLog.objects.create(
                actor=request.user,
                action="staff.save",
                reference=str(user.pk),
                before=before,
                after=staff_data(user),
            )
            return staff_data(user)

        return idempotent(request, save)


class StaffResetView(ClinicView):
    def post(self, request, user_id):
        admin_only(request.user)

        def reset(_):
            issue_token(get_object_or_404(User, pk=user_id), request.user, revoke=True)
            return {"ok": True}

        return idempotent(request, reset)


class AuditView(ClinicView):
    def get(self, request):
        admin_only(request.user)
        return Response(list(AuditLog.objects.order_by("-created_at").values()[:200]))


class SyncView(ClinicView):
    def post(self, request):
        from .email_service import process_outbox

        return Response({"ok": True, "sent": process_outbox(2)})


class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({"status": "ok"})


class MaintenanceView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        if not settings.MAINTENANCE_SECRET or not secrets.compare_digest(
            request.headers.get("Authorization", ""), "Bearer " + settings.MAINTENANCE_SECRET
        ):
            raise PermissionDenied()
        from .email_service import process_outbox

        completed = reconcile()
        publication_reminder()
        return Response({"completed": completed, "sent": process_outbox(10)})

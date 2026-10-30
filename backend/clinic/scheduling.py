from datetime import date, datetime, time, timedelta
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from accounts.models import Provider
from .models import (
    Patient,
    DailySchedule,
    Session,
    Assignment,
    Participation,
    ProviderReservation,
    PatientReservation,
    AuditLog,
    EmailOutbox,
    Notification,
)
from .time_rules import now, slot_end, editable, next_operating_day, IST
from .billing import reconcile_charge
from .api_errors import Conflict


def snapshot(session):
    return {
        "date": str(session.schedule.date),
        "slot": session.slot,
        "therapy": session.therapy_id,
        "providers": sorted(session.assignments.values_list("provider_id", flat=True)),
        "participants": list(
            session.participations.order_by("patient_id").values("patient_id", "status", "removed")
        ),
    }


def sync_reservations(session):
    """Reserve each active resource once, including providers shared by a group.

    Database uniqueness is essential: two transactions can both observe a free
    slot before either commits. A conflicting insert rolls back the whole save,
    while cancelled participation remains in history without reserving the child.
    """
    ProviderReservation.objects.filter(session=session).delete()
    PatientReservation.objects.filter(session=session).delete()
    active = session.participations.exclude(status="Cancelled")
    if active.exists():
        ProviderReservation.objects.bulk_create(
            [
                ProviderReservation(
                    session=session, provider_id=p, date=session.schedule.date, slot=session.slot
                )
                for p in session.assignments.values_list("provider_id", flat=True)
            ]
        )
        PatientReservation.objects.bulk_create(
            [
                PatientReservation(
                    session=session, patient_id=p, date=session.schedule.date, slot=session.slot
                )
                for p in active.values_list("patient_id", flat=True)
            ]
        )


def changed_emails(session, before, previous_published=False):
    if not session.schedule.published_at and not previous_published:
        return
    after = snapshot(session)
    if before == after:
        return
    ids = set(before.get("providers", [])) | set(after["providers"])
    for provider in Provider.objects.filter(pk__in=ids, user__is_active=True, user__role="THERAPIST"):
        EmailOutbox.objects.get_or_create(
            event_key=f"session:{session.pk}:{session.version}:{provider.pk}",
            defaults={"recipient": provider.user, "next_attempt": timezone.now() + timedelta(seconds=30)},
        )


@transaction.atomic
def save_session(actor, data, session_id=None):
    before = {}
    original_context = None
    old_published = False
    if session_id:
        session = Session.objects.select_for_update().select_related("schedule", "therapy").get(pk=session_id)
        editable(actor, session.schedule.date)
        if data.get("version") != session.version:
            raise Conflict("This appointment changed. Refresh before saving.")
        before = snapshot(session)
        original_context = {key: before[key] for key in ("date", "slot", "therapy", "providers")}
        original_context.update(therapy_name=session.therapy.name, ends_at=session.ends_at.isoformat())
        old_published = bool(session.schedule.published_at)
    else:
        session = Session(created_by=actor)
    try:
        day = date.fromisoformat(data["date"])
        slot = data["slot"]
        provider_ids = sorted(set(data["providers"]))
        participant_data = data["participants"]
        patient_ids = sorted({p["patient_id"] for p in participant_data})
    except (KeyError, ValueError, TypeError):
        raise ValidationError("Date, slot, providers and patients are required.")
    editable(actor, day)
    if day.weekday() not in settings.OPERATING_DAYS:
        raise ValidationError("The clinic is closed on this day.")
    if type(slot) is not int:
        raise ValidationError("Choose a valid time slot.")
    from .models import Therapy

    therapy = Therapy.objects.filter(pk=data.get("therapy")).first()
    if not therapy or not provider_ids or not patient_ids or len(patient_ids) != len(participant_data):
        raise ValidationError("Choose valid therapy, distinct patients and providers.")
    if not therapy.group and (len(provider_ids) != 1 or len(patient_ids) != 1):
        raise ValidationError("Ordinary sessions require exactly one child and one provider.")
    providers = list(Provider.objects.filter(pk__in=provider_ids, user__is_active=True).order_by("id"))
    if len(providers) != len(provider_ids):
        raise ValidationError("An assigned provider is inactive or unavailable.")
    old_patient_ids = list(session.participations.values_list("patient_id", flat=True)) if session_id else []
    # Global patient lock order also serializes payments against corrections.
    locked = list(
        Patient.objects.select_for_update().filter(pk__in=set(patient_ids + old_patient_ids)).order_by("pk")
    )
    if any(not p.active for p in locked if p.pk in patient_ids) or not set(patient_ids).issubset(
        {p.pk for p in locked}
    ):
        raise ValidationError("Choose active patients.")
    session.schedule, _ = DailySchedule.objects.get_or_create(date=day)
    session.schedule = DailySchedule.objects.select_for_update().get(pk=session.schedule.pk)
    session.slot = slot
    session.ends_at = slot_end(day, slot)
    session.therapy = therapy
    if session_id:
        session.version += 1
    session.save()
    Assignment.objects.filter(session=session).exclude(provider_id__in=provider_ids).delete()
    for provider in providers:
        Assignment.objects.get_or_create(session=session, provider=provider)
    # Capture cancellation against the old shell before its date/category/providers
    # change. Later saves cannot move a retired child's cancellation to a new month.
    for part in session.participations.exclude(patient_id__in=patient_ids):
        retain_context(part, session, "Cancelled", original_context, actor)
        part.removed = True
        part.status = "Cancelled"
        reconcile_charge(part, actor)
    for item in participant_data:
        status = item.get("status", "Scheduled")
        if status not in Participation.Status.values:
            raise ValidationError("Choose Scheduled, Completed or Cancelled.")
        if status == "Completed" and session.ends_at > timezone.now():
            raise ValidationError("A future session cannot be completed early.")
        if status == "Scheduled" and session.ends_at <= timezone.now():
            status = "Completed"
        part, created = Participation.objects.get_or_create(
            session=session, patient_id=item["patient_id"], defaults={"attendance_date": day}
        )
        part.session = session
        retain_context(part, session, status, None if created else original_context, actor)
        part.removed = False
        part.status = status
        reconcile_charge(part, actor)
    sync_reservations(session)
    after = snapshot(session)
    if before == after:
        session.version -= 1
        session.save(update_fields=["version"])
    else:
        AuditLog.objects.create(
            actor=actor,
            action="session.update" if session_id else "session.create",
            reference=str(session.pk),
            before=before,
            after=after,
            reason=data.get("reason", "")[:500],
        )
        changed_emails(session, before, old_published)
    return session


def retain_context(part, session, status, original_context, actor):
    """Keep one current attendance outcome; restoration supersedes cancellation.

    A removed child retains the appointment context at cancellation. Explicitly
    restoring that child reuses its participation and fee snapshot, and moves its
    attendance to the corrected appointment rather than counting both outcomes.
    """
    if status == "Cancelled":
        if part.cancelled_context is None:
            part.cancelled_context = original_context or {
                "date": str(session.schedule.date),
                "slot": session.slot,
                "therapy": session.therapy_id,
                "therapy_name": session.therapy.name,
                "providers": list(session.assignments.values_list("provider_id", flat=True)),
                "ends_at": session.ends_at.isoformat(),
            }
        part.attendance_date = date.fromisoformat(part.cancelled_context["date"])
    else:
        if part.cancelled_context:
            # Moving the shell into the future cannot reopen yesterday's closed
            # cancellation to reception. Admin can correct either attendance date.
            editable(actor, part.attendance_date)
        part.cancelled_context = None
        part.attendance_date = session.schedule.date


@transaction.atomic
def reconcile(limit=200):
    pending = Participation.objects.filter(status="Scheduled").values("session_id")
    due = list(
        Session.objects.select_for_update(skip_locked=True)
        .filter(ends_at__lte=timezone.now(), pk__in=pending)
        .order_by("ends_at", "pk")[:limit]
    )
    return complete_sessions(due)


def complete_sessions(sessions):
    patient_ids = Participation.objects.filter(session__in=sessions, status="Scheduled").values_list(
        "patient_id", flat=True
    )
    list(Patient.objects.select_for_update().filter(pk__in=patient_ids).order_by("pk"))
    for session in sessions:
        before = snapshot(session)
        for part in session.participations.filter(status="Scheduled").select_related("patient"):
            part.session = session
            part.status = "Completed"
            reconcile_charge(part)
        session.version += 1
        session.save(update_fields=["version"])
        AuditLog.objects.create(
            action="session.autocomplete", reference=str(session.pk), before=before, after=snapshot(session)
        )
    return len(sessions)


@transaction.atomic
def publish(actor, day):
    editable(actor, day)
    if day not in [now().date(), next_operating_day(now().date())]:
        raise ValidationError("Publish the current or next operational day.")
    schedule, _ = DailySchedule.objects.get_or_create(date=day)
    schedule = DailySchedule.objects.select_for_update().get(pk=schedule.pk)
    if not schedule.published_at:
        schedule.published_at = timezone.now()
        schedule.published_by = actor
        schedule.save()
        AuditLog.objects.create(actor=actor, action="schedule.publish", reference=str(day))
    Notification.objects.filter(key=f"publish:{day}").update(resolved=True)
    return schedule


def publication_reminder():
    current = now()
    days = [current.date()] if current.date().weekday() in settings.OPERATING_DAYS else []
    if current.time() >= time(18, 30):
        days.append(next_operating_day(current.date()))
    for day in days:
        if not DailySchedule.objects.filter(date=day, published_at__isnull=False).exists():
            Notification.objects.get_or_create(
                key=f"publish:{day}", defaults={"kind": "publication", "date": day}
            )
    Notification.objects.filter(kind="publication", date__lt=current.date(), resolved=False).update(
        resolved=True
    )


def therapist_visible(day, published_at):
    current = now()
    # Early next-day publication must not expose three dates before yesterday expires.
    newer = DailySchedule.objects.filter(
        date__gt=day, date__lte=next_operating_day(current.date()), published_at__isnull=False
    ).count()
    return (
        bool(published_at)
        and newer < 2
        and day <= next_operating_day(current.date())
        and current < datetime.combine(day + timedelta(days=1), time(10), IST)
    )

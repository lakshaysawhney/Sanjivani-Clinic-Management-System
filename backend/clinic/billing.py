from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .models import LedgerEntry, Notification, Patient, AuditLog


def balance(patient):
    return LedgerEntry.objects.filter(patient=patient).aggregate(total=Sum("amount_paise"))["total"] or 0


def refresh_dues(patient):
    negative = balance(patient) < 0
    notification = Notification.objects.filter(key=f"dues:{patient.pk}").first()
    if negative or notification:
        Notification.objects.update_or_create(
            key=f"dues:{patient.pk}", defaults={"kind": "dues", "patient": patient, "resolved": not negative}
        )


def reconcile_charge(part, actor=None):
    # Caller owns the session lock and locks affected patients in ascending ID order.
    desired = 0
    if part.status == "Completed" and str(part.session.schedule.date) >= settings.ACCOUNTING_START_DATE:
        if part.fee_snapshot is None or part.fee_therapy_id != part.session.therapy_id:
            part.fee_snapshot = part.session.therapy.fee_paise
            part.fee_therapy = part.session.therapy
        desired = part.fee_snapshot
    if desired != part.billed_paise:
        part.billing_revision += 1
        prefix = f"participation:{part.pk}:{part.billing_revision}"
        if part.billed_paise:
            original = (
                LedgerEntry.objects.filter(participation=part, kind="charge").order_by("-created_at").first()
            )
            LedgerEntry.objects.create(
                patient=part.patient,
                amount_paise=part.billed_paise,
                kind="charge_reversal",
                source=prefix + ":reverse",
                participation=part,
                reverses=original,
                description="Session charge correction",
                actor=actor,
                effective_at=timezone.now(),
            )
        if desired:
            LedgerEntry.objects.create(
                patient=part.patient,
                amount_paise=-desired,
                kind="charge",
                source=prefix + ":charge",
                participation=part,
                description=part.session.therapy.name,
                actor=actor,
                effective_at=part.session.ends_at,
            )
        part.billed_paise = desired
    part.save()
    refresh_dues(part.patient)


@transaction.atomic
def post_entry(patient_id, actor, data, source):
    patient = Patient.objects.select_for_update().get(pk=patient_id)
    kind = data.get("kind")
    amount = data.get("amount_paise")
    if type(amount) is not int or abs(amount) > 100_000_000:
        raise ValidationError("Enter a valid amount in paise, up to INR 1,000,000.")
    if kind not in ["opening", "payment", "adjustment"]:
        raise ValidationError("Choose opening balance, payment or adjustment.")
    if kind == "payment" and amount <= 0:
        raise ValidationError("Payments must be positive.")
    if kind == "opening" and LedgerEntry.objects.filter(patient=patient, kind="opening").exists():
        raise ValidationError("An opening balance already exists. Use an adjustment.")
    if kind == "adjustment" and (not amount or not data.get("description", "").strip()):
        raise ValidationError("Adjustments require a non-zero amount and a reason.")
    from django.utils.dateparse import parse_datetime

    effective = parse_datetime(data["effective_at"]) if data.get("effective_at") else timezone.now()
    if not effective or timezone.is_naive(effective):
        raise ValidationError("Payment time must include a timezone.")
    entry = LedgerEntry.objects.create(
        patient=patient,
        amount_paise=amount,
        kind=kind,
        source=source,
        description=data.get("description", "")[:500],
        actor=actor,
        effective_at=effective,
    )
    AuditLog.objects.create(
        actor=actor,
        action="ledger.post",
        reference=str(entry.pk),
        after={"amount_paise": amount, "kind": kind},
    )
    refresh_dues(patient)
    return entry


@transaction.atomic
def reverse_payment(entry_id, actor, reason, source):
    original = LedgerEntry.objects.get(pk=entry_id)
    patient = Patient.objects.select_for_update().get(pk=original.patient_id)
    if original.kind not in ["payment", "opening", "adjustment"] or hasattr(original, "reversal"):
        raise ValidationError("This entry cannot be reversed again.")
    if not reason.strip():
        raise ValidationError("A correction reason is required.")
    entry = LedgerEntry.objects.create(
        patient=patient,
        amount_paise=-original.amount_paise,
        kind="payment_reversal",
        source=source,
        reverses=original,
        actor=actor,
        effective_at=timezone.now(),
        description=reason[:500],
    )
    AuditLog.objects.create(
        actor=actor,
        action="ledger.reverse",
        reference=str(original.pk),
        after={"reversal": str(entry.pk)},
        reason=reason,
    )
    refresh_dues(patient)
    return entry

import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q


class Patient(models.Model):
    name = models.CharField(max_length=160)
    active = models.BooleanField(default=True)
    special_fee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FrequencyPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="plans")
    weekly = models.PositiveSmallIntegerField(default=0)
    monthly = models.PositiveSmallIntegerField(default=0)
    effective_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Therapy(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=60)
    fee_paise = models.PositiveIntegerField()
    group = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]


class DailySchedule(models.Model):
    date = models.DateField(unique=True)
    published_at = models.DateTimeField(null=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule = models.ForeignKey(DailySchedule, on_delete=models.PROTECT, related_name="sessions")
    slot = models.PositiveSmallIntegerField()
    therapy = models.ForeignKey(Therapy, on_delete=models.PROTECT)
    ends_at = models.DateTimeField(db_index=True)
    version = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=Q(slot__gte=0, slot__lte=9), name="valid_slot")]


class Assignment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT, related_name="assignments")
    provider = models.ForeignKey("accounts.Provider", on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["session", "provider"], name="one_assignment")]


class Participation(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "Scheduled"
        COMPLETED = "Completed"
        CANCELLED = "Cancelled"

    session = models.ForeignKey(Session, on_delete=models.PROTECT, related_name="participations")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="participations")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.SCHEDULED)
    fee_snapshot = models.PositiveIntegerField(null=True)
    fee_therapy = models.ForeignKey(Therapy, null=True, on_delete=models.PROTECT)
    billing_revision = models.PositiveIntegerField(default=0)
    billed_paise = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["session", "patient"], name="one_participation"),
            models.CheckConstraint(
                condition=Q(status__in=["Scheduled", "Completed", "Cancelled"]),
                name="valid_participation_status",
            ),
        ]


class ProviderReservation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    provider = models.ForeignKey("accounts.Provider", on_delete=models.PROTECT)
    date = models.DateField()
    slot = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["provider", "date", "slot"], name="provider_slot_unique")
        ]


class PatientReservation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    date = models.DateField()
    slot = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["patient", "date", "slot"], name="patient_slot_unique")
        ]


class LedgerEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="ledger")
    amount_paise = models.BigIntegerField()
    kind = models.CharField(max_length=24)
    source = models.CharField(max_length=150, unique=True)
    participation = models.ForeignKey(Participation, null=True, on_delete=models.PROTECT)
    reverses = models.OneToOneField("self", null=True, on_delete=models.PROTECT, related_name="reversal")
    description = models.CharField(max_length=500)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    effective_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]


class Notification(models.Model):
    key = models.CharField(max_length=150, unique=True)
    kind = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.PROTECT)
    date = models.DateField(null=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmailOutbox(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    event_key = models.CharField(max_length=160, unique=True)
    kind = models.CharField(max_length=24, default="schedule")
    encrypted_payload = models.TextField(blank=True)
    state = models.CharField(max_length=20, default="pending")
    attempts = models.PositiveSmallIntegerField(default=0)
    next_attempt = models.DateTimeField()
    last_error = models.CharField(max_length=100, blank=True)
    sent_at = models.DateTimeField(null=True)
    message_id = models.CharField(max_length=200, blank=True)


class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    action = models.CharField(max_length=60)
    reference = models.CharField(max_length=120)
    before = models.JSONField(default=dict)
    after = models.JSONField(default=dict)
    reason = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class IdempotencyRecord(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    key = models.UUIDField()
    digest = models.CharField(max_length=64)
    response = models.JSONField(null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["actor", "key"], name="actor_idempotency_key")]


class IntegrationSecret(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ciphertext = models.TextField()

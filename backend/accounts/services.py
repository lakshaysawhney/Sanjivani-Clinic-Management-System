import hashlib
import secrets
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from .models import CredentialToken, User
from clinic.models import EmailOutbox, AuditLog


@transaction.atomic
def issue_token(user, actor=None, revoke=False):
    from clinic.email_service import encrypt

    # Resetting credentials revokes existing sessions via password hash change.
    user = User.objects.select_for_update().get(pk=user.pk)
    if revoke:
        user.set_unusable_password()
        user.pending_activation = True
        user.save()
    CredentialToken.objects.filter(user=user, used_at__isnull=True).update(used_at=timezone.now())
    raw = secrets.token_urlsafe(48)
    token = CredentialToken.objects.create(
        user=user,
        digest=hashlib.sha256(raw.encode()).hexdigest(),
        expires_at=timezone.now() + timedelta(hours=24),
    )
    EmailOutbox.objects.create(
        recipient=user,
        event_key=f"activation:{token.pk}",
        kind="activation",
        encrypted_payload=encrypt(raw),
        next_attempt=timezone.now(),
    )
    AuditLog.objects.create(actor=actor, action="staff.reset_credentials", reference=str(user.pk))


@transaction.atomic
def consume_token(raw, password):
    token = (
        CredentialToken.objects.select_for_update()
        .select_related("user")
        .filter(
            digest=hashlib.sha256(raw.encode()).hexdigest(),
            used_at__isnull=True,
            expires_at__gt=timezone.now(),
        )
        .first()
    )
    if not token or not token.user.is_active:
        raise ValidationError("This activation link is invalid or expired.")
    validate_password(password, token.user)
    token.user.set_password(password)
    token.user.pending_activation = False
    token.user.save()
    token.used_at = timezone.now()
    token.save()
    AuditLog.objects.create(actor=token.user, action="staff.activate", reference=str(token.user_id))

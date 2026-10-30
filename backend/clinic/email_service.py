import base64
from datetime import timedelta
from email.message import EmailMessage
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from .models import IntegrationSecret, EmailOutbox


def encrypt(value):
    if not settings.TOKEN_ENCRYPTION_KEY:
        raise ValueError("Email encryption key is not configured")
    return Fernet(settings.TOKEN_ENCRYPTION_KEY.encode()).encrypt(value.encode()).decode()


def decrypt(value):
    return Fernet(settings.TOKEN_ENCRYPTION_KEY.encode()).decrypt(value.encode()).decode()


def send_email(item):
    secret = IntegrationSecret.objects.get(name="gmail_refresh_token")
    credentials = Credentials(
        None,
        refresh_token=decrypt(secret.ciphertext),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GMAIL_CLIENT_ID,
        client_secret=settings.GMAIL_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )
    credentials.refresh(Request())
    message = EmailMessage()
    message["From"] = settings.GMAIL_SENDER
    message["To"] = item.recipient.email
    message["Message-ID"] = f"<sanjivani-outbox-{item.pk}@notifications.invalid>"
    if item.kind == "activation":
        message["Subject"] = "Sanjivani: Set your password"
        message.set_content(
            f"Set your clinic password within 24 hours: {settings.APP_ORIGIN}/activate#token={decrypt(item.encrypted_payload)}\nIf you did not expect this invitation, contact clinic administration."
        )
    else:
        message["Subject"] = "Sanjivani: Your schedule has been updated"
        message.set_content(
            f"Your published clinic schedule has changed. Please sign in to view the latest schedule: {settings.APP_ORIGIN}/schedule"
        )
    service = build("gmail", "v1", credentials=credentials, cache_discovery=False)
    return (
        service.users()
        .messages()
        .send(userId="me", body={"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()})
        .execute()["id"]
    )


def process_outbox(limit=20):
    sent = 0
    for _ in range(limit):
        with transaction.atomic():
            item = (
                EmailOutbox.objects.select_for_update(skip_locked=True)
                .filter(state="pending", next_attempt__lte=timezone.now())
                .order_by("next_attempt")
                .first()
            )
            if not item:
                break
            if not item.recipient.is_active:
                item.state = "cancelled"
                item.save()
                continue
            # Mark before I/O. A crash/ambiguous timeout needs review rather than duplicate sending.
            item.state = "sending"
            item.attempts += 1
            item.save()
        try:
            message_id = send_email(item)
        except Exception as exc:
            from googleapiclient.errors import HttpError

            definite = isinstance(exc, (IntegrationSecret.DoesNotExist, ValueError)) or isinstance(
                exc, HttpError
            )
            item.state = ("pending" if item.attempts < 5 else "failed") if definite else "uncertain"
            item.last_error = type(exc).__name__[:100]
            item.next_attempt = timezone.now() + timedelta(seconds=min(3600, 60 * 2**item.attempts))
        else:
            item.state = "sent"
            item.sent_at = timezone.now()
            item.message_id = message_id
            item.encrypted_payload = ""
            sent += 1
        item.save()
    return sent

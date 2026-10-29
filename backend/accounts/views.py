import hashlib
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import User, LoginAttempt
from .services import consume_token, issue_token


def user_data(user):
    return {
        "id": user.pk,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "provider_id": getattr(getattr(user, "provider", None), "pk", None),
    }


class CSRFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = str(request.data.get("username", ""))[:150]
        # Login failures are durable and shared across Gunicorn workers.
        keys = [
            hashlib.sha256(("user:" + username.lower()).encode()).hexdigest(),
            hashlib.sha256(
                (
                    "ip:" + request.META.get("HTTP_X_CLINIC_CLIENT_IP", request.META.get("REMOTE_ADDR", ""))
                ).encode()
            ).hexdigest(),
        ]
        with transaction.atomic():
            for key in sorted(keys):
                attempt, _ = LoginAttempt.objects.get_or_create(key=key, defaults={"window": timezone.now()})
                attempt = LoginAttempt.objects.select_for_update().get(pk=attempt.pk)
                if attempt.window < timezone.now() - timedelta(minutes=15):
                    attempt.window = timezone.now()
                    attempt.count = 0
                if attempt.count >= 10:
                    return Response({"detail": "Too many attempts. Try again in 15 minutes."}, status=429)
                attempt.count += 1
                attempt.save()
        user = authenticate(request, username=username, password=request.data.get("password", ""))
        if not user or user.pending_activation:
            raise ValidationError("Invalid credentials or account awaiting activation.")
        LoginAttempt.objects.filter(key__in=keys).update(count=0)
        login(request, user)
        if request.data.get("shared_computer"):
            request.session.set_expiry(0)
        return Response(user_data(user))


class MeView(APIView):
    def get(self, request):
        return Response(user_data(request.user))


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"ok": True})


class PasswordView(APIView):
    def post(self, request):
        if not request.user.check_password(request.data.get("current_password", "")):
            raise ValidationError("The current password is incorrect.")
        password = request.data.get("new_password", "")
        validate_password(password, request.user)
        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return Response({"ok": True})


@method_decorator(csrf_protect, name="dispatch")
class ActivationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        consume_token(str(request.data.get("token", "")), request.data.get("password", ""))
        return Response({"ok": True})


@method_decorator(csrf_protect, name="dispatch")
class ResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = str(request.data.get("email", "")).lower()
        key = hashlib.sha256(("reset:" + email).encode()).hexdigest()
        with transaction.atomic():
            attempt, _ = LoginAttempt.objects.get_or_create(key=key, defaults={"window": timezone.now()})
            attempt = LoginAttempt.objects.select_for_update().get(pk=attempt.pk)
            if attempt.count and attempt.window > timezone.now() - timedelta(minutes=15):
                return Response({"ok": True})
            attempt.count = 1
            attempt.window = timezone.now()
            attempt.save()
            user = User.objects.filter(email__iexact=email, is_active=True).first()
            if user and settings.TOKEN_ENCRYPTION_KEY:
                issue_token(user)
        return Response({"ok": True})


class GmailAuthorizeView(APIView):
    def post(self, request):
        if request.user.role != "ADMIN":
            raise PermissionDenied()
        flow = gmail_flow()
        url, state = flow.authorization_url(
            access_type="offline",
            prompt="consent",
            include_granted_scopes="true",
            login_hint=settings.GMAIL_SENDER,
        )
        request.session["gmail_oauth_state"] = state
        return Response({"url": url})


def gmail_flow(state=None):
    from google_auth_oauthlib.flow import Flow

    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GMAIL_CLIENT_ID,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["https://www.googleapis.com/auth/gmail.send"],
        state=state,
        redirect_uri=settings.APP_ORIGIN + "/api/auth/gmail/callback/",
    )


class GmailCallbackView(APIView):
    def get(self, request):
        import secrets

        if request.user.role != "ADMIN":
            raise PermissionDenied()
        state = request.session.pop("gmail_oauth_state", "")
        if not state or not secrets.compare_digest(state, request.query_params.get("state", "")):
            raise PermissionDenied("Invalid OAuth state.")
        flow = gmail_flow(state)
        flow.fetch_token(code=request.query_params.get("code", ""))
        if not flow.credentials.refresh_token:
            raise ValidationError("Offline consent did not provide a refresh credential.")
        from clinic.email_service import encrypt
        from clinic.models import IntegrationSecret

        IntegrationSecret.objects.update_or_create(
            name="gmail_refresh_token", defaults={"ciphertext": encrypt(flow.credentials.refresh_token)}
        )
        return Response(
            {"ok": True, "detail": "Email authorization saved. Return to the clinic application."}
        )

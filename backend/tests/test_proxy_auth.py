"""Regressions for the production proxy, session and CSRF boundaries."""

import uuid

import pytest
from freezegun import freeze_time
from rest_framework.test import APIClient

from clinic.models import IdempotencyRecord

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def production_boundary(settings):
    settings.DEBUG = False
    settings.SECURE_SSL_REDIRECT = False
    settings.PROXY_SECRET = "synthetic-test-proxy"


@pytest.mark.parametrize("secret", [None, "", "incorrect"])
def test_proxy_rejects_untrusted_requests_before_authentication(secret):
    client = APIClient()
    if secret is not None:
        client.credentials(HTTP_X_CLINIC_PROXY=secret)
    response = client.get("/api/auth/csrf/")
    assert response.status_code == 403
    assert response.json() == {"detail": "Use the clinic application origin."}


def test_proxy_requires_configured_secret(settings):
    settings.PROXY_SECRET = ""
    response = APIClient(HTTP_X_CLINIC_PROXY="synthetic-test-proxy").get("/api/auth/csrf/")
    assert response.status_code == 403


@freeze_time("2026-10-28 09:00:00+05:30")
def test_trusted_proxy_preserves_session_csrf_and_deactivation(team, booking):
    client = APIClient(enforce_csrf_checks=True, HTTP_X_CLINIC_PROXY="synthetic-test-proxy")
    assert client.get("/api/auth/me/").status_code == 403
    body = {"username": "reception", "password": "Synthetic-only-Password-482!"}
    assert client.post("/api/auth/login/", body).status_code == 403
    token = client.get("/api/auth/csrf/").json()["csrfToken"]
    assert client.post("/api/auth/login/", body, HTTP_X_CSRFTOKEN=token).status_code == 200
    assert client.get("/api/auth/me/").json()["role"] == "RECEPTIONIST"
    # Login rotates CSRF. A valid session and trusted proxy never waive it.
    token = client.get("/api/auth/csrf/").json()["csrfToken"]
    key = str(uuid.uuid4())
    assert client.post("/api/sessions/", booking, format="json", HTTP_IDEMPOTENCY_KEY=key).status_code == 403
    assert IdempotencyRecord.objects.count() == 0
    assert (
        client.post(
            "/api/sessions/", booking, format="json", HTTP_IDEMPOTENCY_KEY=key, HTTP_X_CSRFTOKEN=token
        ).status_code
        == 200
    )
    assert client.get("/api/staff/").status_code == 403
    team["reception"].is_active = False
    team["reception"].save()
    assert client.get("/api/auth/me/").status_code == 403

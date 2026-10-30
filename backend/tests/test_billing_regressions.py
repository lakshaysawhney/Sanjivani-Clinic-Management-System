"""Regressions for immutable corrections and concurrent financial requests."""

import copy
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from django.db import close_old_connections
from freezegun import freeze_time
from rest_framework.test import APIClient

from accounts.models import User
from clinic.billing import balance, post_entry, reverse_payment
from clinic.models import AuditLog, IdempotencyRecord, LedgerEntry
from clinic.scheduling import reconcile, save_session

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def production_boundary(settings):
    settings.DEBUG = False
    settings.SECURE_SSL_REDIRECT = False
    settings.PROXY_SECRET = "synthetic-test-proxy"


@freeze_time("2026-10-28 12:00:00+05:30")
@pytest.mark.parametrize("therapy", ["OT", "GROUP"])
def test_repeated_corrections_reverse_only_the_active_charge(team, booking, therapy):
    data = {**booking, "therapy": therapy}
    if therapy == "GROUP":
        data["providers"] = [team["one"].provider.pk, team["two"].provider.pk]
        data["participants"] = [{"patient_id": team["patient"].pk}, {"patient_id": team["other"].pk}]
    session = save_session(team["admin"], data)
    original_rows = list(LedgerEntry.objects.values())
    # All created_at values tie; UUID or timestamp order cannot identify the live charge.
    for _ in range(3):
        cancelled = copy.deepcopy(data)
        cancelled["participants"][0]["status"] = "Cancelled"
        session = save_session(team["admin"], {**cancelled, "version": session.version}, session.pk)
        assert balance(team["patient"]) == 0
        session = save_session(team["admin"], {**data, "version": session.version}, session.pk)
        assert balance(team["patient"]) == -90000
        if therapy == "GROUP":
            assert balance(team["other"]) == -90000
    session = save_session(
        team["admin"],
        {**data, "therapy": "ASSESS_2500" if therapy == "OT" else "GROUP", "version": session.version},
        session.pk,
    )
    assert balance(team["patient"]) == (-250000 if therapy == "OT" else -90000)
    for reversal in LedgerEntry.objects.filter(kind="charge_reversal").select_related("reverses"):
        assert reversal.reverses.kind == "charge"
        assert reversal.participation_id == reversal.reverses.participation_id
        assert reversal.amount_paise == -reversal.reverses.amount_paise
    for row in original_rows:
        assert LedgerEntry.objects.values().get(pk=row["id"]) == row
    before = list(LedgerEntry.objects.values())
    save_session(
        team["admin"], {**data, "therapy": session.therapy_id, "version": session.version}, session.pk
    )
    assert reconcile() == 0
    assert list(LedgerEntry.objects.values()) == before


@pytest.mark.django_db(transaction=True)
@freeze_time("2026-10-28 09:00:00+05:30")
def test_concurrent_identical_mutations_return_one_response(team, booking):
    barrier = Barrier(2)
    key = str(uuid.uuid4())

    def worker(_):
        close_old_connections()
        try:
            client = APIClient(HTTP_X_CLINIC_PROXY="synthetic-test-proxy")
            client.force_authenticate(User.objects.get(pk=team["reception"].pk))
            barrier.wait(timeout=15)
            response = client.post("/api/sessions/", booking, format="json", HTTP_IDEMPOTENCY_KEY=key)
            return response.status_code, response.json()
        finally:
            close_old_connections()

    with ThreadPoolExecutor(2) as executor:
        results = list(executor.map(worker, range(2)))
    assert results[0][0] == 200
    assert results[0] == results[1]
    assert IdempotencyRecord.objects.count() == 1
    assert AuditLog.objects.filter(action="session.create").count() == 1


@pytest.mark.django_db(transaction=True)
def test_concurrent_payment_reversals_append_once(team):
    payment = post_entry(
        team["patient"].pk, team["admin"], {"kind": "payment", "amount_paise": 90000}, "payment"
    )
    barrier = Barrier(2)

    def worker(index):
        from rest_framework.exceptions import ValidationError

        close_old_connections()
        try:
            actor = User.objects.get(pk=team["admin"].pk)
            barrier.wait(timeout=15)
            try:
                reverse_payment(payment.pk, actor, "Synthetic correction", f"reverse:{index}")
                return "reversed"
            except ValidationError:
                return "rejected"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(2) as executor:
        results = list(executor.map(worker, range(2)))
    assert sorted(results) == ["rejected", "reversed"]
    assert balance(team["patient"]) == 0
    assert LedgerEntry.objects.filter(reverses=payment).count() == 1

"""Participation history must outlive edits to the shared appointment shell."""

import pytest
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from django.db import close_old_connections, transaction, IntegrityError
from freezegun import freeze_time
from rest_framework.test import APIClient
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from clinic.api import session_data
from clinic.billing import balance, post_entry
from clinic.models import (
    LedgerEntry,
    Patient,
    PatientReservation,
    ProviderReservation,
    AuditLog,
    IdempotencyRecord,
)
from clinic.scheduling import save_session, reconcile
from clinic.api_errors import Conflict

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def proxy_boundary(settings):
    settings.PROXY_SECRET = "synthetic-test-proxy"
    settings.SECURE_SSL_REDIRECT = False


def client_for(user):
    client = APIClient(HTTP_X_CLINIC_PROXY="synthetic-test-proxy")
    client.force_authenticate(user)
    return client


def edit(team, session, data, **changes):
    return save_session(team["admin"], {**data, **changes, "version": session.version}, session.pk)


@freeze_time("2026-10-28 12:00:00+05:30")
def test_ordinary_replacement_round_trip_excludes_retired_child(team, booking):
    session = save_session(team["admin"], booking)
    replacement = {**booking, "participants": [{"patient_id": team["other"].pk}]}
    session = save_session(team["admin"], {**replacement, "version": session.version}, session.pk)
    payload = session_data(session, team["admin"])
    assert [p["patient_id"] for p in payload["participants"]] == [team["other"].pk]
    session = save_session(team["admin"], payload, session.pk)
    assert session.participations.exclude(status="Cancelled").count() == 1
    assert session.participations.get(patient=team["patient"]).status == "Cancelled"
    assert balance(team["patient"]) == 0
    assert balance(team["other"]) == -90000


@freeze_time("2026-11-02 12:00:00+05:30")
def test_removed_cancellation_keeps_original_context_after_move(team, booking):
    session = save_session(team["admin"], booking)
    moved = {
        **booking,
        "date": "2026-11-02",
        "slot": 1,
        "therapy": "ASSESS_2500",
        "providers": [team["two"].provider.pk],
        "participants": [{"patient_id": team["other"].pk}],
    }
    save_session(team["admin"], {**moved, "version": session.version}, session.pk)
    response = client_for(team["admin"]).get(f"/api/patients/{team['patient'].pk}/?month=2026-10")
    assert response.status_code == 200
    assert response.data["cancelled"] == 1
    history = response.data["history"][0]
    assert (history["date"], history["slot"], history["therapy"], history["providers"]) == (
        booking["date"],
        booking["slot"],
        "OT",
        booking["providers"],
    )
    current = client_for(team["admin"]).get(f"/api/patients/{team['patient'].pk}/?month=2026-11")
    assert current.data["cancelled"] == 0
    frequency = client_for(team["admin"]).get("/api/frequency/?month=2026-10&week=2026-10-28")
    assert next(p for p in frequency.data if p["id"] == team["patient"].pk)["cancelled"] == 1
    daily = client_for(team["reception"]).get("/api/schedule/?date=2026-10-28")
    assert daily.data["cancelled_history"][0]["providers"] == booking["providers"]


@freeze_time("2026-10-28 12:00:00+05:30")
def test_equal_price_category_change_replaces_charge_lineage(team, booking):
    session = save_session(team["admin"], booking)
    original = LedgerEntry.objects.get(kind="charge")
    save_session(team["admin"], {**booking, "therapy": "ABA", "version": session.version}, session.pk)
    assert balance(team["patient"]) == -90000
    assert LedgerEntry.objects.filter(reverses=original, kind="charge_reversal").count() == 1
    active = LedgerEntry.objects.get(kind="charge", reversal__isnull=True)
    assert active.description == "ABA"


@freeze_time("2026-10-28 12:00:00+05:30")
def test_completed_move_reverses_charge_with_old_effective_time(team, booking):
    session = save_session(team["admin"], booking)
    original = LedgerEntry.objects.get(kind="charge")
    session = edit(team, session, booking, slot=1)
    assert LedgerEntry.objects.filter(reverses=original).exists()
    assert LedgerEntry.objects.get(kind="charge", reversal__isnull=True).effective_at == session.ends_at
    assert LedgerEntry.objects.get(pk=original.pk).effective_at == original.effective_at


@freeze_time("2026-10-28 12:00:00+05:30")
def test_patient_history_orders_by_original_cancelled_slot(team, booking):
    session = save_session(team["admin"], {**booking, "slot": 2})
    edit(team, session, booking, participants=[{"patient_id": team["other"].pk}])
    save_session(team["admin"], {**booking, "slot": 1})
    history = (
        client_for(team["admin"]).get(f"/api/patients/{team['patient'].pk}/?month=2026-10").data["history"]
    )
    assert [s["slot"] for s in history] == [1, 2]


@freeze_time("2026-10-29 12:00:00+05:30")
def test_reception_cannot_restore_retired_cancellation_after_original_cutoff(team, booking):
    session = save_session(team["admin"], booking)
    moved = {**booking, "date": "2026-10-30", "participants": [{"patient_id": team["other"].pk}]}
    session = edit(team, session, moved)
    with pytest.raises(PermissionDenied):
        save_session(
            team["reception"], {**booking, "date": "2026-10-30", "version": session.version}, session.pk
        )
    session = edit(team, session, booking, date="2026-10-30")
    assert session.participations.get(patient=team["patient"]).status == "Scheduled"


@freeze_time("2026-10-28 12:00:00+05:30")
def test_group_counts_membership_restoration_and_released_reservations(team, booking):
    third = Patient.objects.create(name="Synthetic Child Gamma")
    data = {
        **booking,
        "therapy": "GROUP",
        "providers": [team["one"].provider.pk, team["two"].provider.pk],
        "participants": [
            {"patient_id": team["patient"].pk},
            {"patient_id": team["other"].pk},
            {"patient_id": third.pk, "status": "Cancelled"},
        ],
    }
    session = save_session(team["admin"], data)
    for child in (team["patient"], team["other"]):
        profile = client_for(team["admin"]).get(f"/api/patients/{child.pk}/?month=2026-10").data
        assert profile["completed"] == 1
        assert profile["categories"]["GROUP"] == 1
        assert sorted(profile["providers"].values()) == [1, 1]
        assert balance(child) == -90000
    for key in ("one", "two"):
        history = client_for(team[key]).get("/api/history/?month=2026-10").data
        assert history["total"] == 1
    assert balance(third) == 0
    assert LedgerEntry.objects.filter(kind="charge").count() == 2
    assert PatientReservation.objects.filter(session=session).count() == 2
    assert ProviderReservation.objects.filter(session=session).count() == 2

    # Removing one member must neither bill it nor release the shared providers.
    remaining = {**data, "participants": [{"patient_id": team["other"].pk}]}
    session = edit(team, session, remaining)
    assert balance(team["patient"]) == 0
    assert balance(team["other"]) == -90000
    assert ProviderReservation.objects.filter(session=session).count() == 2
    replacement = save_session(team["admin"], {**booking, "providers": [team["admin"].provider.pk]})
    rows = list(LedgerEntry.objects.values())
    with pytest.raises(IntegrityError), transaction.atomic():
        edit(team, session, data)
    assert list(LedgerEntry.objects.values()) == rows
    assert session.participations.get(patient=team["patient"]).status == "Cancelled"

    replacement = edit(
        team,
        replacement,
        booking,
        providers=[team["admin"].provider.pk],
        participants=[{"patient_id": team["patient"].pk, "status": "Cancelled"}],
    )
    session.refresh_from_db()
    session = edit(team, session, data)
    assert session.participations.get(patient=team["patient"]).removed is False
    assert balance(team["patient"]) == -90000
    cancelled = {**data, "participants": [{**p, "status": "Cancelled"} for p in data["participants"]]}
    session = edit(team, session, cancelled)
    assert not ProviderReservation.objects.filter(session=session).exists()
    assert not PatientReservation.objects.filter(session=session).exists()
    for key in ("one", "two"):
        assert client_for(team[key]).get("/api/history/?month=2026-10").data["total"] == 0
    assert balance(team["patient"]) == balance(team["other"]) == 0
    save_session(team["admin"], {**booking, "participants": [{"patient_id": third.pk}]})


@freeze_time("2026-11-02 12:00:00+05:30")
@pytest.mark.parametrize("removed", [False, True])
def test_cancellation_context_survives_repeated_edits_then_restoration(team, booking, removed):
    session = save_session(team["admin"], booking)
    part = session.participations.get()
    snapshot = part.fee_snapshot
    session = edit(
        team, session, booking, participants=[{"patient_id": team["patient"].pk, "status": "Cancelled"}]
    )
    original = session.participations.get().cancelled_context
    moved = {
        **booking,
        "date": "2026-11-02",
        "slot": 1,
        "therapy": "ABA",
        "providers": [team["two"].provider.pk],
        "participants": [{"patient_id": team["other"].pk}]
        if removed
        else [{"patient_id": team["patient"].pk, "status": "Cancelled"}],
    }
    session = edit(team, session, moved)
    session = edit(team, session, moved, slot=2)
    part.refresh_from_db()
    assert part.cancelled_context == original
    assert part.attendance_date.isoformat() == "2026-10-28"
    assert part.fee_snapshot == snapshot
    assert balance(team["patient"]) == 0
    session.therapy.fee_paise = 123456
    session.therapy.save()
    session = edit(team, session, moved, therapy="OT", participants=[{"patient_id": team["patient"].pk}])
    part.refresh_from_db()
    assert part.pk == session.participations.get(patient=team["patient"]).pk
    assert part.cancelled_context is None
    assert part.attendance_date.isoformat() == "2026-11-02"
    assert part.fee_snapshot == 90000
    profile = client_for(team["admin"]).get(f"/api/patients/{team['patient'].pk}/?month=2026-10").data
    assert profile["cancelled"] == 0


@freeze_time("2026-10-28 12:00:00+05:30")
def test_accounting_cutoff_corrections_and_exact_paise(team, booking, settings):
    settings.ACCOUNTING_START_DATE = "2026-10-28"
    session = save_session(team["admin"], {**booking, "date": "2026-09-30"})
    assert balance(team["patient"]) == 0
    session = edit(team, session, booking)
    original_rows = list(LedgerEntry.objects.values())
    post_entry(
        team["patient"].pk, team["reception"], {"kind": "payment", "amount_paise": 90001}, "exact-paise"
    )
    assert balance(team["patient"]) == 1
    session = edit(team, session, booking, date="2026-09-30")
    assert balance(team["patient"]) == 90001
    session = edit(team, session, booking)
    assert balance(team["patient"]) == 1
    for row in original_rows:
        assert LedgerEntry.objects.values().get(pk=row["id"]) == row
    rows = list(LedgerEntry.objects.values())
    edit(team, session, booking)
    assert reconcile() == 0
    assert list(LedgerEntry.objects.values()) == rows


@pytest.mark.parametrize("therapy", ["OT", "GROUP"])
@pytest.mark.parametrize("clock,allowed", [("17:59:59", True), ("18:00:00", False), ("18:15:00", False)])
def test_financial_correction_cutoff_is_enforced_on_writes(team, booking, therapy, clock, allowed):
    data = {**booking, "therapy": therapy}
    with freeze_time("2026-10-28 17:00:00+05:30"):
        session = save_session(team["reception"], data)
    payload = {
        **data,
        "version": session.version,
        "participants": [{"patient_id": team["patient"].pk, "status": "Cancelled"}],
    }
    with freeze_time("2026-10-28 " + clock + "+05:30"):
        response = client_for(team["reception"]).post(
            f"/api/sessions/{session.pk}/", payload, format="json", HTTP_IDEMPOTENCY_KEY=str(uuid.uuid4())
        )
        assert response.status_code == (200 if allowed else 403)
        assert balance(team["patient"]) == (0 if allowed else -90000)
        if not allowed:
            assert not IdempotencyRecord.objects.exists()
            save_session(team["admin"], payload, session.pk)
        assert balance(team["patient"]) == 0
        save_session(team["reception"], {**data, "date": "2026-10-29"})


@freeze_time("2026-10-28 18:15:00+05:30")
def test_final_slot_completed_correction_requires_admin(team, booking):
    session = save_session(team["admin"], {**booking, "slot": 9})
    assert balance(team["patient"]) == -90000
    payload = {
        **booking,
        "slot": 9,
        "version": session.version,
        "participants": [{"patient_id": team["patient"].pk, "status": "Cancelled"}],
    }
    with pytest.raises(PermissionDenied):
        save_session(team["reception"], payload, session.pk)
    save_session(team["admin"], payload, session.pk)
    assert balance(team["patient"]) == 0


@pytest.mark.django_db(transaction=True)
@freeze_time("2026-10-28 12:00:00+05:30")
@pytest.mark.parametrize("operation", ["same-version", "payment", "retry"])
@pytest.mark.parametrize("therapy", ["OT", "GROUP"])
def test_concurrent_financial_correction_serializes_and_retries(team, booking, operation, therapy):
    booking = {**booking, "therapy": therapy}
    if therapy == "GROUP":
        booking["providers"] = [team["one"].provider.pk, team["two"].provider.pk]
        booking["participants"] = [{"patient_id": team["patient"].pk}, {"patient_id": team["other"].pk}]
    session = save_session(team["admin"], booking)
    original = list(LedgerEntry.objects.values())
    barrier = Barrier(2)
    key = str(uuid.uuid4())
    payload = {
        **booking,
        "version": session.version,
        "participants": [{"patient_id": team["patient"].pk, "status": "Cancelled"}],
    }
    if therapy == "GROUP":
        payload["participants"].append({"patient_id": team["other"].pk, "status": "Completed"})

    def worker(index):
        close_old_connections()
        try:
            actor = User.objects.get(pk=team["admin" if index == 0 else "reception"].pk)
            barrier.wait(timeout=15)
            if index == 1 and operation == "payment":
                post_entry(
                    team["patient"].pk,
                    actor,
                    {"kind": "payment", "amount_paise": 90001},
                    "concurrent-payment",
                )
                return 200
            if operation == "retry":
                response = client_for(team["admin"]).post(
                    f"/api/sessions/{session.pk}/", payload, format="json", HTTP_IDEMPOTENCY_KEY=key
                )
                return response.status_code, response.json()
            try:
                save_session(actor, payload, session.pk)
                return 200
            except Conflict:
                return 409
        finally:
            close_old_connections()

    with ThreadPoolExecutor(2) as executor:
        results = list(executor.map(worker, range(2)))
    if operation == "retry":
        assert results[0] == results[1]
        assert results[0][0] == 200
        assert IdempotencyRecord.objects.count() == 1
    else:
        assert sorted(results) == ([200, 409] if operation == "same-version" else [200, 200])
    assert balance(team["patient"]) == (90001 if operation == "payment" else 0)
    assert LedgerEntry.objects.filter(kind="charge_reversal").count() == 1
    assert AuditLog.objects.filter(action="session.update").count() == 1
    if therapy == "GROUP":
        assert balance(team["other"]) == -90000
        assert LedgerEntry.objects.filter(patient=team["other"], kind="charge").count() == 1
    for row in original:
        assert LedgerEntry.objects.values().get(pk=row["id"]) == row

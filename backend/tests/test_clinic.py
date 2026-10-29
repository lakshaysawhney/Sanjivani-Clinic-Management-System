import copy
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from threading import Barrier
from unittest.mock import patch
import pytest
from freezegun import freeze_time
from django.db import IntegrityError, transaction, close_old_connections, DatabaseError
from django.test import override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.exceptions import PermissionDenied, ValidationError
from clinic.models import (
    Session,
    Participation,
    LedgerEntry,
    Notification,
    EmailOutbox,
    FrequencyPlan,
    AuditLog,
)
from clinic.scheduling import save_session, reconcile, publish, publication_reminder
from clinic.billing import balance, post_entry, reverse_payment
from clinic.time_rules import editable, history_scope
from accounts.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def proxy_settings(settings):
    # pytest disables DEBUG, so API tests must model the trusted edge proxy.
    # Keep the production boundary active instead of bypassing it in tests.
    settings.PROXY_SECRET = "synthetic-test-proxy"
    settings.SECURE_SSL_REDIRECT = False


def api_client(**kwargs):
    return APIClient(HTTP_X_CLINIC_PROXY="synthetic-test-proxy", **kwargs)


def client_for(user):
    client = api_client()
    client.force_authenticate(user)
    return client


@freeze_time("2026-10-28 04:00:00+00:00")
def test_booking_conflicts_and_cancellation(team, booking):
    first = save_session(team["reception"], booking)
    with pytest.raises(IntegrityError), transaction.atomic():
        save_session(team["admin"], {**booking, "participants": [{"patient_id": team["other"].pk}]})
    with pytest.raises(IntegrityError), transaction.atomic():
        save_session(team["admin"], {**booking, "providers": [team["two"].provider.pk]})
    save_session(
        team["reception"],
        {
            **booking,
            "version": first.version,
            "participants": [{"patient_id": team["patient"].pk, "status": "Cancelled"}],
        },
        first.pk,
    )
    save_session(team["reception"], {**booking, "participants": [{"patient_id": team["other"].pk}]})
    assert Session.objects.count() == 2
    assert Participation.objects.filter(status="Cancelled").count() == 1


@pytest.mark.parametrize("field", ["providers", "participants"])
@freeze_time("2026-10-28 04:00:00+00:00")
def test_ordinary_cardinality(team, booking, field):
    booking[field] += (
        [team["two"].provider.pk] if field == "providers" else [{"patient_id": team["other"].pk}]
    )
    with pytest.raises(ValidationError):
        save_session(team["reception"], booking)


@pytest.mark.parametrize(
    "code,fee",
    [
        ("OT", 90000),
        ("SP_EDU", 90000),
        ("ABA", 90000),
        ("GROUP", 90000),
        ("ASSESS_2000", 200000),
        ("ASSESS_2500", 250000),
        ("HOME_PLAN", 450000),
    ],
)
def test_all_fees_end_boundary_and_retries(team, booking, code, fee):
    with freeze_time("2026-10-28 10:00:00+05:30"):
        session = save_session(team["admin"], {**booking, "therapy": code})
    with freeze_time("2026-10-28 10:44:59+05:30"):
        assert reconcile() == 0
        assert balance(team["patient"]) == 0
    with freeze_time("2026-10-28 10:45:00+05:30"):
        assert reconcile() == 1
        assert reconcile() == 0
    assert balance(team["patient"]) == -fee
    charge = LedgerEntry.objects.get(kind="charge")
    assert charge.effective_at == session.ends_at
    assert Notification.objects.get(kind="dues").resolved is False


def test_group_attendance_and_billing(team, booking):
    data = {
        **booking,
        "therapy": "GROUP",
        "providers": [team["one"].provider.pk, team["two"].provider.pk],
        "participants": [
            {"patient_id": team["patient"].pk},
            {"patient_id": team["other"].pk, "status": "Cancelled"},
        ],
    }
    with freeze_time("2026-10-28 10:00:00+05:30"):
        session = save_session(team["admin"], data)
        publish(team["reception"], date(2026, 10, 28))
    with freeze_time("2026-10-28 11:00:00+05:30"):
        reconcile()
        for key in ["one", "two"]:
            result = client_for(team[key]).get("/api/history/?month=2026-10")
            assert result.status_code == 200
            assert result.data["total"] == 1
        profile = client_for(team["reception"]).get(f"/api/patients/{team['patient'].pk}/?month=2026-10").data
        assert profile["completed"] == 1
        assert list(profile["providers"].values()) == [1, 1]
    assert balance(team["patient"]) == -90000
    assert balance(team["other"]) == 0
    assert session.participations.get(patient=team["other"]).status == "Cancelled"


@freeze_time("2026-10-28 12:00:00+05:30")
def test_correction_reversal_and_fee_snapshot(team, booking):
    session = save_session(team["admin"], booking)
    assert balance(team["patient"]) == -90000
    session.therapy.fee_paise = 100000
    session.therapy.save()
    session = save_session(
        team["admin"],
        {
            **booking,
            "version": session.version,
            "participants": [{"patient_id": team["patient"].pk, "status": "Cancelled"}],
        },
        session.pk,
    )
    assert balance(team["patient"]) == 0
    session = save_session(
        team["admin"],
        {
            **booking,
            "version": session.version,
            "participants": [{"patient_id": team["patient"].pk, "status": "Completed"}],
        },
        session.pk,
    )
    assert balance(team["patient"]) == -90000
    session = save_session(
        team["admin"],
        {
            **booking,
            "therapy": "ASSESS_2500",
            "version": session.version,
            "participants": [{"patient_id": team["patient"].pk, "status": "Completed"}],
        },
        session.pk,
    )
    assert balance(team["patient"]) == -250000
    assert LedgerEntry.objects.filter(kind="charge_reversal").count() == 2
    assert AuditLog.objects.count() == 4


@pytest.mark.parametrize("amount", [200000, -150000, 0])
def test_opening_balance_and_payments(team, amount):
    post_entry(
        team["patient"].pk, team["reception"], {"kind": "opening", "amount_paise": amount}, str(uuid.uuid4())
    )
    payment = post_entry(
        team["patient"].pk, team["reception"], {"kind": "payment", "amount_paise": 500000}, str(uuid.uuid4())
    )
    assert balance(team["patient"]) == amount + 500000
    reverse_payment(payment.pk, team["admin"], "Incorrect payment", str(uuid.uuid4()))
    assert balance(team["patient"]) == amount
    with pytest.raises(ValidationError):
        reverse_payment(payment.pk, team["admin"], "Again", str(uuid.uuid4()))


@pytest.mark.parametrize("amount", [0, -1, 1.2, "500", True, 100_000_001])
def test_invalid_payment(team, amount):
    with pytest.raises(ValidationError):
        post_entry(
            team["patient"].pk,
            team["reception"],
            {"kind": "payment", "amount_paise": amount},
            str(uuid.uuid4()),
        )


def test_immutable_ledger(team):
    entry = post_entry(
        team["patient"].pk, team["admin"], {"kind": "payment", "amount_paise": 100}, "immutable"
    )
    with pytest.raises(DatabaseError), transaction.atomic():
        LedgerEntry.objects.filter(pk=entry.pk).update(amount_paise=200)
    with pytest.raises(DatabaseError), transaction.atomic():
        entry.delete()


@pytest.mark.parametrize("time,allowed", [("17:59:59", True), ("18:00:00", False), ("18:15:00", False)])
def test_receptionist_cutoff(team, time, allowed):
    with freeze_time("2026-10-28 " + time + "+05:30"):
        if allowed:
            editable(team["reception"], date(2026, 10, 28))
        else:
            with pytest.raises(PermissionDenied):
                editable(team["reception"], date(2026, 10, 28))
        editable(team["reception"], date(2026, 10, 29))
        editable(team["admin"], date(2025, 1, 1))


def test_last_slot(team, booking):
    with freeze_time("2026-10-28 17:59:00+05:30"):
        save_session(team["reception"], {**booking, "slot": 9})
    with freeze_time("2026-10-28 18:14:59+05:30"):
        assert reconcile() == 0
    with freeze_time("2026-10-28 18:15:00+05:30"):
        assert reconcile() == 1
    assert balance(team["patient"]) == -90000


@pytest.mark.parametrize(
    "role,day,allowed",
    [
        ("reception", "2026-08-01", True),
        ("reception", "2026-07-31", False),
        ("reception", "2027-01-01", True),
        ("one", "2026-09-01", True),
        ("one", "2026-08-31", False),
        ("admin", "2020-01-01", True),
    ],
)
@freeze_time("2026-10-28 12:00:00+05:30")
def test_calendar_history(team, role, day, allowed):
    if allowed:
        history_scope(team[role], date.fromisoformat(day))
    else:
        with pytest.raises(PermissionDenied):
            history_scope(team[role], date.fromisoformat(day))


@pytest.mark.parametrize(
    "path", ["patients/", "finance/", "frequency/", "staff/", "notifications/", "audit/"]
)
@freeze_time("2026-10-28 12:00:00+05:30")
def test_therapist_forbidden_apis(team, path):
    assert client_for(team["one"]).get("/api/" + path).status_code == 403
    assert api_client().get("/api/" + path).status_code == 403


def test_publication_ownership_expiry_and_payload(team, booking):
    team["patient"].special_fee = True
    team["patient"].save()
    with freeze_time("2026-10-28 09:00:00+05:30"):
        session = save_session(team["admin"], booking)
        c = client_for(team["one"])
        assert c.get("/api/schedule/?date=2026-10-28").status_code == 403
        publish(team["reception"], date(2026, 10, 28))
        result = c.get("/api/schedule/?date=2026-10-28")
        assert result.status_code == 200
        assert "special_fee" not in str(result.data)
        assert "balance" not in str(result.data)
        assert client_for(team["two"]).get(f"/api/sessions/{session.pk}/").status_code == 403
        assert client_for(team["two"]).get("/api/schedule/?date=2026-10-28").data["sessions"] == []
    with freeze_time("2026-10-29 09:59:59+05:30"):
        assert c.get("/api/schedule/?date=2026-10-28").status_code == 200
    with freeze_time("2026-10-29 10:00:00+05:30"):
        assert c.get("/api/schedule/?date=2026-10-28").status_code == 403


@freeze_time("2026-10-28 09:00:00+05:30")
def test_publication_change_recipients_and_noop(team, booking):
    session = save_session(team["admin"], booking)
    assert EmailOutbox.objects.count() == 0
    publish(team["reception"], date(2026, 10, 28))
    same = save_session(team["admin"], {**booking, "version": session.version}, session.pk)
    assert EmailOutbox.objects.count() == 0
    save_session(
        team["admin"],
        {**booking, "providers": [team["two"].provider.pk], "version": same.version},
        session.pk,
    )
    assert set(EmailOutbox.objects.values_list("recipient_id", flat=True)) == {team["one"].pk, team["two"].pk}


def test_reminder_recovery_and_resolution(team):
    with freeze_time("2026-10-28 09:00:00+05:30"):
        publish(team["reception"], date(2026, 10, 28))
    with freeze_time("2026-10-28 18:29:59+05:30"):
        publication_reminder()
        assert Notification.objects.count() == 0
    with freeze_time("2026-10-28 20:00:00+05:30"):
        publication_reminder()
        publication_reminder()
        assert Notification.objects.count() == 1
        publish(team["reception"], date(2026, 10, 29))
        assert Notification.objects.get().resolved


@freeze_time("2026-10-29 08:00:00+05:30")
def test_missed_evening_reminder_recovers_next_morning(team):
    publication_reminder()
    assert Notification.objects.get(kind="publication").date == date(2026, 10, 29)


@freeze_time("2026-10-28 12:00:00+05:30")
def test_frequency_and_dues(team, booking):
    save_session(team["admin"], booking)
    FrequencyPlan.objects.create(
        patient=team["patient"], weekly=3, monthly=14, effective_date=date(2026, 10, 1), actor=team["admin"]
    )
    data = client_for(team["reception"]).get("/api/frequency/?month=2026-10&week=2026-10-28").data
    row = next(p for p in data if p["id"] == team["patient"].pk)
    assert (row["actual_weekly"], row["actual_monthly"], row["weekly"], row["monthly"]) == (1, 1, 3, 14)
    post_entry(team["patient"].pk, team["reception"], {"kind": "payment", "amount_paise": 90000}, "settle")
    assert Notification.objects.get(kind="dues").resolved


@freeze_time("2026-10-28 09:00:00+05:30")
def test_idempotency_and_staff_boundaries(team, booking):
    client = client_for(team["reception"])
    key = str(uuid.uuid4())
    for _ in range(2):
        assert (
            client.post("/api/sessions/", booking, format="json", HTTP_IDEMPOTENCY_KEY=key).status_code == 200
        )
    assert Session.objects.count() == 1
    assert (
        client.post(
            "/api/sessions/", {**booking, "slot": 1}, format="json", HTTP_IDEMPOTENCY_KEY=key
        ).status_code
        == 409
    )
    assert client.get("/api/staff/").status_code == 403


def test_csrf_and_deactivation(team):
    client = api_client(enforce_csrf_checks=True)
    body = {"username": "one", "password": "Synthetic-only-Password-482!"}
    assert client.post("/api/auth/login/", body).status_code == 403
    token = client.get("/api/auth/csrf/").data["csrfToken"]
    assert client.post("/api/auth/login/", body, HTTP_X_CSRFTOKEN=token).status_code == 200
    assert client.get("/api/auth/me/").status_code == 200
    team["one"].is_active = False
    team["one"].save()
    assert client.get("/api/auth/me/").status_code == 403


@pytest.mark.django_db(transaction=True)
@freeze_time("2026-10-28 09:00:00+05:30")
def test_concurrent_conflicting_bookings(team, booking):
    barrier = Barrier(2)

    def worker(index):
        close_old_connections()
        user = User.objects.get(pk=team["admin"].pk)
        data = copy.deepcopy(booking)
        data["participants"] = [{"patient_id": team["patient" if index == 0 else "other"].pk}]
        barrier.wait(timeout=15)
        try:
            save_session(user, data)
            return "saved"
        except IntegrityError:
            return "conflict"
        finally:
            close_old_connections()

    with ThreadPoolExecutor(2) as executor:
        results = list(executor.map(worker, [0, 1]))
    assert sorted(results) == ["conflict", "saved"]
    assert Session.objects.count() == 1


def test_outbox_success_and_uncertain(team):
    from clinic.email_service import process_outbox

    EmailOutbox.objects.create(recipient=team["one"], event_key="test", next_attempt=timezone.now())
    with patch("clinic.email_service.send_email", return_value="gmail-id") as send:
        assert process_outbox() == 1
        assert process_outbox() == 0
        assert send.call_count == 1
    second = EmailOutbox.objects.create(
        recipient=team["one"], event_key="uncertain", next_attempt=timezone.now()
    )
    with patch("clinic.email_service.send_email", side_effect=TimeoutError):
        assert process_outbox() == 0
    second.refresh_from_db()
    assert second.state == "uncertain"


@override_settings(MAINTENANCE_SECRET="synthetic-maintenance-secret")
def test_protected_maintenance():
    client = api_client()
    assert client.post("/api/maintenance/").status_code == 403
    assert (
        client.post("/api/maintenance/", HTTP_AUTHORIZATION="Bearer synthetic-maintenance-secret").status_code
        == 200
    )

import pytest
from accounts.models import User, Provider
from clinic.models import Patient, Therapy


@pytest.fixture(autouse=True)
def synthetic_password_hashing(settings):
    # Only synthetic test users use this hasher; runtime settings remain secure.
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def team(db):
    users = {}
    for index, role in enumerate(["ADMIN", "RECEPTIONIST", "THERAPIST", "THERAPIST"]):
        key = ["admin", "reception", "one", "two"][index]
        user = User.objects.create_user(
            username=key,
            email=f"{key}@example.test",
            password="Synthetic-only-Password-482!",
            role=role,
            full_name="Synthetic " + key,
            pending_activation=False,
        )
        if role != "RECEPTIONIST":
            Provider.objects.create(user=user, display_name="Provider " + key, display_order=index)
        users[key] = user
    users["patient"] = Patient.objects.create(name="Synthetic Child Alpha")
    users["other"] = Patient.objects.create(name="Synthetic Child Beta")
    # TransactionTestCase flush does not rerun data migrations.
    for order, (code, fee) in enumerate(
        [
            ("OT", 90000),
            ("SP_EDU", 90000),
            ("ABA", 90000),
            ("GROUP", 90000),
            ("ASSESS_2000", 200000),
            ("ASSESS_2500", 250000),
            ("HOME_PLAN", 450000),
        ]
    ):
        Therapy.objects.get_or_create(
            code=code, defaults={"name": code, "fee_paise": fee, "group": code == "GROUP", "order": order}
        )
    return users


@pytest.fixture
def booking(team):
    return {
        "date": "2026-10-28",
        "slot": 0,
        "therapy": "OT",
        "providers": [team["one"].provider.pk],
        "participants": [{"patient_id": team["patient"].pk, "status": "Scheduled"}],
    }

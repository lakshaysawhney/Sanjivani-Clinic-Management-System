"""Exercise the history backfill against the actual legacy PostgreSQL schema."""

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from freezegun import freeze_time

from clinic.models import Participation, LedgerEntry
from clinic.time_rules import slot_end
from datetime import date


@pytest.mark.django_db(transaction=True)
@freeze_time("2026-10-28 12:00:00+05:30")
def test_history_migration_preserves_legacy_rows_and_ledger(team):
    executor = MigrationExecutor(connection)
    executor.migrate([("clinic", "0002_catalog_and_ledger_guards")])
    try:
        old = executor.loader.project_state([("clinic", "0002_catalog_and_ledger_guards")]).apps
        schedule = old.get_model("clinic", "DailySchedule").objects.create(date=date(2026, 10, 28))
        session = old.get_model("clinic", "Session").objects.create(
            schedule=schedule,
            slot=0,
            therapy_id="OT",
            ends_at=slot_end(schedule.date, 0),
            created_by_id=team["admin"].pk,
        )
        old.get_model("clinic", "Assignment").objects.create(
            session=session, provider_id=team["one"].provider.pk
        )
        legacy = old.get_model("clinic", "Participation")
        cancelled = legacy.objects.create(session=session, patient_id=team["patient"].pk, status="Cancelled")
        completed = legacy.objects.create(session=session, patient_id=team["other"].pk, status="Completed")
        entry = LedgerEntry.objects.create(
            patient=team["other"],
            participation_id=completed.pk,
            kind="charge",
            amount_paise=-90000,
            source="legacy-charge",
            description="OT",
            effective_at=session.ends_at,
        )
        original = LedgerEntry.objects.values().get(pk=entry.pk)
    finally:
        MigrationExecutor(connection).migrate([("clinic", "0003_participation_history")])
    part = Participation.objects.get(pk=cancelled.pk)
    assert part.removed is True
    assert part.attendance_date == schedule.date
    assert part.cancelled_context["providers"] == [team["one"].provider.pk]
    assert part.cancelled_context["therapy"] == "OT"
    assert Participation.objects.get(pk=completed.pk).removed is False
    assert LedgerEntry.objects.values().get(pk=entry.pk) == original

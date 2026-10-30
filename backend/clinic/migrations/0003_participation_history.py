from django.db import migrations, models


def preserve_existing_context(apps, schema_editor):
    """Freeze the best available legacy context without rewriting immutable records.

    Earlier edits may already have lost cancellation context. This migration
    cannot invent that history; it preserves the stored shell at migration time.
    Ordinary replacements with a live child can safely retire cancelled siblings.
    """
    Participation = apps.get_model("clinic", "Participation")
    for part in (
        Participation.objects.using(schema_editor.connection.alias)
        .select_related("session__schedule", "session__therapy")
        .iterator()
    ):
        session = part.session
        part.attendance_date = session.schedule.date
        if part.status == "Cancelled":
            part.cancelled_context = {
                "date": str(session.schedule.date),
                "slot": session.slot,
                "therapy": session.therapy_id,
                "therapy_name": session.therapy.name,
                "providers": list(session.assignments.values_list("provider_id", flat=True)),
                "ends_at": session.ends_at.isoformat(),
            }
            part.removed = (
                not session.therapy.group and session.participations.exclude(status="Cancelled").exists()
            )
        part.save(update_fields=["attendance_date", "cancelled_context", "removed"])


class Migration(migrations.Migration):
    dependencies = [("clinic", "0002_catalog_and_ledger_guards")]
    operations = [
        migrations.AddField(
            model_name="participation", name="removed", field=models.BooleanField(default=False)
        ),
        migrations.AddField(
            model_name="participation", name="cancelled_context", field=models.JSONField(null=True)
        ),
        migrations.AddField(
            model_name="participation",
            name="attendance_date",
            field=models.DateField(null=True, db_index=True),
        ),
        migrations.RunPython(preserve_existing_context, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="participation", name="attendance_date", field=models.DateField(db_index=True)
        ),
        migrations.AddConstraint(
            model_name="participation",
            constraint=models.CheckConstraint(
                condition=models.Q(removed=False) | models.Q(status="Cancelled"),
                name="removed_participation_cancelled",
            ),
        ),
    ]

from django.db import migrations


def catalog(apps, schema_editor):
    Therapy = apps.get_model("clinic", "Therapy")
    rows = [
        ("OT", "OT", 90000, False),
        ("SP_EDU", "Sp. Edu.", 90000, False),
        ("ABA", "ABA", 90000, False),
        ("GROUP", "Group Therapy", 90000, True),
        ("ASSESS_2000", "Assessment (2000)", 200000, False),
        ("ASSESS_2500", "Assessment (2500)", 250000, False),
        ("HOME_PLAN", "Assessment + Home Plan", 450000, False),
    ]
    for order, (code, name, fee, group) in enumerate(rows):
        Therapy.objects.get_or_create(
            code=code, defaults={"name": name, "fee_paise": fee, "group": group, "order": order}
        )


class Migration(migrations.Migration):
    dependencies = [("clinic", "0001_initial")]
    operations = [
        migrations.RunPython(catalog, migrations.RunPython.noop),
        migrations.RunSQL(
            """
CREATE FUNCTION clinic_immutable_record() RETURNS trigger AS $$
BEGIN RAISE EXCEPTION 'Historical ledger and audit records are immutable'; END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER immutable_ledger BEFORE UPDATE OR DELETE ON clinic_ledgerentry FOR EACH ROW EXECUTE FUNCTION clinic_immutable_record();
CREATE TRIGGER immutable_audit BEFORE UPDATE OR DELETE ON clinic_auditlog FOR EACH ROW EXECUTE FUNCTION clinic_immutable_record();
""",
            """DROP TRIGGER immutable_ledger ON clinic_ledgerentry; DROP TRIGGER immutable_audit ON clinic_auditlog; DROP FUNCTION clinic_immutable_record();""",
        ),
    ]

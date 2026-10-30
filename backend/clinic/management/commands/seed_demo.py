import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from accounts.models import User, Provider
from clinic.models import Patient, FrequencyPlan
from clinic.time_rules import now


class Command(BaseCommand):
    help = "Create synthetic local browser-test data. Requires DEBUG and E2E_PASSWORD."

    def handle(self, *args, **options):
        password = os.environ.get("E2E_PASSWORD")
        if not settings.DEBUG or not password:
            raise CommandError("Demo data requires DEBUG=1 and E2E_PASSWORD.")
        users = []
        for index in range(12):
            role = "ADMIN" if index == 0 else "RECEPTIONIST" if index == 1 else "THERAPIST"
            username = (
                "demo_admin"
                if index == 0
                else "demo_reception"
                if index == 1
                else f"demo_therapist{index - 1}"
            )
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": username + "@example.test",
                    "full_name": f"Synthetic Staff {index + 1:02}",
                    "role": role,
                },
            )
            user.set_password(password)
            user.pending_activation = False
            user.is_active = True
            user.save()
            users.append(user)
            if role != "RECEPTIONIST":
                Provider.objects.get_or_create(
                    user=user, defaults={"display_name": f"Provider {index + 1:02}", "display_order": index}
                )
        for index in range(20):
            patient, _ = Patient.objects.get_or_create(
                name=f"Synthetic Child {index + 1:02}", defaults={"special_fee": index % 5 == 0}
            )
            if not patient.plans.exists():
                FrequencyPlan.objects.create(
                    patient=patient,
                    weekly=3,
                    monthly=14,
                    effective_date=now().date().replace(day=1),
                    actor=users[0],
                )
        self.stdout.write("Synthetic accounts and patients ready. No credentials printed.")

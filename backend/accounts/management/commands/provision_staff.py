import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from accounts.models import User, Provider


class Command(BaseCommand):
    help = "Provision pending accounts from a private JSON roster. Never logs the roster."

    def add_arguments(self, parser):
        parser.add_argument("file")

    @transaction.atomic
    def handle(self, *args, **options):
        rows = json.loads(Path(options["file"]).read_text(encoding="utf-8"))
        for row in rows:
            if row["role"] not in User.Role.values:
                raise CommandError("Invalid role in private roster.")
            email = row["email"].lower()
            user = User.objects.filter(email__iexact=email).first()
            if user is None:
                username = row["username"]
                suffix = 1
                while User.objects.filter(username=username).exists():
                    suffix += 1
                    username = row["username"] + str(suffix)
                user = User(
                    username=username,
                    email=email,
                    full_name=row["full_name"],
                    role=row["role"],
                    pending_activation=True,
                )
                user.set_unusable_password()
                user.save()
            elif user.role != row["role"]:
                raise CommandError("Existing account role mismatch. Review before updating.")
            if row["role"] != "RECEPTIONIST":
                Provider.objects.update_or_create(
                    user=user,
                    defaults={
                        "display_name": row.get("display_name", row["full_name"]),
                        "display_order": row.get("display_order", 100),
                        "specialization": row.get("specialization", ""),
                    },
                )
        self.stdout.write(
            "Provisioning complete. Existing passwords were preserved; new accounts require activation."
        )

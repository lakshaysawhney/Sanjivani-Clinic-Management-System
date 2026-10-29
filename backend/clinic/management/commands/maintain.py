from django.core.management.base import BaseCommand
from clinic.scheduling import reconcile, publication_reminder
from clinic.email_service import process_outbox


class Command(BaseCommand):
    help = "Run bounded business maintenance explicitly."

    def handle(self, *args, **options):
        count = reconcile()
        publication_reminder()
        sent = process_outbox()
        self.stdout.write(f"Completed {count} sessions; sent {sent} messages.")

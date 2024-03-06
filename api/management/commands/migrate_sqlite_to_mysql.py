from django.core.management.base import BaseCommand
from api.models import Joke
from django.db import transaction
import traceback


class Command(BaseCommand):
    help = "Migrates data from SQLite to MySQL"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("Starting migration from SQLite to MySQL...")
        )

        try:
            with transaction.atomic(using="mysql"):
                objlist = Joke.objects.using("sqlite").all()
                for obj in objlist:
                    obj.pk = None  # Reset primary key to avoid conflicts
                    obj.save(using="mysql")
                    self.stdout.write(self.style.SUCCESS(f"Saved: {obj}"))

                self.stdout.write(
                    self.style.SUCCESS("Successfully migrated data to MySQL.")
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred: {e}"))
            traceback.print_exc()

from django.core.management.base import BaseCommand
from api.models import Joke, OffenseTrait


class Command(BaseCommand):
    help = "Migrates joke traits to offense_trait table"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting joke traits migration..."))
        all_jokes = Joke.objects.all()
        # iterate over all jokes create a trait from the joke's offense_type and offense_degree
        # and save the joke's trait
        for joke in all_jokes:
            trait, created = OffenseTrait.objects.get_or_create(
                name=joke.offense_type, degree=joke.offense_degree
            )
            joke.trait = trait
            joke.save()
            self.stdout.write(self.style.SUCCESS(f"Saved: {joke}"))

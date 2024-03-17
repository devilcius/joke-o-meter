from django.core.management.base import BaseCommand
from faker import Faker
import random
from api.models import (
    OffenseTrait,
    Joke,
    EvaluationSession,
    JokeEvaluation,
    JokometianRanking,
)

NUMBER_OF_JOKES = 150


class Command(BaseCommand):
    help = "Populates the database with fake data for testing purposes."

    def handle(self, *args, **options):
        faker = Faker()

        # Ensure OffenseTraits exist
        for trait, _ in OffenseTrait.OFFENSE_TYPE_CHOICES:
            OffenseTrait.objects.get_or_create(
                name=trait, defaults={"degree": random.randint(1, 10)}
            )

        # Fetch saved OffenseTraits
        offense_traits = list(OffenseTrait.objects.all())

        # Populate Jokes
        jokes = []
        for _ in range(NUMBER_OF_JOKES):
            joke = Joke(
                content=faker.text(max_nb_chars=200),
                trait=random.choice(offense_traits),  # Use saved traits
                language=random.choice(["en", "es"]),
            )
            jokes.append(joke)
        Joke.objects.bulk_create(jokes)

        # Populate EvaluationSessions
        sessions = [EvaluationSession() for _ in range(10)]
        EvaluationSession.objects.bulk_create(sessions)

        # Populate JokeEvaluations
        evaluations = []
        for session in sessions:
            # Ensure to fetch Jokes from db
            for joke in random.sample(list(Joke.objects.all()), 10):
                evaluations.append(
                    JokeEvaluation(
                        session=session,
                        joke=joke,
                        liked=faker.boolean(chance_of_getting_true=50),
                    )
                )
        JokeEvaluation.objects.bulk_create(evaluations)

        # No need to populate JokometianRanking

        self.stdout.write(
            self.style.SUCCESS("Database successfully populated with fake data.")
        )

from django.test import TestCase
from api.models import (
    Joke,
    OffenseTrait,
    JokeEvaluation,
    EvaluationSession,
    JokometianRanking,
)
from api.jokometian_utils import (
    create_jokometian_from_jokes_evaluation,
    update_jokometian_ranking,
)
from django.conf import settings
from django.test import override_settings


@override_settings(LANGUAGE_CODE="en-us")
class CreateJokometianFromJokesEvaluationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create offense traits
        cls.race_trait = OffenseTrait.objects.create(name=OffenseTrait.RACE, degree=10)
        cls.gender_trait = OffenseTrait.objects.create(
            name=OffenseTrait.GENDER, degree=8
        )
        cls.no_offense_trait = OffenseTrait.objects.create(
            name=OffenseTrait.NO_OFFENSE_FOUND, degree=0
        )

        # Create jokes linked to traits
        cls.joke_with_race = Joke.objects.create(
            content="Race joke", trait=cls.race_trait
        )
        cls.joke_with_gender = Joke.objects.create(
            content="Gender joke", trait=cls.gender_trait
        )
        cls.joke_with_no_offense = Joke.objects.create(
            content="No offense joke", trait=cls.no_offense_trait
        )

        # Create an evaluation session
        cls.session = EvaluationSession.objects.create()

    def test_with_mixed_liked_jokes(self):
        # Create liked evaluations for different traits
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=True
        )
        evaluations = JokeEvaluation.objects.all()

        jokometian = create_jokometian_from_jokes_evaluation(evaluations)

        # Assert that Jokometian's name and description consider the dominant trait (Race in this case)
        self.assertEqual(jokometian.name, OffenseTrait.RACE)
        self.assertIn("Born from the flames of challenge", jokometian.description)
        self.assertEqual(
            jokometian.image_url,
            settings.STATIC_URL + "images/jokometians/image_race.svg",
        )

    def test_no_offense_found_alone(self):
        # Create an evaluation that likes a joke with no offense only
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_no_offense, liked=True
        )
        evaluations = JokeEvaluation.objects.all()

        jokometian = create_jokometian_from_jokes_evaluation(evaluations)

        # Assert that Jokometian considers the NO_OFFENSE_FOUND trait when it's the only one liked
        self.assertEqual(jokometian.name, OffenseTrait.NO_OFFENSE_FOUND)
        self.assertIn("An untainted soul", jokometian.description)
        self.assertEqual(
            jokometian.image_url,
            settings.STATIC_URL + "images/jokometians/image_pure.svg",
        )

    def test_jokometian_traits(self):
        # Create liked evaluations for different traits
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_no_offense, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
        )

        # Check Jokomenain.traits is a list of 3 traits
        evaluations = JokeEvaluation.objects.all()
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        # Only 2 traits sin no offense trait is removed
        self.assertEqual(len(jokometian.traits), 2)

        # Test they are sorted by degree desc
        self.assertEqual(jokometian.traits[0].name, self.race_trait.name)
        self.assertEqual(jokometian.traits[1].name, self.gender_trait.name)

    def test_no_liked_jokes(self):
        # Case where there are no liked jokes
        evaluations = JokeEvaluation.objects.all()

        jokometian = create_jokometian_from_jokes_evaluation(evaluations)

        # Assert default Jokometian properties when no jokes are liked
        self.assertEqual(jokometian.name, "Jokometian")
        self.assertEqual(
            jokometian.description,
            "An enigmatic Jokometian with a unique blend of traits.",
        )
        self.assertEqual(
            jokometian.image_url, settings.STATIC_URL + "images/jokometians/default.svg"
        )

    def test_create_new_jokometian_ranking(self):
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=True
        )
        evaluations = JokeEvaluation.objects.all()

        # Expected score is the sum of degrees from the liked traits
        expected_score = self.race_trait.degree + self.gender_trait.degree
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        # Call the function under test
        update_jokometian_ranking(evaluations)

        # Verify a new JokometianRanking was created with expected properties
        self.assertEqual(JokometianRanking.objects.count(), 1)
        ranking = JokometianRanking.objects.first()
        self.assertIsNotNone(ranking)
        self.assertEqual(ranking.score, expected_score)
        self.assertEqual(ranking.image_url, jokometian.image_url)

    def test_update_existing_jokometian_ranking(self):
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=True
        )
        evaluations = JokeEvaluation.objects.all()
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        # Create an initial JokometianRanking that should be updated
        initial_ranking = JokometianRanking.objects.create(
            name=jokometian.name, score=50, image_url="initial_image_url.png"
        )

        # Set up evaluations leading to an update of this ranking
        evaluations = JokeEvaluation.objects.all()

        # Call the function under test
        update_jokometian_ranking(evaluations)
        updated_score = (
            initial_ranking.score + self.race_trait.degree + self.gender_trait.degree
        )
        # Refresh the ranking from the database and verify updates
        initial_ranking.refresh_from_db()
        self.assertEqual(JokometianRanking.objects.count(), 1)
        self.assertEqual(initial_ranking.score, updated_score)
        self.assertEqual(
            initial_ranking.image_url, "/static/images/jokometians/image_race.svg"
        )

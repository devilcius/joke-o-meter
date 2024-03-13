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
        cls.joke_with_disability = Joke.objects.create(
            content="Disability joke", trait=cls.no_offense_trait
        )

        # Create an evaluation session
        cls.session = EvaluationSession.objects.create()

    def test_with_mixed_jokes(self):
        # Create liked and not liked evaluations for different traits
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=False
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_no_offense, liked=True
        )
        evaluations = JokeEvaluation.objects.all()

        jokometian = create_jokometian_from_jokes_evaluation(evaluations)

        # Assert that Jokometian's name and description consider the dominant trait (Race in this case)
        self.assertEqual(jokometian.key_name, OffenseTrait.RACE)
        self.assertIn("Born from the flames of challenge", jokometian.description)
        self.assertEqual(
            jokometian.image_url,
            settings.STATIC_URL + "images/jokometians/image_race.svg",
        )

    def test_no_offense_found_alone(self):
        # Create an evaluation that the only jokes liked are NO_OFFENSE_FOUND
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_no_offense, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_disability, liked=False
        )
        evaluations = JokeEvaluation.objects.all()

        jokometian = create_jokometian_from_jokes_evaluation(evaluations)

        # Assert that Jokometian considers the NO_OFFENSE_FOUND trait when it's the only one liked
        self.assertEqual(jokometian.key_name, OffenseTrait.NO_OFFENSE_FOUND)
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
            session=self.session, joke=self.joke_with_race, liked=False
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
        # Only 2 traits since no offense trait is removed
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
            session=self.session, joke=self.joke_with_race, liked=False
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
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
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=False
        )
        evaluations = JokeEvaluation.objects.all()
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        # Create an initial JokometianRanking that should be updated
        initial_ranking = JokometianRanking.objects.create(
            name=jokometian.key_name, score=50, image_url="initial_image_url.png"
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
            initial_ranking.image_url, "/assets/images/jokometians/image_race.svg"
        )

    def test_jokometian_includes_liked_jokes_only(self):
        # Create evaluations, mixing liked and not liked
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_race, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_gender, liked=False
        )  # Not liked
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_no_offense, liked=True
        )
        JokeEvaluation.objects.create(
            session=self.session, joke=self.joke_with_disability, liked=True
        )

        # Fetch all evaluations for the session
        evaluations = JokeEvaluation.objects.filter(session=self.session)

        # Generate the Jokometian
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)

        # Assert that Jokometian includes only the liked jokes
        self.assertIn(self.joke_with_race, jokometian.jokes)
        # This joke was not liked
        self.assertNotIn(self.joke_with_gender, jokometian.jokes)
        # Since jokes with NO_OFFENSE_FOUND trait are not included in the dominant traits
        # when another offense trait is liked, this joke is not included
        self.assertNotIn(self.joke_with_no_offense, jokometian.jokes)

        # Additionally, check the length of the jokes list matches the number of liked jokes
        self.assertEqual(len(jokometian.jokes), 1)

    def test_no_jokes_liked(self):
        # Case where there are no liked jokes
        for i in range(5):
            JokeEvaluation.objects.create(
                session=self.session, joke=self.joke_with_disability, liked=False
            )
        evaluations = JokeEvaluation.objects.all()
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        self.assertEqual(jokometian.key_name, "GRUMPY")
        self.assertEqual(
            jokometian.image_url,
            settings.STATIC_URL + "images/jokometians/image_grumpy.svg",
        )

    def test_all_jokes_liked(self):
        # Case where all jokes are liked
        # array of 5 trait names
        trait_names = [
            OffenseTrait.RELIGION,
            OffenseTrait.ETHNICITY,
            OffenseTrait.NO_OFFENSE_FOUND,
            OffenseTrait.DISABILITY,
            OffenseTrait.GENERIC_VIOLENCE,
        ]

        for i in range(5):
            trait = OffenseTrait.objects.create(name=trait_names[i], degree=i)
            joke = Joke.objects.create(
                content=f"Joke {i}",
                trait=trait,
                language="en",
            )
            JokeEvaluation.objects.create(session=self.session, joke=joke, liked=True)
        evaluations = JokeEvaluation.objects.all()
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        self.assertEqual(jokometian.key_name, "GIGGLY")
        self.assertEqual(
            jokometian.image_url,
            settings.STATIC_URL + "images/jokometians/image_giggly.svg",
        )

    def test_all_jokes_liked_no_favorite_jokes(self):
        trait_names = [
            OffenseTrait.RELIGION,
            OffenseTrait.ETHNICITY,
            OffenseTrait.NO_OFFENSE_FOUND,
            OffenseTrait.DISABILITY,
            OffenseTrait.GENERIC_VIOLENCE,
            OffenseTrait.RACE,
        ]

        for i in range(len(trait_names)):
            trait = OffenseTrait.objects.create(name=trait_names[i], degree=i)
            joke = Joke.objects.create(
                content=f"Joke {i}",
                trait=trait,
                language="en",
            )
            if trait.name == OffenseTrait.NO_OFFENSE_FOUND:
                JokeEvaluation.objects.create(
                    session=self.session, joke=joke, liked=False
                )
            else:
                JokeEvaluation.objects.create(
                    session=self.session, joke=joke, liked=True
                )

        evaluations = JokeEvaluation.objects.all()
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        self.assertEqual(jokometian.key_name, "DIABOLICAL")

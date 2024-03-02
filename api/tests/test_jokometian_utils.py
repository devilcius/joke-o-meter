from django.test import TestCase
from api.models import Jokometian, Joke, JokeEvaluation, EvaluationSession
from api.jokometian_utils import generate_jokometian_name, generate_jokometian_description, generate_jokometian_image, determine_offense_rates_for_evaluation


class JokometianUtilsTest(TestCase):

    def test_generate_jokometian_name(self):
        # Test for "Fire Jokometian" name
        jokometian_fire = Jokometian(race_rate=51)
        self.assertEqual(generate_jokometian_name(
            jokometian_fire), "Fiery Jokometian")

        # Test for "Pure Soul Jokometian" name (default case)
        jokometian_pure = Jokometian()
        self.assertEqual(generate_jokometian_name(
            jokometian_pure), "Pure Soul Jokometian")

        # Add more scenarios for other traits...

    def test_generate_jokometian_description(self):
        # Test specific descriptions based on offense rates
        jokometian_fire = Jokometian(race_rate=51)
        self.assertIn("flames of challenge",
                      generate_jokometian_description(jokometian_fire))

        # Test the default description
        jokometian_pure = Jokometian()
        self.assertIn("untainted soul",
                      generate_jokometian_description(jokometian_pure))

        # Add more scenarios for other traits...

    def test_generate_jokometian_image(self):
        # Test image selection based on offense rates
        jokometian_fire = Jokometian(race_rate=51)
        self.assertTrue(
            "image_race.svg" in generate_jokometian_image(jokometian_fire))

        # Test the default image (no offense)
        jokometian_pure = Jokometian()
        self.assertTrue(
            "image_pure.svg" in generate_jokometian_image(jokometian_pure))


class DetermineOffenseRatesForEvaluationTests(TestCase):

    def setUp(self):
        # Create some jokes with different offense types
        self.joke_race = Joke.objects.create(
            content="Race joke", offense_type="RACE")
        self.joke_gender = Joke.objects.create(
            content="Gender joke", offense_type="GENDER")
        # Assuming EvaluationSession model exists and is required
        self.session = EvaluationSession.objects.create()

    def test_all_liked_jokes_same_type(self):
        """All liked jokes are of the same offense type."""
        evaluations = [
            JokeEvaluation(session=self.session,
                           joke=self.joke_race, liked=True),
            JokeEvaluation(session=self.session,
                           joke=self.joke_race, liked=True)
        ]
        offense_rates = determine_offense_rates_for_evaluation(evaluations)
        self.assertEqual(offense_rates['race_rate'], 100)
        self.assertEqual(offense_rates['gender_rate'], 0)

    def test_mixed_liked_jokes_different_types(self):
        """Liked jokes are evenly split between two offense types."""
        evaluations = [
            JokeEvaluation(session=self.session,
                           joke=self.joke_race, liked=True),
            JokeEvaluation(session=self.session,
                           joke=self.joke_gender, liked=True)
        ]
        offense_rates = determine_offense_rates_for_evaluation(evaluations)
        self.assertEqual(offense_rates['race_rate'], 50)
        self.assertEqual(offense_rates['gender_rate'], 50)

    def test_no_liked_jokes(self):
        """No jokes are liked, resulting in a default no offense rate."""
        evaluations = [
            JokeEvaluation(session=self.session,
                           joke=self.joke_race, liked=False),
            JokeEvaluation(session=self.session,
                           joke=self.joke_gender, liked=False)
        ]
        offense_rates = determine_offense_rates_for_evaluation(evaluations)
        self.assertEqual(offense_rates['no_offense_rate'], 100)

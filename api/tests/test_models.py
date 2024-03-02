from api.models import Jokometian, Joke, JokeEvaluation, EvaluationSession
from django.test import TestCase
from django.test import TestCase
from unittest.mock import patch


class JokeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Joke.objects.create(content="Why did the chicken cross the road?",
                            offense_degree=5, offense_type=Joke.RACE, language="English")

    def test_content_label(self):
        joke = Joke.objects.get(id=1)
        field_label = joke._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_offense_degree_label(self):
        joke = Joke.objects.get(id=1)
        field_label = joke._meta.get_field('offense_degree').verbose_name
        self.assertEquals(field_label, 'offense degree')

    def test_offense_type_label(self):
        joke = Joke.objects.get(id=1)
        field_label = joke._meta.get_field('offense_type').verbose_name
        self.assertEquals(field_label, 'offense type')

    def test_object_name_is_content(self):
        joke = Joke.objects.get(id=1)
        expected_object_name = joke.content
        self.assertEquals(expected_object_name, str(joke.content))

    def test_language_label(self):
        joke = Joke.objects.get(id=1)
        field_label = joke._meta.get_field('language').verbose_name
        self.assertEquals(field_label, 'language')

    def test_language_default_value(self):
        joke = Joke.objects.get(id=1)
        self.assertEquals(joke.language, "English")


class JokometianModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a Jokometian instance for use in tests
        cls.jokometian = Jokometian.objects.create(
            uuid="123e4567-e89b-12d3-a456-426614174000",
        )

    def test_uuid_label(self):
        jokometian = Jokometian.objects.get(id=1)
        field_label = jokometian._meta.get_field('uuid').verbose_name
        self.assertEquals(field_label, 'uuid')

    def test_offense_rates_defaults(self):
        # Test the default values for offense rates
        self.assertEqual(self.jokometian.race_rate, 0)
        self.assertEqual(self.jokometian.religion_rate, 0)
        self.assertEqual(self.jokometian.ethnicity_rate, 0)
        self.assertEqual(self.jokometian.gender_rate, 0)
        self.assertEqual(self.jokometian.sexual_orientation_rate, 0)
        self.assertEqual(self.jokometian.disability_rate, 0)
        self.assertEqual(self.jokometian.violence_rate, 0)
        self.assertEqual(self.jokometian.no_offense_rate, 0)

    @patch('api.models.generate_jokometian_name')
    @patch('api.models.generate_jokometian_description')
    def test_jokometian_name_and_description_properties(self, mock_generate_description, mock_generate_name):
        # Setup mock return values
        mock_generate_name.return_value = "Test Name"
        mock_generate_description.return_value = "Test Description"

        # Create a Jokometian instance (no need to save to DB for this test)
        jokometian = Jokometian()

        # Test the name property
        self.assertEqual(jokometian.name, "Test Name")
        mock_generate_name.assert_called_once_with(jokometian)

        # Test the description property
        self.assertEqual(jokometian.description, "Test Description")
        mock_generate_description.assert_called_once_with(jokometian)


class JokesEvaluationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create an EvaluationSession instance
        session = EvaluationSession.objects.create()
        joke = Joke.objects.create(
            content="Why did the chicken cross the road?", offense_degree=5, offense_type=Joke.RACE, language="English")
        JokeEvaluation.objects.create(joke=joke, liked=True, session=session)

    def test_joke_label(self):
        evaluation = JokeEvaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field('joke').verbose_name
        self.assertEquals(field_label, 'joke')

    def test_liked_label(self):
        evaluation = JokeEvaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field('liked').verbose_name
        self.assertEquals(field_label, 'liked')

    # Add a test for the session field if you've introduced an EvaluationSession model
    def test_session_label(self):
        evaluation = JokeEvaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field('session').verbose_name
        self.assertEquals(field_label, 'session')

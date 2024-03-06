from api.models import Joke, JokeEvaluation, EvaluationSession, OffenseTrait
from django.test import TestCase
from django.test import TestCase


class JokeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a sample offense trait for use in tests
        cls.sample_trait = OffenseTrait.objects.create(name=OffenseTrait.RACE, degree=5)

    def test_create_joke_without_trait(self):
        """
        Test the creation of a Joke instance without specifying an offense trait.
        """
        joke = Joke.objects.create(
            content="Why did the chicken cross the road?", language="English"
        )
        self.assertEqual(joke.content, "Why did the chicken cross the road?")
        self.assertIsNone(joke.trait)
        self.assertEqual(joke.language, "English")

    def test_create_joke_with_trait(self):
        """
        Test the creation of a Joke instance with a specified offense trait.
        """
        joke = Joke.objects.create(
            content="Just a random joke.", trait=self.sample_trait, language="Spanish"
        )
        self.assertEqual(joke.content, "Just a random joke.")
        self.assertEqual(joke.trait, self.sample_trait)
        self.assertEqual(joke.language, "Spanish")

    def test_joke_default_language(self):
        """
        Test that the default language of a Joke instance is "Spanish".
        """
        joke = Joke.objects.create(content="Another random joke.")
        self.assertEqual(joke.language, "Spanish")

    def test_joke_string_representation(self):
        """
        Test the string representation of a Joke instance.
        """
        joke_content = "Why did the chicken cross the road? To get to the other side!"
        joke = Joke.objects.create(content=joke_content, language="English")
        self.assertEqual(str(joke.content), joke_content)


class JokesEvaluationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create an EvaluationSession instance
        session = EvaluationSession.objects.create()
        offense_trait = OffenseTrait.objects.create(name=OffenseTrait.RACE, degree=10)

        joke = Joke.objects.create(
            content="Why did the chicken cross the road?",
            trait=offense_trait,
            language="English",
        )
        JokeEvaluation.objects.create(joke=joke, liked=True, session=session)

    def test_joke_label(self):
        evaluation = JokeEvaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field("joke").verbose_name
        self.assertEquals(field_label, "joke")

    def test_liked_label(self):
        evaluation = JokeEvaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field("liked").verbose_name
        self.assertEquals(field_label, "liked")

    # Add a test for the session field if you've introduced an EvaluationSession model
    def test_session_label(self):
        evaluation = JokeEvaluation.objects.get(id=1)
        field_label = evaluation._meta.get_field("session").verbose_name
        self.assertEquals(field_label, "session")

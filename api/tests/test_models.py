from api.models import (
    Joke,
    JokeEvaluation,
    EvaluationSession,
    OffenseTrait,
    JokometianRanking,
)
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


class JokometianRankingModelTest(TestCase):

    def test_create_jokometian_ranking(self):
        # Test creating a new JokometianRanking instance
        ranking = JokometianRanking.objects.create(
            name="Jokometian One", score=100, image_url="image_one_url.png"
        )

        # Verify the instance was created as expected
        self.assertEqual(JokometianRanking.objects.count(), 1)
        self.assertEqual(ranking.name, "Jokometian One")
        self.assertEqual(ranking.score, 100)
        self.assertEqual(ranking.image_url, "image_one_url.png")

    def test_update_jokometian_ranking(self):
        # Create and then update a JokometianRanking instance
        ranking = JokometianRanking.objects.create(
            name="Jokometian Two", score=50, image_url="image_two_url.png"
        )
        JokometianRanking.objects.filter(name="Jokometian Two").update(score=150)

        # Fetch the updated instance and verify the update took place
        updated_ranking = JokometianRanking.objects.get(name="Jokometian Two")
        self.assertEqual(updated_ranking.score, 150)

    def test_ordering_by_score(self):
        # Create multiple JokometianRanking instances with different scores
        JokometianRanking.objects.create(
            name="Low Score", score=10, image_url="low_score_url.png"
        )
        JokometianRanking.objects.create(
            name="High Score", score=200, image_url="high_score_url.png"
        )
        JokometianRanking.objects.create(
            name="Medium Score", score=100, image_url="medium_score_url.png"
        )

        # Fetch all instances and verify they are ordered by score descending
        rankings = JokometianRanking.objects.all()
        self.assertEqual(rankings[0].name, "High Score")
        self.assertEqual(rankings[1].name, "Medium Score")
        self.assertEqual(rankings[2].name, "Low Score")

    def test_unique_name_constraint(self):
        # Verify that attempting to create a JokometianRanking with a duplicate name raises an error
        JokometianRanking.objects.create(
            name="Unique Name", score=123, image_url="unique_name_url.png"
        )

        # Adjust the exception type based on your database backend
        with self.assertRaises(Exception):
            JokometianRanking.objects.create(
                name="Unique Name", score=456, image_url="another_unique_name_url.png"
            )

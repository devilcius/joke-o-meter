from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Joke, JokeEvaluation, EvaluationSession, OffenseTrait
import uuid


class JokeListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.session = EvaluationSession.objects.create()
        # Create 30 jokes in Spanish: 17 with NO_OFFENSE_FOUND and the rest with
        # each of the other offense types
        for i in range(17):
            offense_trait = OffenseTrait.objects.create(
                name=OffenseTrait.NO_OFFENSE_FOUND, degree=i
            )
            Joke.objects.create(
                content=f"Joke {i}",
                trait=offense_trait,
                language="es",
            )
        for trait in OffenseTrait.OFFENSE_TYPE_CHOICES:
            if trait[0] == OffenseTrait.NO_OFFENSE_FOUND:
                continue
            for i in range(3):
                offense_trait = OffenseTrait.objects.create(name=trait[0], degree=i)
                Joke.objects.create(
                    content=f"Joke {i}",
                    trait=offense_trait,
                    language="es",
                )

        # Create additional jokes in another language for testing language filtering
        for i in range(5):
            offense_trait = OffenseTrait.objects.create(
                name=OffenseTrait.DISABILITY, degree=(i + 26)
            )
            Joke.objects.create(
                content=f"Chiste {i}",
                trait=offense_trait,
                language="en",
            )

    def test_view_url_exists_at_desired_location(self):
        # Adjust if your URL pattern differs
        response = self.client.get("/api/jokes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("joke-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_uses_correct_serializer(self):
        response = self.client.get(reverse("joke-list"))
        self.assertTrue("session" in response.data)
        self.assertTrue("jokes" in response.data)
        # Verify the session UUID format
        session_uuid = response.data["session"]
        self.assertIsInstance(session_uuid, uuid.UUID)
        # Now check the jokes part of the response
        jokes_data = response.data["jokes"]
        self.assertEqual(len(jokes_data), 20)
        for joke_data in jokes_data:
            self.assertIn("id", joke_data)
            self.assertIn("content", joke_data)

    def test_get_jokes_and_session(self):
        response = self.client.get(reverse("joke-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("session" in response.data)
        self.assertTrue("jokes" in response.data)
        self.assertEqual(len(response.data["jokes"]), 20)
        # Verify the session UUID format
        session_uuid = response.data["session"]
        self.assertIsInstance(session_uuid, uuid.UUID)

    def test_jokes_filtered_by_language(self):
        # Assuming your API and tests run in English by default
        response = self.client.get(reverse("joke-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jokes_data = response.data["jokes"]
        for joke_data in jokes_data:
            self.assertNotIn(
                "Chiste", joke_data["content"], "Jokes should be filtered by language."
            )

    def test_random_jokes_selection(self):
        # Call the endpoint multiple times to check for different results due to random selection
        first_response = self.client.get(reverse("joke-list")).data["jokes"]
        second_response = self.client.get(reverse("joke-list")).data["jokes"]

        # It's possible but unlikely that two random selections are the same, so this test might not be 100% reliable
        self.assertNotEqual(
            first_response,
            second_response,
            "Multiple requests should return different sets of jokes due to random selection.",
        )

    def test_correct_number_of_jokes_returned_with_no_offense_preference(self):
        response = self.client.get(reverse("joke-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        jokes_data = response.data["jokes"]
        # Verify that 20 jokes are returned
        self.assertEqual(len(jokes_data), 20, "Should return exactly 20 jokes.")

        # Count NO_OFFENSE_FOUND jokes
        no_offense_jokes = [
            joke
            for joke in jokes_data
            if joke["trait"] == OffenseTrait.NO_OFFENSE_FOUND
        ]
        self.assertEqual(
            len(no_offense_jokes),
            6,
            "Should return exactly 6 jokes with NO_OFFENSE_FOUND.",
        )


class JokesEvaluationViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a new session and jokes for evaluation
        cls.session = EvaluationSession.objects.create()
        race_offense_trait = OffenseTrait.objects.create(
            name=OffenseTrait.RACE, degree=10
        )
        gender_offense_trait = OffenseTrait.objects.create(
            name=OffenseTrait.GENDER, degree=8
        )
        cls.jokes = [
            Joke.objects.create(
                content="Why did the chicken cross the road?",
                trait=race_offense_trait,
                language="English",
            ),
            Joke.objects.create(
                content="I told my computer I needed a break, and it didn't respond.",
                trait=gender_offense_trait,
                language="English",
            ),
        ]

    def test_submit_evaluations(self):
        evaluations = [
            {"joke": self.jokes[0].id, "liked": True, "session": str(self.session.id)},
            {"joke": self.jokes[1].id, "liked": False, "session": str(self.session.id)},
        ]
        response = self.client.post(
            reverse("evaluate-jokes"), evaluations, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that evaluations are saved
        self.assertEqual(JokeEvaluation.objects.count(), 2)

    # test a jokometian uuid is returned
    def test_submit_evaluations_returns_jakometian_uuid(self):
        evaluations = [
            {"joke": self.jokes[0].id, "liked": True, "session": str(self.session.id)},
            {"joke": self.jokes[1].id, "liked": False, "session": str(self.session.id)},
        ]
        response = self.client.post(
            reverse("evaluate-jokes"), evaluations, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that a Jokometian url is returned
        self.assertEqual(str(response.data["uuid"]), str(self.session.id))


class JokometianDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create offense traits
        cls.race_trait = OffenseTrait.objects.create(name="RACE", degree=10)
        cls.gender_trait = OffenseTrait.objects.create(name="GENDER", degree=8)

        # Create an evaluation session
        cls.session = EvaluationSession.objects.create()

        # Create jokes linked to traits
        cls.joke_with_race = Joke.objects.create(
            content="Race joke", trait=cls.race_trait, language="English"
        )
        cls.joke_with_gender = Joke.objects.create(
            content="Gender joke", trait=cls.gender_trait, language="Spanish"
        )

        # Create evaluations for the session
        JokeEvaluation.objects.create(
            session=cls.session, joke=cls.joke_with_race, liked=True
        )
        JokeEvaluation.objects.create(
            session=cls.session, joke=cls.joke_with_gender, liked=False
        )

    def test_jokometian_detail_view_success(self):
        # Fetch the Jokometian generated from evaluations
        url = reverse("jokometian-detail", kwargs={"uuid": self.session.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Asserts to verify response data structure could include:
        # Checking for the presence of 'name', 'description', and 'image_url' in the response
        self.assertIn("name", response.data)
        self.assertIn("description", response.data)
        self.assertIn("image_url", response.data)
        self.assertIn("traits", response.data)

    def test_jokometian_detail_view_no_evaluations(self):
        # Testing response when no evaluations exist for a given session
        new_session = EvaluationSession.objects.create()
        url = reverse("jokometian-detail", kwargs={"uuid": new_session.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_jokometian_detail_view_invalid_uuid(self):
        # Testing response for a non-existing session UUID
        url = reverse("jokometian-detail", kwargs={"uuid": uuid.uuid4()})
        response = self.client.get(url)

        # Expected to fail due to not found error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

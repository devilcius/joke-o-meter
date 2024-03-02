from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Joke, JokeEvaluation, EvaluationSession, Jokometian
import uuid


class JokeListViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create sample jokes
        for i in range(5):
            Joke.objects.create(
                content=f"Joke {i}",
                offense_degree=1,
                offense_type=Joke.RACE,
                language="English"
            )

    def test_view_url_exists_at_desired_location(self):
        # Adjust if your URL pattern differs
        response = self.client.get('/jokes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('joke-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_uses_correct_serializer(self):
        response = self.client.get(reverse('joke-list'))
        self.assertTrue('session' in response.data)
        self.assertTrue('jokes' in response.data)
        # Verify the session UUID format
        session_uuid = response.data['session']
        self.assertIsInstance(session_uuid, uuid.UUID)
        # Now check the jokes part of the response
        jokes_data = response.data['jokes']
        self.assertEqual(len(jokes_data), 5)  # Adjust based on setUpTestData
        for joke_data in jokes_data:
            self.assertIn('id', joke_data)
            self.assertIn('content', joke_data)

    def test_get_jokes_and_session(self):
        response = self.client.get(reverse('joke-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('session' in response.data)
        self.assertTrue('jokes' in response.data)
        self.assertEqual(len(response.data['jokes']), 5)
        # Verify the session UUID format
        session_uuid = response.data['session']
        self.assertIsInstance(session_uuid, uuid.UUID)


class JokesEvaluationViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a new session and jokes for evaluation
        cls.session = EvaluationSession.objects.create()
        cls.jokes = [
            Joke.objects.create(content="Why did the chicken cross the road?",
                                offense_degree=1, offense_type=Joke.RACE, language="English"),
            Joke.objects.create(content="I told my computer I needed a break, and it didn't respond.",
                                offense_degree=2, offense_type=Joke.GENDER, language="English")
        ]

    def test_submit_evaluations(self):
        evaluations = [
            {"joke": self.jokes[0].id, "liked": True,
                "session": str(self.session.id)},
            {"joke": self.jokes[1].id, "liked": False,
                "session": str(self.session.id)}
        ]
        response = self.client.post(
            reverse('evaluate-jokes'), evaluations, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that evaluations are saved
        self.assertEqual(JokeEvaluation.objects.count(), 2)

    # test a jokometian is returned
    def test_submit_evaluations_returns_jokometian(self):
        evaluations = [
            {"joke": self.jokes[0].id, "liked": True,
                "session": str(self.session.id)},
            {"joke": self.jokes[1].id, "liked": False,
                "session": str(self.session.id)}
        ]
        response = self.client.post(
            reverse('evaluate-jokes'), evaluations, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify that a Jokometian instance is returned
        self.assertEqual(Jokometian.objects.count(), 1)


class JokometianDetailViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a Jokometian instance
        cls.jokometian = Jokometian.objects.create(
            uuid=uuid.uuid4(),
            # Set other necessary fields for your Jokometian model
        )

    def test_retrieve_jokometian_by_uuid(self):
        # Construct the URL using the 'reverse' function and the Jokometian's UUID
        url = reverse('jokometian-detail',
                      kwargs={'uuid': self.jokometian.uuid})

        # Make a GET request to the constructed URL
        response = self.client.get(url)

        # Verify the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data (example checks, adjust according to your model fields)
        self.assertEqual(response.data['uuid'], str(self.jokometian.uuid))
        # Add more assertions as necessary to verify the serializer data

from rest_framework.test import APITestCase
from api.models import Joke
from api.serializers import JokeSerializer


class JokeSerializerTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a joke to use for testing the serializer
        cls.joke = Joke.objects.create(
            content="Serializer test joke", offense_degree=1, offense_type=Joke.GENDER)

    def test_contains_expected_fields(self):
        serializer = JokeSerializer(instance=self.joke)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'content']))

    def test_content_field_content(self):
        serializer = JokeSerializer(instance=self.joke)
        data = serializer.data
        self.assertEqual(data['content'], self.joke.content)

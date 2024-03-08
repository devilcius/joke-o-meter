from django.test import TestCase
from api.models import Joke, OffenseTrait, JokometianRanking
from api.serializers import (
    JokeSerializer,
    JokometianSerializer,
    OffenseTraitSerializer,
    JokometianRankingSerializer,
)
from api.dtos import Jokometian


class JokeSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create sample traits for jokes
        cls.trait_with_name = OffenseTrait.objects.create(name="Humor", degree=5)

        # Create jokes with and without traits
        cls.joke_with_trait = Joke.objects.create(
            content="Why did the chicken cross the road?",
            trait=cls.trait_with_name,
            language="English",
        )

        cls.joke_without_trait = Joke.objects.create(
            content="To get to the other side.", trait=None, language="English"
        )

    def test_serialize_joke_with_trait(self):
        """
        Test serialization of a Joke instance that has an associated trait.
        """
        serializer = JokeSerializer(instance=self.joke_with_trait)
        trait_serializer = OffenseTraitSerializer(instance=self.trait_with_name)
        expected_data = {
            "id": self.joke_with_trait.id,
            "content": "Why did the chicken cross the road?",
            "trait": trait_serializer.data,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serialize_joke_without_trait(self):
        """
        Test serialization of a Joke instance that does not have an associated trait.
        """
        serializer = JokeSerializer(instance=self.joke_without_trait)
        expected_data = {
            "id": self.joke_without_trait.id,
            "content": "To get to the other side.",
            "trait": None,  # Expect trait to be None since there's no associated trait
        }

        self.assertEqual(serializer.data, expected_data)

    def test_trait_method_field(self):
        """
        Test the custom get_trait method to ensure it correctly handles both presence and absence of a trait.
        """
        # Check with trait
        self.assertEqual(
            self.joke_with_trait.trait.name,
            JokeSerializer().get_trait(self.joke_with_trait),
        )

        # Check without trait
        self.assertIsNone(JokeSerializer().get_trait(self.joke_without_trait))


class JokometianSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some OffenseTrait instances for use in tests
        cls.trait1 = OffenseTrait.objects.create(name=OffenseTrait.RACE, degree=5)
        cls.trait2 = OffenseTrait.objects.create(name=OffenseTrait.GENDER, degree=3)
        cls.joke1 = Joke.objects.create(
            content="Test Joke 1", trait=cls.trait1, language="en"
        )
        cls.joke2 = Joke.objects.create(
            content="Test Joke 2", trait=cls.trait2, language="en"
        )

    def test_jokometian_serializer_with_traits(self):
        # Create a Jokometian instance with traits and jokes
        jokometian = Jokometian(
            traits=[self.trait1, self.trait2], jokes=[self.joke1, self.joke2]
        )

        # Serialize the Jokometian instance
        serializer = JokometianSerializer(instance=jokometian)

        serialized_traits = OffenseTraitSerializer(
            instance=[self.trait1, self.trait2], many=True
        ).data

        serialized_jokes = JokeSerializer(
            instance=[self.joke1, self.joke2], many=True
        ).data

        # Expected data format
        expected_data = {
            "id": str(jokometian.id),
            "traits": serialized_traits,
            "jokes": serialized_jokes,
            "name": "",
            "description": "",
            "image_url": "",
        }

        # Test that the serializer data matches the expected data
        self.assertEqual(serializer.data, expected_data)

    def test_jokometian_serializer_empty_traits(self):
        # Create a Jokometian instance without traits nor jokes
        jokometian = Jokometian()

        # Serialize the Jokometian instance
        serializer = JokometianSerializer(instance=jokometian)

        # Expected data format
        expected_data = {
            "id": str(jokometian.id),
            "traits": [],  # No traits
            "jokes": [],  # No jokes
            "name": "",
            "description": "",
            "image_url": "",
        }

        # Test that the serializer data matches the expected data for an instance without traits
        self.assertEqual(serializer.data, expected_data)


class JokometianRankingSerializerTest(TestCase):
    def setUp(self):
        self.jokometian_attributes = {
            "name": "Test Joke",
            "score": 5,
            "image_url": "http://example.com/test.jpg",
        }

        self.serializer_data = {
            "name": "Test Joke",
            "score": 5,
            "image_url": "http://example.com/test.jpg",
        }

        self.jokometian = JokometianRanking.objects.create(**self.jokometian_attributes)
        self.serializer = JokometianRankingSerializer(instance=self.jokometian)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(["name", "score", "image_url"]))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], self.jokometian_attributes["name"])

    def test_score_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["score"], self.jokometian_attributes["score"])

    def test_image_url_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["image_url"], self.jokometian_attributes["image_url"])

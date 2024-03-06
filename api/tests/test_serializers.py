from rest_framework.test import APITestCase
from django.test import TestCase
from api.models import Joke, OffenseTrait
from api.serializers import JokeSerializer, JokometianSerializer, OffenseTraitSerializer
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
        expected_data = {
            "id": self.joke_with_trait.id,
            "content": "Why did the chicken cross the road?",
            "trait": "Humor",
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

    def test_jokometian_serializer_with_traits(self):
        # Create a Jokometian instance with traits
        jokometian = Jokometian(traits=[self.trait1, self.trait2])

        # Serialize the Jokometian instance
        serializer = JokometianSerializer(instance=jokometian)

        serialized_traits = OffenseTraitSerializer(
            instance=[self.trait1, self.trait2], many=True
        ).data

        # Expected data format
        expected_data = {
            "id": str(jokometian.id),
            "traits": serialized_traits,
            "name": "",
            "description": "",
            "image_url": "",
        }

        # Test that the serializer data matches the expected data
        self.assertEqual(serializer.data, expected_data)

    def test_jokometian_serializer_empty_traits(self):
        # Create a Jokometian instance without traits
        jokometian = Jokometian()

        # Serialize the Jokometian instance
        serializer = JokometianSerializer(instance=jokometian)

        # Expected data format
        expected_data = {
            "id": str(jokometian.id),
            "traits": [],  # No traits
            "name": "",
            "description": "",
            "image_url": "",
        }

        # Test that the serializer data matches the expected data for an instance without traits
        self.assertEqual(serializer.data, expected_data)

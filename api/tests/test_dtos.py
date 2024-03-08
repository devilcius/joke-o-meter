from django.test import TestCase
from uuid import UUID
from api.jokometian_utils import Jokometian
from api.models import OffenseTrait, Joke


class JokometianTest(TestCase):
    def test_jokometian_initialization(self):
        # Simulate creating offense traits
        offense_traits = [
            OffenseTrait(name=OffenseTrait.RACE, degree=5),
            OffenseTrait(name=OffenseTrait.GENDER, degree=3),
        ]

        # Simulate creating jokes
        jokes = [
            Joke(content="Test Joke 1", trait=offense_traits[0]),
            Joke(content="Test Joke 2", trait=offense_traits[1]),
        ]

        # Initialize Jokometian instance
        jokometian = Jokometian(
            traits=offense_traits,
            jokes=jokes,
            name="Test Name",
            description="Test Description",
            image_url="http://example.com/image.svg",
        )

        # Validate that the Jokometian instance was correctly initialized
        self.assertTrue(isinstance(jokometian.id, UUID))
        self.assertEqual(len(jokometian.traits), 2)
        self.assertEqual(len(jokometian.jokes), 2)
        self.assertEqual(jokometian.name, "Test Name")
        self.assertEqual(jokometian.description, "Test Description")
        self.assertEqual(jokometian.image_url, "http://example.com/image.svg")

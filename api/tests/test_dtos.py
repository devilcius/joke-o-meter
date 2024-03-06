from django.test import TestCase
from uuid import UUID
from api.jokometian_utils import Jokometian
from api.models import OffenseTrait


class JokometianTest(TestCase):
    def test_jokometian_initialization(self):
        # Simulate creating offense traits
        offense_traits = [
            OffenseTrait(name=OffenseTrait.RACE, degree=5),
            OffenseTrait(name=OffenseTrait.GENDER, degree=3),
        ]

        # Initialize Jokometian instance
        jokometian = Jokometian(
            traits=offense_traits,
            name="Test Name",
            description="Test Description",
            image_url="http://example.com/image.svg",
        )

        # Validate that the Jokometian instance was correctly initialized
        self.assertTrue(isinstance(jokometian.id, UUID))
        self.assertEqual(len(jokometian.traits), 2)
        self.assertEqual(jokometian.name, "Test Name")
        self.assertEqual(jokometian.description, "Test Description")
        self.assertEqual(jokometian.image_url, "http://example.com/image.svg")

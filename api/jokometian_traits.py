from django.conf import settings
from django.utils.translation import gettext as _
from .models import OffenseTrait
from django.utils import translation


def traits():
    traits = {
        OffenseTrait.RACE: {
            "name": _("Fiery"),
            "description": _(
                "Born from the flames of challenge, always ready to ignite change."
            ),
            "image_url": settings.STATIC_URL + "images/jokometians/image_race.svg",
        },
        OffenseTrait.RELIGION: {
            "name": _("Spiritual"),
            "description": _(
                "With a deep spiritual connection, seeking harmony in all."
            ),
            "image_url": settings.STATIC_URL + "images/jokometians/image_religion.svg",
        },
        OffenseTrait.ETHNICITY: {
            "name": _("Diverse"),
            "description": _(
                "Celebrating diversity, embodying the beauty of all cultures."
            ),
            "image_url": settings.STATIC_URL + "images/jokometians/image_ethnicity.svg",
        },
        OffenseTrait.GENDER: {
            "name": _("Wise"),
            "description": _("Imbued with wisdom, understanding the balance of power."),
            "image_url": settings.STATIC_URL + "images/jokometians/image_gender.svg",
        },
        OffenseTrait.SEXUAL_ORIENTATION: {
            "name": _("Radiant"),
            "description": _("Radiating acceptance, embracing all forms of love."),
            "image_url": settings.STATIC_URL
            + "images/jokometians/image_sexual_orientation.svg",
        },
        OffenseTrait.DISABILITY: {
            "name": _("Resilient"),
            "description": _(
                "Showing unmatched resilience, overcoming every obstacle."
            ),
            "image_url": settings.STATIC_URL
            + "images/jokometians/image_disability.svg",
        },
        OffenseTrait.GENERIC_VIOLENCE: {
            "name": _("Fierce"),
            "description": _("Fierce in the face of adversity, a warrior of light."),
            "image_url": settings.STATIC_URL + "images/jokometians/image_violence.svg",
        },
        OffenseTrait.NO_OFFENSE_FOUND: {
            "name": _("Pure Soul"),
            "description": _(
                "An untainted soul, spreading joy and laughter wherever they go."
            ),
            "image_url": settings.STATIC_URL + "images/jokometians/image_pure.svg",
        },
        "GRUMPY": {
            "name": _("Grumpy"),
            "description": _(
                "A grumpy soul, always ready to complain. No joke is good enough."
            ),
            "image_url": settings.STATIC_URL + "images/jokometians/image_grumpy.svg",
        },
        "GIGGLY": {
            "name": _("Giggly"),
            "description": _(
                "A giggly soul, always ready to laugh. Every joke is a good joke."
            ),
            "image_url": settings.STATIC_URL + "images/jokometians/image_giggly.svg",
        },
    }

    return traits

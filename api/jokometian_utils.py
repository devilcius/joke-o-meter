from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import OffenseTrait, JokometianRanking
from .dtos import Jokometian
from django.db import transaction
from django.db.models import F

trait_names = {
    OffenseTrait.RACE: _("Fiery"),
    OffenseTrait.RELIGION: _("Spiritual"),
    OffenseTrait.ETHNICITY: _("Diverse"),
    OffenseTrait.GENDER: _("Wise"),
    OffenseTrait.SEXUAL_ORIENTATION: _("Radiant"),
    OffenseTrait.DISABILITY: _("Resilient"),
    OffenseTrait.GENERIC_VIOLENCE: _("Fierce"),
    OffenseTrait.NO_OFFENSE_FOUND: _("Pure Soul"),
}

trait_descriptions = {
    OffenseTrait.RACE: _(
        "Born from the flames of challenge, always ready to ignite change."
    ),
    OffenseTrait.RELIGION: _(
        "With a deep spiritual connection, seeking harmony in all."
    ),
    OffenseTrait.ETHNICITY: _(
        "Celebrating diversity, embodying the beauty of all cultures."
    ),
    OffenseTrait.GENDER: _("Imbued with wisdom, understanding the balance of power."),
    OffenseTrait.SEXUAL_ORIENTATION: _(
        "Radiating acceptance, embracing all forms of love."
    ),
    OffenseTrait.DISABILITY: _(
        "Showing unmatched resilience, overcoming every obstacle."
    ),
    OffenseTrait.GENERIC_VIOLENCE: _(
        "Fierce in the face of adversity, a warrior of light."
    ),
    OffenseTrait.NO_OFFENSE_FOUND: _(
        "An untainted soul, spreading joy and laughter wherever they go."
    ),
}

# Adjusted image mappings to use the OffenseTrait model's identifiers
trait_images = {
    OffenseTrait.RACE: settings.STATIC_URL + "images/jokometians/image_race.svg",
    OffenseTrait.RELIGION: settings.STATIC_URL
    + "images/jokometians/image_religion.svg",
    OffenseTrait.ETHNICITY: settings.STATIC_URL
    + "images/jokometians/image_ethnicity.svg",
    OffenseTrait.GENDER: settings.STATIC_URL + "images/jokometians/image_gender.svg",
    OffenseTrait.SEXUAL_ORIENTATION: settings.STATIC_URL
    + "images/jokometians/image_sexual_orientation.svg",
    OffenseTrait.DISABILITY: settings.STATIC_URL
    + "images/jokometians/image_disability.svg",
    OffenseTrait.GENERIC_VIOLENCE: settings.STATIC_URL
    + "images/jokometians/image_violence.svg",
    OffenseTrait.NO_OFFENSE_FOUND: settings.STATIC_URL
    + "images/jokometians/image_pure.svg",
}


def create_jokometian_from_jokes_evaluation(evaluations):
    # Initialize a list to keep track of aggregated OffenseTrait objects
    aggregated_traits = []
    liked_jokes = []

    for eval in evaluations:
        if eval.liked:
            # Add the liked joke to the liked_jokes list
            if eval.joke not in liked_jokes:
                liked_jokes.append(eval.joke)

            existing_trait = next(
                (t for t in aggregated_traits if t.name == eval.joke.trait.name), None
            )
            if existing_trait:
                # Increment the degree of the existing trait object
                existing_trait.degree += eval.joke.trait.degree
            else:
                # Instantiate a new OffenseTrait object with initial degree, but don't save it to the database
                new_trait = OffenseTrait(
                    name=eval.joke.trait.name, degree=eval.joke.trait.degree
                )
                aggregated_traits.append(new_trait)

    # Exclude NO_OFFENSE_FOUND unless it's the only trait liked
    no_offense_found_trait = [
        t for t in aggregated_traits if t.name == OffenseTrait.NO_OFFENSE_FOUND
    ]
    if len(aggregated_traits) > 1 and no_offense_found_trait:
        aggregated_traits.remove(no_offense_found_trait[0])
        # remove also from liked jokes
        liked_jokes = [
            j for j in liked_jokes if j.trait.name != OffenseTrait.NO_OFFENSE_FOUND
        ]

    # Sort the traits by their aggregated degree to find the top traits
    dominant_traits = sorted(aggregated_traits, key=lambda t: t.degree, reverse=True)
    if len(dominant_traits) > 2:
        dominant_traits = dominant_traits[:3]

    # Creating the Jokometian instance with the top dominant traits
    jokometian = Jokometian()
    jokometian.traits = dominant_traits
    jokometian.jokes = liked_jokes

    if dominant_traits:
        # Set additional properties based on dominant traits
        dominant_trait = dominant_traits[0]
        jokometian.name = dominant_trait.name
        jokometian.description = trait_descriptions.get(
            dominant_trait.name,
            "An enigmatic Jokometian with a unique blend of traits.",
        )
        jokometian.image_url = trait_images.get(
            dominant_trait.name, settings.STATIC_URL + "images/jokometians/default.svg"
        )
    else:
        # Set default Jokometian properties when no jokes are liked
        jokometian.name = "Jokometian"
        jokometian.description = _(
            "An enigmatic Jokometian with a unique blend of traits."
        )
        jokometian.image_url = settings.STATIC_URL + "images/jokometians/default.svg"

    return jokometian


def update_jokometian_ranking(evaluations):

    # Create a Jokometian from the evaluations
    jokometian = create_jokometian_from_jokes_evaluation(evaluations)

    # Calculate the total score from the jokometian's traits
    total_score = sum(trait.degree for trait in jokometian.traits)

    with transaction.atomic():
        # Retrieve or create the JokometianRanking instance
        ranking, created = JokometianRanking.objects.get_or_create(
            name=jokometian.name,
            defaults={
                "image_url": jokometian.image_url,  # Set during creation
                "score": total_score,  # Initial score set for new creation
            },
        )

        if not created:
            # For existing rankings, update both score and image_url
            ranking.score = F("score") + total_score
            # Updating image_url for existing instances
            ranking.image_url = jokometian.image_url
            ranking.save()

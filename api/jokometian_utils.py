from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import OffenseTrait, JokometianRanking
from .dtos import Jokometian
from django.db import transaction
from django.db.models import F
from .jokometian_traits import traits


def create_jokometian_from_jokes_evaluation(evaluations):
    # Initialize a list to keep track of aggregated OffenseTrait objects
    aggregated_traits = []
    liked_jokes = []
    JOKOMETIAN_TRAITS = traits()

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
    jokometian.jokes = liked_jokes
    if len(evaluations) > 0:
        jokometian.id = evaluations[0].session.id

    # No jokes liked
    if len(evaluations) > 0 and len(liked_jokes) == 0:
        # Set grumpy Jokometian properties
        dominant_traits = [OffenseTrait(name="GRUMPY", degree=10)]
    # All evaluation's jokes liked
    evaluation_liked_jokes = [eval.joke for eval in evaluations if eval.liked]
    if len(evaluation_liked_jokes) > 0 and (
        len(evaluation_liked_jokes) == len(evaluations)
    ):
        # Set giglly Jokometian properties
        dominant_traits = [OffenseTrait(name="GIGGLY", degree=10)]
        # If you like all jokes, uou have no favorite jokes
        jokometian.jokes = []

    jokometian.traits = dominant_traits

    if dominant_traits:
        dominant_trait = dominant_traits[0]
        jokometian.key_name = dominant_trait.name
        trait_info = JOKOMETIAN_TRAITS.get(dominant_traits[0].name, None)
        jokometian.description = trait_info.get(
            "description", "An enigmatic Jokometian with a unique blend of traits."
        )
        jokometian.name = trait_info.get("name", "Jokometian")
        jokometian.image_url = trait_info.get(
            "image_url", settings.STATIC_URL + "images/jokometians/default.svg"
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
            name=jokometian.key_name,
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

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.translation import gettext

# Trait mappings for names
trait_names = {
    'race_rate': _("Fiery"),
    'religion_rate': _("Spiritual"),
    'ethnicity_rate': _("Diverse"),
    'gender_rate': _("Wise"),
    'sexual_orientation_rate': _("Radiant"),
    'disability_rate': _("Resilient"),
    'violence_rate': _("Fierce"),
    'no_offense_rate': _("Pure Soul"),
}

# Descriptive mappings for descriptions
trait_descriptions = {
    'race_rate': _("born from the flames of challenge, always ready to ignite change."),
    'religion_rate': _("with a deep spiritual connection, seeking harmony in all."),
    'ethnicity_rate': _("celebrating diversity, embodying the beauty of all cultures."),
    'gender_rate': _("imbued with wisdom, understanding the balance of power."),
    'sexual_orientation_rate': _("radiating acceptance, embracing all forms of love."),
    'disability_rate': _("showing unmatched resilience, overcoming every obstacle."),
    'violence_rate': _("fierce in the face of adversity, a warrior of light."),
    'no_offense_rate': _("an untainted soul, spreading joy and laughter wherever they go."),
}

# Image mappings for each trait
trait_images = {
    'race_rate': settings.STATIC_URL + "api/images/jokometians/image_race.svg",
    'religion_rate': settings.STATIC_URL + "api/images/jokometians/image_religion.svg",
    'ethnicity_rate': settings.STATIC_URL + "api/images/jokometians/image_ethnicity.svg",
    'gender_rate': settings.STATIC_URL + "api/images/jokometians/image_gender.svg",
    'sexual_orientation_rate': settings.STATIC_URL + "api/images/jokoemtians/image_sexual_orientation.svg",
    'disability_rate': settings.STATIC_URL + "api/images/jokometians/image_disability.svg",
    'violence_rate': settings.STATIC_URL + "api/images/jokometians/image_violence.svg",
    'no_offense_rate': settings.STATIC_URL + "api/images/jokometians/image_pure.svg",
}


def generate_jokometian_name(jokometian):
    # Sort traits by their rates in descending order and filter out non-dominant traits
    sorted_traits = sorted(
        trait_names.keys(), key=lambda x: getattr(jokometian, x), reverse=True)
    dominant_trait = sorted_traits[0] if getattr(
        jokometian, sorted_traits[0]) > 50 else 'no_offense_rate'
    return f"{trait_names[dominant_trait]} Jokometian"


def generate_jokometian_description(jokometian):
    # Construct the description based on the top traits, considering their rates
    sorted_traits = sorted(trait_descriptions.keys(),
                           key=lambda x: getattr(jokometian, x), reverse=True)
    top_descriptions = [str(trait_descriptions[trait]) for trait in sorted_traits if getattr(
        jokometian, trait) > 20][:2]  # Convert to string here

    if not top_descriptions:  # Fallback to no offense description, ensure conversion to string if needed
        return gettext("A Jokometian ") + str(trait_descriptions['no_offense_rate'])
    return gettext("A Jokometian ") + " and ".join(top_descriptions)


def generate_jokometian_image(jokometian):
    # Sort traits by their rates in descending order and filter out non-dominant traits
    sorted_traits = sorted(trait_images.keys(),
                           key=lambda x: getattr(jokometian, x), reverse=True)
    dominant_trait = sorted_traits[0] if getattr(
        jokometian, sorted_traits[0]) > 20 else 'no_offense_rate'
    return trait_images[dominant_trait]


def determine_offense_rates_for_evaluation(evaluations):
    # Initialize a dictionary to hold offense rates
    offense_rates = {
        'race_rate': 0,
        'religion_rate': 0,
        'ethnicity_rate': 0,
        'gender_rate': 0,
        'sexual_orientation_rate': 0,
        'disability_rate': 0,
        'violence_rate': 0,
        'no_offense_rate': 100  # Assuming a base rate for no offense
    }

    # Initialize a counter for liked evaluations
    total_liked = 0

    # Process each evaluation in the list
    for evaluation in evaluations:
        if evaluation.liked:
            total_liked += 1
            offense_type = evaluation.joke.offense_type.lower() + '_rate'
            if offense_type in offense_rates:
                offense_rates[offense_type] += 1

    # Calculate rates for each offense type based on liked evaluations
    if total_liked > 0:
        for offense_type in offense_rates.keys():
            # Calculate and update offense rates
            # Exclude 'no_offense_rate' from direct calculation
            if offense_type != 'no_offense_rate':
                offense_rates[offense_type] = (
                    offense_rates[offense_type] / total_liked) * 100

        # Adjust 'no_offense_rate' based on other rates
        # Exclude the initial no_offense_rate
        total_rates = sum(offense_rates.values()) - \
            offense_rates['no_offense_rate']
        offense_rates['no_offense_rate'] = max(0, 100 - total_rates)

    return offense_rates

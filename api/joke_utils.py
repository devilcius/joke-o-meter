from .models import Joke, OffenseTrait
import random


def prepare_joke_list(language_code):
    # Filter jokes by current language
    jokes_language_filtered = Joke.objects.filter(language=language_code)

    # Initialize a list to hold the final selection of jokes
    selected_jokes = []

    # Fetch and add 7 NO_OFFENSE_FOUND jokes
    no_offense_jokes = list(
        jokes_language_filtered.filter(
            trait__name=OffenseTrait.NO_OFFENSE_FOUND
        ).order_by("?")[:6]
    )
    selected_jokes.extend(no_offense_jokes)

    # For each other type, fetch 2 jokes
    for offense_type in OffenseTrait.OFFENSE_TYPE_CHOICES:
        if offense_type[0] == OffenseTrait.NO_OFFENSE_FOUND:
            continue  # Skip NO_OFFENSE_FOUND since it's already handled
        # Fetch 2 jokes of the current type, ensuring they match the language
        jokes_of_type = list(
            jokes_language_filtered.filter(trait__name=offense_type[0]).order_by("?")[
                :2
            ]
        )
        selected_jokes.extend(jokes_of_type)

    # Shuffle the combined list of selected jokes
    random.shuffle(selected_jokes)

    return selected_jokes

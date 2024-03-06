from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Joke, EvaluationSession, JokeEvaluation, OffenseTrait
from .serializers import JokeSerializer, JokeEvaluationSerializer, JokometianSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .jokometian_utils import create_jokometian_from_jokes_evaluation
import random
from django.utils.translation import get_language
from django.urls import reverse


class JokeListView(APIView):
    def get(self, request, format=None):
        # Create a new EvaluationSession
        session = EvaluationSession.objects.create()

        # Get the current language set in Django's settings
        current_language = get_language()

        # Filter jokes by current language
        jokes_language_filtered = Joke.objects.filter(language=current_language)

        # Separate NO_OFFENSE_FOUND jokes and others
        # filter all jokes with NO_OFFENSE_FOUND trait
        no_offense_jokes = list(
            jokes_language_filtered.filter(trait__name=OffenseTrait.NO_OFFENSE_FOUND)
        )
        other_jokes = list(
            jokes_language_filtered.exclude(trait__name=OffenseTrait.NO_OFFENSE_FOUND)
        )

        # Randomly select 10 NO_OFFENSE_FOUND jokes, ensuring not to exceed the list size
        no_offense_selection = random.sample(
            no_offense_jokes, min(len(no_offense_jokes), 10)
        )

        # Determine how many more jokes are needed to make up the total of 25
        remaining_joke_count = 25 - len(no_offense_selection)

        # Randomly select the remaining jokes from other types
        other_jokes_selection = random.sample(
            other_jokes, min(len(other_jokes), remaining_joke_count)
        )

        # Combine the two selections
        selected_jokes = no_offense_selection + other_jokes_selection

        # Serialize the selected jokes
        serializer = JokeSerializer(selected_jokes, many=True)

        # Shuffle the jokes
        shuffled_jokes = random.sample(serializer.data, len(serializer.data))

        # Include the session UUID in the response
        return Response(
            {
                "session": session.id,  # Send the UUID to the client
                "jokes": shuffled_jokes,
            }
        )


class JokesEvaluationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JokeEvaluationSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()  # Save the evaluations
            response = {
                "uuid": serializer.validated_data[0]["session"].id,
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JokometianDetailView(APIView):
    """
    Generates a Jokometian dto based on the evaluations of a session.
    """

    def get(self, request, uuid, format=None):
        # Find all evaluations for the given UUID
        evaluations = JokeEvaluation.objects.filter(session=uuid)
        if not evaluations:
            return Response(
                "No evaluations found for the given session UUID.",
                status=status.HTTP_404_NOT_FOUND,
            )
        jokometian = create_jokometian_from_jokes_evaluation(evaluations)
        serializer = JokometianSerializer(jokometian)
        return Response(serializer.data, status=status.HTTP_200_OK)

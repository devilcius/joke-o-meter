from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Joke, EvaluationSession, JokeEvaluation, OffenseTrait
from .serializers import JokeSerializer, JokeEvaluationSerializer, JokometianSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .jokometian_utils import create_jokometian_from_jokes_evaluation
import random
from django.utils.translation import get_language
from .joke_utils import prepare_joke_list


class JokeListView(APIView):
    def get(self, request, format=None):
        # Create a new EvaluationSession
        session = EvaluationSession.objects.create()

        # Get the current language set in Django's settings
        current_language = get_language()

        joke_list = prepare_joke_list(current_language)

        # Serialize the selected jokes
        serializer = JokeSerializer(joke_list, many=True)

        # Include the session UUID in the response
        return Response(
            {
                "session": session.id,  # Send the UUID to the client
                "jokes": serializer.data,
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

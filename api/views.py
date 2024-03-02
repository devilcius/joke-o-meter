from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Joke, EvaluationSession
from .serializers import JokeSerializer, JokeEvaluationSerializer, JokometianSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Jokometian
from .jokometian_utils import determine_offense_rates_for_evaluation


class JokeListView(APIView):
    def get(self, request, format=None):
        # Create a new EvaluationSession
        session = EvaluationSession.objects.create()

        jokes = Joke.objects.all()
        serializer = JokeSerializer(jokes, many=True)

        # Include the session UUID in the response
        return Response({
            'session': session.id,  # Send the UUID to the client
            'jokes': serializer.data
        })


class JokesEvaluationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JokeEvaluationSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()  # Save the evaluations

            # Calculate offense rates based on the evaluations
            offense_rates = determine_offense_rates_for_evaluation(
                serializer.instance)

            # Here, you could use the offense rates to update or create a Jokometian instance.
            # This is just a placeholder for where you would include that logic.
            jokometian, created = Jokometian.objects.update_or_create(
                defaults=offense_rates
            )

            # Serialize and return the updated or created Jokometian
            jokometian_serializer = JokometianSerializer(
                jokometian, context={'request': request})
            return Response(jokometian_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JokometianDetailView(APIView):
    """
    Retrieve a Jokometian instance by its UUID.
    """

    def get(self, request, uuid, format=None):
        jokometian = get_object_or_404(Jokometian, uuid=uuid)
        serializer = JokometianSerializer(
            jokometian, context={'request': request})
        return Response(serializer.data)

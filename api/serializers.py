from rest_framework import serializers
from .models import Joke, JokeEvaluation, Jokometian
from django.urls import reverse


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'content']  # Only include id and content


class JokeEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JokeEvaluation
        fields = ['joke', 'liked', 'session']

    def create(self, validated_data):
        """
        Create and return a new `JokesEvaluation` instance, given the validated data.
        """
        return JokeEvaluation.objects.create(**validated_data)


class JokometianSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Jokometian
        fields = ['uuid', 'image_url', 'name', 'description', 'detail_url']

    def get_detail_url(self, obj):
        # Assuming you have a named URL 'jokometian-detail' taking 'uuid' as an argument
        request = self.context.get('request')
        return request.build_absolute_uri(reverse('jokometian-detail', kwargs={'uuid': obj.uuid}))

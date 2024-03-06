from rest_framework import serializers
from .models import Joke, JokeEvaluation, OffenseTrait


class JokeSerializer(serializers.ModelSerializer):
    trait = serializers.SerializerMethodField()

    class Meta:
        model = Joke
        fields = ["id", "content", "trait"]

    def get_trait(self, obj):
        return obj.trait.name if obj.trait else None


class JokeEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JokeEvaluation
        fields = ["joke", "liked", "session"]

    def create(self, validated_data):
        """
        Create and return a new `JokesEvaluation` instance, given the validated data.
        """
        return JokeEvaluation.objects.create(**validated_data)


class OffenseTraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffenseTrait
        fields = ["name", "degree"]


class JokometianSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    traits = serializers.SerializerMethodField()
    image_url = serializers.URLField()
    name = serializers.CharField()
    description = serializers.CharField()

    def get_traits(self, obj):
        # Use the OffenseTraitSerializer to serialize the traits
        serializer = OffenseTraitSerializer(instance=obj.traits, many=True)
        return serializer.data

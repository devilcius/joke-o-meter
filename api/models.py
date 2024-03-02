from django.db import models
import uuid
from .jokometian_utils import generate_jokometian_name, generate_jokometian_description, generate_jokometian_image


class Joke(models.Model):
    RACE = 'RACE'
    RELIGION = 'RELIGION'
    ETHNICITY = 'ETHNICITY'
    GENDER = 'GENDER'
    SEXUAL_ORIENTATION = 'SEXUAL_ORIENTATION'
    DISABILITY = 'DISABILITY'
    GENERIC_VIOLENCE = 'VIOLENCE'
    NO_OFFENSE_FOUND = 'NO_OFFENSE_FOUND'

    OFFENSE_TYPE_CHOICES = [
        (RACE, 'Race'),
        (RELIGION, 'Religion'),
        (ETHNICITY, 'Ethnicity'),
        (GENDER, 'Gender'),
        (SEXUAL_ORIENTATION, 'Sexual Orientation'),
        (DISABILITY, 'Disability'),
        (GENERIC_VIOLENCE, 'Generic Violence'),
        (NO_OFFENSE_FOUND, 'No Offense Found'),
    ]

    content = models.TextField()
    offense_degree = models.IntegerField(default=0)
    offense_type = models.CharField(
        max_length=50,
        choices=OFFENSE_TYPE_CHOICES,
        null=True
    )
    language = models.CharField(max_length=100, default='Spanish')


class EvaluationSession(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class JokeEvaluation(models.Model):
    session = models.ForeignKey(
        EvaluationSession, on_delete=models.CASCADE, related_name="evaluations", default=uuid.uuid4)
    joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
    liked = models.BooleanField()


class Jokometian(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Properties for offense rates
    race_rate = models.FloatField(default=0)
    religion_rate = models.FloatField(default=0)
    ethnicity_rate = models.FloatField(default=0)
    gender_rate = models.FloatField(default=0)
    sexual_orientation_rate = models.FloatField(default=0)
    disability_rate = models.FloatField(default=0)
    violence_rate = models.FloatField(default=0)
    no_offense_rate = models.FloatField(default=0)

    @property
    def name(self):
        # Dynamic name generation logic based on offense rates
        return generate_jokometian_name(self)

    @property
    def description(self):
        # Dynamic description generation logic based on offense rates
        return generate_jokometian_description(self)

    @property
    def image_url(self):
        return generate_jokometian_image(self)

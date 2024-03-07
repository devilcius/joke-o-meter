from django.db import models
import uuid


class OffenseTrait(models.Model):
    RACE = "RACE"
    RELIGION = "RELIGION"
    ETHNICITY = "ETHNICITY"
    GENDER = "GENDER"
    SEXUAL_ORIENTATION = "SEXUAL_ORIENTATION"
    DISABILITY = "DISABILITY"
    GENERIC_VIOLENCE = "GENERIC_VIOLENCE"
    NO_OFFENSE_FOUND = "NO_OFFENSE_FOUND"
    OFFENSE_TYPE_CHOICES = [
        (RACE, "Race"),
        (RELIGION, "Religion"),
        (ETHNICITY, "Ethnicity"),
        (GENDER, "Gender"),
        (SEXUAL_ORIENTATION, "Sexual Orientation"),
        (DISABILITY, "Disability"),
        (GENERIC_VIOLENCE, "Generic Violence"),
        (NO_OFFENSE_FOUND, "No Offense Found"),
    ]

    name = models.CharField(max_length=50, choices=OFFENSE_TYPE_CHOICES)
    degree = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} | {self.degree}"

    class Meta:
        unique_together = ["name", "degree"]


class Joke(models.Model):
    content = models.TextField()
    trait = models.ForeignKey(
        OffenseTrait, on_delete=models.CASCADE, null=True, blank=True
    )
    language = models.CharField(max_length=100, default="Spanish")


class EvaluationSession(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class JokeEvaluation(models.Model):
    session = models.ForeignKey(
        EvaluationSession,
        on_delete=models.CASCADE,
        related_name="evaluations",
        default=uuid.uuid4,
    )
    joke = models.ForeignKey(Joke, on_delete=models.CASCADE)
    liked = models.BooleanField()


class JokometianRanking(models.Model):
    name = models.CharField(max_length=100, unique=True)
    score = models.IntegerField(default=0)
    image_url = models.CharField(max_length=100)

    class Meta:
        ordering = ["-score"]

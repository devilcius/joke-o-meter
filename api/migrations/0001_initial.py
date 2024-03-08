# Generated by Django 3.2.12 on 2024-02-29 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Jokes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("offense_degree", models.IntegerField()),
                (
                    "offense_type",
                    models.CharField(
                        choices=[
                            ("RACE", "Race"),
                            ("RELIGION", "Religion"),
                            ("ETHNICITY", "Ethnicity"),
                            ("GENDER", "Gender"),
                            ("SEXUAL_ORIENTATION", "Sexual Orientation"),
                            ("DISABILITY", "Disability"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Results",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("image", models.URLField()),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="JokesEvaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("positive", models.BooleanField()),
                (
                    "joke",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.jokes"
                    ),
                ),
            ],
        ),
    ]
# Generated by Django 3.2.12 on 2024-03-01 12:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_auto_20240301_1159"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name="jokesevaluation",
            name="session",
            field=models.ForeignKey(
                default=uuid.uuid4,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="evaluations",
                to="api.evaluationsession",
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="session",
            field=models.OneToOneField(
                default=uuid.uuid4,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="result",
                to="api.evaluationsession",
            ),
        ),
    ]

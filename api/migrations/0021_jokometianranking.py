# Generated by Django 3.2.12 on 2024-03-07 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_delete_jokometian"),
    ]

    operations = [
        migrations.CreateModel(
            name="JokometianRanking",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("score", models.IntegerField(default=0)),
                ("image_url", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["-score"],
            },
        ),
    ]

# Generated by Django 3.2.12 on 2024-02-29 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_jokes_offense_degree"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Jokes",
            new_name="Joke",
        ),
        migrations.RenameModel(
            old_name="Results",
            new_name="Result",
        ),
    ]

# Generated by Django 3.2.12 on 2024-03-06 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_auto_20240306_0856"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="joke",
            name="offense_degree",
        ),
        migrations.RemoveField(
            model_name="joke",
            name="offense_type",
        ),
    ]

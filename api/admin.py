from django.contrib import admin

from .models import Joke, JokeEvaluation

admin.site.register(Joke)
admin.site.register(JokeEvaluation)

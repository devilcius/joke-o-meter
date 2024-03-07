from django.contrib import admin

from .models import Joke, JokeEvaluation, JokometianRanking

admin.site.register(Joke)
admin.site.register(JokeEvaluation)
admin.site.register(JokometianRanking)

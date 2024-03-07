"""jokeometer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from api.views import (
    JokeListView,
    JokesEvaluationView,
    JokometianDetailView,
    JokometianRankingListView,
)
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configure the basic information for your Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Joke-O-Meter API",
        default_version="v1",
        description="API documentation for Joke-O-Meter",
        terms_of_service="https://jokometer.local/terms/",
        contact=openapi.Contact(email="contact@jokometer.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/jokes/", JokeListView.as_view(), name="joke-list"),
    path("api/evaluate-jokes/", JokesEvaluationView.as_view(), name="evaluate-jokes"),
    path(
        "api/jokometians/<uuid:uuid>/",
        JokometianDetailView.as_view(),
        name="jokometian-detail",
    ),
    path(
        "api/jokometian-rankings/",
        JokometianRankingListView.as_view(),
        name="jokometian_rankings",
    ),
    # URL patterns for the Swagger UI
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

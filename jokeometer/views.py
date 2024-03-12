import requests
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import re
from django.views import View
from api.models import JokeEvaluation
from api.jokometian_utils import create_jokometian_from_jokes_evaluation
from api.jokometian_traits import traits


class DynamicMetaView(View):

    def get(self, request, uuid, *args, **kwargs):
        # Try to get the crawlers list from cache
        crawlers = cache.get("crawlers_list")
        # If not in cache, fetch it and store it in cache
        if not crawlers:
            response = requests.get(
                "https://raw.githubusercontent.com/monperrus/crawler-user-agents/master/crawler-user-agents.json"
            )
            crawlers = response.json()
            # Cache the list for 24 hours (86400 seconds)
            cache.set("crawlers_list", crawlers, 86400)

        # Get the user agent of the incoming request
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # Check if the user agent matches any crawler patterns
        is_crawler = any(
            re.search(crawler["pattern"], user_agent, re.IGNORECASE)
            for crawler in crawlers
        )

        if is_crawler:
            # It's a bot, serve the SEO-optimized content
            evaluations = JokeEvaluation.objects.filter(session=uuid)
            if evaluations.exists():
                # Assuming create_jokometian_from_jokes_evaluation() and other necessary logic is implemented correctly
                jokometian = create_jokometian_from_jokes_evaluation(evaluations)
                jpg_image = re.sub(r"\.svg$", ".jpg", jokometian.image_url)
                # Absolute url
                absolute_url = request.build_absolute_uri()
                # Removes the trailing /share from the absolute url
                jokometian_url = re.sub(r"/share$", "", absolute_url)
                jokometian_info = traits.get(jokometian.name, None)
                context = {
                    "og_title": jokometian_info.get("name", "Jokometian"),
                    "og_description": jokometian.description,
                    "og_image": request.build_absolute_uri(jpg_image),
                    "og_url": jokometian_url,
                }
                return render(request, "jokeometer/dynamic_index.html", context)
            else:
                return HttpResponse(status=404)
        else:
            # It's not a bot, remove '/share' from the request path and redirect
            redirect_url = request.path_info.rsplit("/share", 1)[0]
            return HttpResponseRedirect(redirect_url)

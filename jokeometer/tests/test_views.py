from django.test import TestCase
from api.models import JokeEvaluation, EvaluationSession, Joke, OffenseTrait
from unittest.mock import patch
import json

MOCK_CRAWLER_USER_AGENTS = json.dumps(
    [
        {"pattern": "Googlebot/", "url": "http://www.google.com/bot.html"},
        {"pattern": "bingbot/", "url": "http://www.bing.com/bot.htm"},
    ]
)


class DynamicMetaViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create an EvaluationSession instance
        cls.session = EvaluationSession.objects.create()
        offense_trait = OffenseTrait.objects.create(name=OffenseTrait.RACE, degree=10)

        joke = Joke.objects.create(
            content="Why did the chicken cross the road?",
            trait=offense_trait,
            language="English",
        )
        JokeEvaluation.objects.create(joke=joke, liked=True, session=cls.session)

    @patch("requests.get")
    def test_seo_optimized_content_for_bots(self, mock_get):

        # Mock the response from requests.get to return our mock crawler list
        mock_get.return_value.json.return_value = json.loads(MOCK_CRAWLER_USER_AGENTS)

        # Use a bot's user agent
        bot_user_agent = (
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        )
        response = self.client.get(
            f"/jokometian/{self.session.id}/share", HTTP_USER_AGENT=bot_user_agent
        )
        # Check that the SEO-optimized template was used
        self.assertTemplateUsed(response, "jokeometer/dynamic_index.html")
        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    @patch("requests.get")
    def test_redirect_for_regular_browsers(self, mock_get):
        # Mock setup as above
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = json.loads(MOCK_CRAWLER_USER_AGENTS)

        # Use a typical browser's user agent
        browser_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        response = self.client.get(
            f"/jokometian/{self.session.id}/share", HTTP_USER_AGENT=browser_user_agent
        )

        # Assert that a redirection occurs
        self.assertEqual(response.status_code, 302)

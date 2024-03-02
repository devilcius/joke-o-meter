from openai import OpenAI
from django.core.management.base import BaseCommand
from api.models import Joke
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()


class Command(BaseCommand):
    help = "Fill sentiment fields in the Joke model"

    def handle(self, *args, **kwargs):
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            api_key=openai_api_key
        )
        self.stdout.write("Starting the process...")
        self.fill_sentiment_fields()
        self.stdout.write("Process completed.")

    def fill_sentiment_fields(self):
        jokes = Joke.objects.filter(offense_type__isnull=True)
        for joke in jokes:
            self.stdout.write(f"Processing joke {joke.id}")
            self.fill_sentimient_fields_for_joke(joke)
            self.stdout.write(f"Joke {joke.id} processed")
            # sleep half a second to avoid getting blocked
            time.sleep(0.5)

    def fill_sentimient_fields_for_joke(self, joke):
        # Create the messages to send to the API
        messages = [
            {
                "role": "system",
                "content": f"""
                        You will act as a sentiment analyst specializing in identifying potentially offensive content in jokes. Upon receiving a {joke.language} joke, analyze its content and generate a response in JSON format. This response should contain two key properties: offense_degree and offense_type.

                        1. offense_degree: Assign an integer value from 1 to 10, where 1 represents the least offensive and 10 represents the most offensive content.

                        2. offense_type: Determine the category of offense, if any, from the following list:
                        - RACE
                        - RELIGION
                        - ETHNICITY
                        - GENDER
                        - SEXUAL_ORIENTATION
                        - DISABILITY
                        - GENERIC_VIOLENCE
                        - NO_OFFENSE_FOUND (use this if the joke is not offensive in any category)

                        Please ensure accuracy and sensitivity in your analysis, considering the context and nuances of the joke. Use GENERIC_VIOLENCE as last resort, only in case no other category applies.

                        Example Joke (don't use it): "Why did the chicken cross the road? To get to the other side!"

                        Expected Response Format:

                        {{
                        "offense_degree": "integer_value",
                        "offense_type": "category"
                        }}

                        Note: The response should strictly adhere to the JSON format for compatibility with downstream applications. Every value must be enclosed in double quotes. Just pass the json without formatting!
                """
            },
            {
                "role": "user",
                "content": f"Joke: {joke.content}",
            },
        ]
        # Generate the sentiment
        degree, type = self.generate_sentimient(messages)
        # Save the joke
        joke.offense_degree = degree
        joke.offense_type = type
        joke.save()

    def generate_sentimient(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.3,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\\n"],
        )
        response = response.choices[0].message.content
        # Load response as JSON
        try:
            # Make sure the every values are quoted
            response = json.loads(response)
            return response["offense_degree"], response["offense_type"]
        except:
            print(response)
            raise ValueError("The response is not in the expected format")

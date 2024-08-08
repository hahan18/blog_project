import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Google Cloud Natural Language API endpoint for sentiment analysis
GOOGLE_NLP_API_URL = "https://language.googleapis.com/v1/documents:analyzeSentiment"

# Retrieve the API key from environment variables
API_KEY = os.getenv('GOOGLE_API_KEY')


def moderate_content(text):
    try:
        # Set up the request payload
        payload = {
            "document": {
                "type": "PLAIN_TEXT",
                "content": text
            },
            "encodingType": "UTF8"
        }

        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Construct the full URL with the API key
        url = f"{GOOGLE_NLP_API_URL}?key={API_KEY}"

        # Send the request to the Google API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        result = response.json()

        # Analyze the sentiment score and magnitude
        sentiment = result['documentSentiment']

        # Define thresholds for determining if content is inappropriate
        if sentiment['score'] < -0.5 and sentiment['magnitude'] > 0.5:
            return True  # Content is likely to be inappropriate

    except requests.exceptions.RequestException as e:
        print(f"Error calling Google AI API: {e}")
        if response:
            print(f"Response content: {response.content}")

    # Return False if not flagged as inappropriate or if there's an error
    return False

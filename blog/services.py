import requests

GOOGLE_AI_API_URL = "https://api.google.dev/language/v1beta2/documents:analyzeSyntax"


def moderate_content(text):
    # Call Google AI API to check for inappropriate content
    response = requests.post(GOOGLE_AI_API_URL, json={"document": {"type": "PLAIN_TEXT", "content": text}})

    if response.status_code == 200:
        result = response.json()
        # Example logic: Assume the API returns a field 'inappropriate'
        if result.get("inappropriate", False):
            return True  # Content is inappropriate

    # Return False if not flagged as inappropriate
    return False

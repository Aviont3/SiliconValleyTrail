"""Module for interacting with Google's Generative AI API to fetch news content."""

import os
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Create client with API key
client = genai.Client(api_key=api_key)


try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Explain how AI works in a few words",
    )
    print(response.text)
except Exception as exc:
    print("Failed to generate content:", exc)
    raise
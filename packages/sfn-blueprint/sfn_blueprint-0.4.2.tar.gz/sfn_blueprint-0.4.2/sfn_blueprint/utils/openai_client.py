from openai import OpenAI
from dotenv import load_dotenv
import os

def SFNOpenAIClient():
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    return client
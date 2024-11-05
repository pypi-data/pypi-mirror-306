import os
from openai import OpenAI
from dotenv import load_dotenv
from .openai_cost_calculation import openai_cost_calculation

class sfn_openai_completions():
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

        self.client = OpenAI(api_key=api_key)

    def execute_api_call(self, model, configuration):
        """
        Execute API call to OpenAI using the provided model and configuration.
        
        Args:
            model (str): The model ID to use (e.g., "gpt-3.5-turbo").
            configuration (dict): A dictionary containing API call configuration such as 'messages', 'temperature', 'max_tokens'.

        Returns:
            response (dict): The API response object from OpenAI.
        """
        response = self.client.chat.completion.create(
            model=model,
            messages=configuration["messages"],
            temperature=configuration.get("temperature", 0.7),
            max_tokens=configuration.get("max_tokens", 1000),
        )

        token_consumption_dict = openai_cost_calculation(
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            model="gpt-3.5-turbo-0125",
        )
        print('-----------------token_consumption_dict',token_consumption_dict)
        return response

import os
from typing import List, Dict, Any
import pandas as pd
from .base_agent import SFNAgent
from sfn_blueprint.tasks.task import Task
from sfn_blueprint.utils.prompt_manager import SFNPromptManager
from sfn_blueprint.config.model_config import MODEL_CONFIG
from sfn_blueprint.utils.openai_client import SFNOpenAIClient

class SFNSuggestionsGeneratorAgent(SFNAgent):
    def __init__(self):
        super().__init__(name="Suggestions Generator", role="Generic Suggestions Generator")
        self.client = SFNOpenAIClient()
        print('temp1>>>', MODEL_CONFIG["suggestions_generator"])
        self.model_config = MODEL_CONFIG["suggestions_generator"]
        self.prompt_manager = SFNPromptManager()  # Rename this in model_config.py

    def execute_task(self, task: Task, llm_provider='openai') -> List[str]:
        """
        Execute the suggestion generation task.
        
        :param task: Task object containing the data, task_type and category
        :return: List of suggestions
        """
        if not isinstance(task.data, dict) or 'df' not in task.data:
            raise ValueError("Task data must be a dictionary containing 'df' key")

        df = task.data['df']
        task_type = task.task_type or 'feature_suggestion'  # Default to feature suggestions
        category = task.category
        
        columns = df.columns.tolist()
        sample_records = df.head(3).to_dict(orient='records')
        describe_dict = df.describe().to_dict()

        suggestions = self._generate_suggestions(
            columns=columns,
            sample_records=sample_records,
            describe_dict=describe_dict,
            task_type=task_type,
            category=category,
            llm_provider=llm_provider
        )
        return suggestions

    def _generate_suggestions(self, columns: List[str], sample_records: List[Dict[str, Any]], 
                            describe_dict: Dict[str, Dict[str, float]], 
                            task_type: str,
                            category: str,
                            llm_provider: str) -> List[str]:
        """
        Generate suggestions based on the data, task type and category.
        """
        system_prompt, user_prompt = self.prompt_manager.get_prompt(
            agent_type='suggestions_generator',
            llm_provider=llm_provider,
            columns=columns,
            sample_records=sample_records,
            describe_dict=describe_dict,
            task_type=task_type,
            category=category
        )
        
        response = self.client.chat.completions.create(
            model=self.model_config[llm_provider]["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.model_config[llm_provider]["temperature"],
            max_tokens=self.model_config[llm_provider]["max_tokens"]
        )

        suggestions_text = response.choices[0].message.content.strip()
        return self._parse_suggestions(suggestions_text)
    
    
    def _parse_suggestions(self, suggestions_text: str) -> List[str]:
        """
        Parse the suggestions text into a list of individual suggestions.
        
        :param suggestions_text: Raw text of suggestions from the OpenAI model
        :return: List of individual suggestions
        """
        # Split the text by newlines and remove any empty lines
        suggestions = [line.strip() for line in suggestions_text.split('\n') if line.strip()]
        
        # Remove numbering from each suggestion
        suggestions = [suggestion.split('. ', 1)[-1] for suggestion in suggestions]
        
        return suggestions
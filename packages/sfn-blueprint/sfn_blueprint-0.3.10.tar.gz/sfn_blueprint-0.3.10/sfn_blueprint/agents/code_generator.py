import os
import pandas as pd
from .base_agent import SFNAgent
import re
from sfn_blueprint.utils.prompt_manager import SFNPromptManager
from sfn_blueprint.config.model_config import MODEL_CONFIG
from sfn_blueprint.utils.llm_handler.llm_handler import SFNAIHandler 
class SFNFeatureCodeGeneratorAgent(SFNAgent):
    def __init__(self):
        super().__init__(name="Feature Code Generator", role="Python Developer")
        self.model_config = MODEL_CONFIG["code_generator"]
        parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        prompt_config_path = os.path.join(parent_path, 'config', 'prompts_config.json')
        self.prompt_manager = SFNPromptManager(prompt_config_path)
        self.ai_handler = SFNAIHandler()  # Initialize the handler

    def execute_task(self, task, llm_provider='openai', error_message=None) -> str:
        # Prepare kwargs for prompt
        prompt_kwargs = {
            'suggestion': task.data['suggestion'],
            'columns': task.data['columns'],
            'dtypes': task.data['dtypes'],
            'sample_records': task.data['sample_records'],
            'error_message': error_message
        }
        
        # Get both system and user prompts using SFNPromptManager
        system_prompt, user_prompt = self.prompt_manager.get_prompt(
            agent_type='code_generator',
            llm_provider=llm_provider,
            sfn_blueprint_prompt = True, 
            **prompt_kwargs
        )

        # Route to the correct LLM client via the handler
        configuration = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.model_config[llm_provider]["temperature"],
            "max_tokens": self.model_config[llm_provider]["max_tokens"]
        }

        response = self.ai_handler.route_to(llm_provider, self.model_config[llm_provider]["model"], configuration)
        
        code = response.choices[0].message.content.strip()
        return self.clean_generated_code(code)
    
    @staticmethod
    def clean_generated_code(code: str) -> str:
        code = re.sub(r'```python\n|```', '', code)
        code = re.sub(r'print\(.*\)\n?', '', code)
        code = re.sub(r'#.*\n', '', code)
        code = '\n'.join(line for line in code.split('\n') if line.strip())
        print('>>code cleaned..', code)
        return code
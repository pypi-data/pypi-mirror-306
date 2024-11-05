import os
import json
from typing import Dict, Tuple

class SFNPromptManager:
    def __init__(self, prompts_config_path: str = "sfn_blueprint/config/prompts_config.json"):
        try:
            self.prompts_config = self._load_prompts_config(prompts_config_path)
            print(f"Prompt Manager initialized with config from: {prompts_config_path}")
            print(f"Loaded prompt config: {self.prompts_config}")
        except Exception as e:
            print(f"Failed to initialize Prompt Manager: {str(e)}")
            raise RuntimeError(f"Prompt Manager initialization failed: {str(e)}") from e

    def _load_prompts_config(self, path: str) -> Dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Prompts config file not found at: {path}")
            
        try:
            with open(path, 'r') as f:
                config = json.load(f)
            if not isinstance(config, dict):
                raise ValueError("Config file must contain a JSON object")
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading prompts config: {str(e)}")    

    def get_prompt(self, agent_type: str, llm_provider: str, **kwargs) -> Tuple[str, str]:
        """
        Get formatted prompts for specific agent and LLM provider
        
        Args:
            agent_type: Type of agent (e.g., 'feature_suggester', 'code_generator')
            llm_provider: LLM provider (e.g., 'openai', 'anthropic')
            **kwargs: Variables for formatting the prompt template
            
        Returns:
            Tuple[str, str]: (system_prompt, formatted_user_prompt)
        """
        print("3>>>", self.prompts_config)
        if agent_type not in self.prompts_config:
            raise ValueError(f"Unknown agent type: {agent_type}")
            
        if llm_provider not in self.prompts_config[agent_type]:
            raise ValueError(f"Unknown LLM provider: {llm_provider}")

        prompts = self.prompts_config[agent_type][llm_provider]
        system_prompt = prompts["system_prompt"]
        user_prompt = prompts["user_prompt_template"].format(**kwargs)
        
        return system_prompt, user_prompt
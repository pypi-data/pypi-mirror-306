import os
from typing import Dict, Any, Tuple, List
from sfn_blueprint.utils.prompt_manager import SFNPromptManager

def get_code_generator_prompt(llm_provider: str = "openai", **kwargs) -> Tuple[str, str]:
    """
    Generate prompts for feature engineering code generation.
    
    Required kwargs:
    - suggestion: str
    - columns: list
    - dtypes: dict
    - sample_records: list
    - error_message: str (optional)
    
    Returns:
        Tuple[str, str]: (system_prompt, formatted_user_prompt)
    """
    # Input validation
    required_fields = {
        'suggestion': str,
        'columns': list,
        'dtypes': dict,
        'sample_records': list
    }
    
    for field, expected_type in required_fields.items():
        if field not in kwargs:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(kwargs[field], expected_type):
            raise TypeError(f"Field {field} must be of type {expected_type.__name__}")
    
    # Validate non-empty inputs
    if not kwargs['columns']:
        raise ValueError("Columns list cannot be empty")
    if not kwargs['sample_records']:
        raise ValueError("Sample records cannot be empty")
    if not kwargs['suggestion'].strip():
        raise ValueError("Suggestion cannot be empty")
    
    # Preprocess inputs into required format
    processed_kwargs = {
        'suggestion': kwargs['suggestion'],
        'columns': ", ".join(str(col) for col in kwargs['columns']),
        'dtypes': _format_dtypes(kwargs['dtypes']),
        'sample_records': _format_sample_records(kwargs['sample_records'][:3])  # Limit to 3 samples
    }
    
    # Get prompts from PromptManager
    parent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    prompt_config_path = os.path.join(parent_path, 'config', 'prompts_config.json')
    prompt_manager = SFNPromptManager(prompt_config_path)  
    system_prompt, user_prompt = prompt_manager.get_prompt("code_generator", llm_provider, **processed_kwargs)
    
    # Add error message if present
    if error_msg := kwargs.get('error_message'):
        user_prompt += f"\n\nThe previous code failed: {error_msg}\nPlease fix it."
    
    return system_prompt, user_prompt

def _format_dtypes(dtypes: Dict[str, Any]) -> str:
    """Format the dtypes dictionary in a readable format."""
    return "\n".join(f"{col}: {dtype}" for col, dtype in dtypes.items())

def _format_sample_records(records: List[Dict[str, Any]]) -> str:
    """Format sample records in a readable format."""
    return "\n".join(str(record) for record in records)
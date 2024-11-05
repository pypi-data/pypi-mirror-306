MODEL_CONFIG = {
  "code_generator": {
    "openai": {
      "model": "gpt-3.5-turbo",
      "temperature": 0.7,
      "max_tokens": 500
    },
    "anthropic": {
      "model": "claude-3-5-sonnet-20240620",
      "temperature": 0.7,
      "max_tokens": 500
    }
  },
  "suggestions_generator": {
    "openai": {
      "model": "gpt-3.5-turbo",
      "temperature": 0.7,
      "max_tokens": 1000
    },
    "anthropic": {
      "model": "claude-3-5-sonnet-20240620",
      "temperature": 0.7,
      "max_tokens": 1000
    }
  }
}

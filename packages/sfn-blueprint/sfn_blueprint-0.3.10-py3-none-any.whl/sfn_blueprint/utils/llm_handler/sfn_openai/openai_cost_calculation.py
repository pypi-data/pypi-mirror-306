def openai_cost_calculation(
    total_prompt_tokens, total_completion_tokens, model="gpt-3.5-turbo-0125"
):
    # pricing for 1k tokens
    pricing = {
        "gpt-3.5-turbo-0125": {
            "prompt": 0.0005,
            "completion": 0.0015,
        },
        "gpt-3.5-turbo-16k": {
            "prompt": 0.003,
            "completion": 0.004,
        },
        "gpt-4-8k": {
            "prompt": 0.03,
            "completion": 0.06,
        },
        "gpt-4-32k": {
            "prompt": 0.06,
            "completion": 0.12,
        },
        "gpt-4o": {
            "prompt": 0.005,
            "completion": 0.015,
        },
        "text-embedding-ada-002-v2": {
            "prompt": 0.0001,
            "completion": 0.0001,
        },
    }

    try:
        model_pricing = pricing[model]
    except KeyError:
        raise ValueError("Invalid model specified")

    prompt_cost = total_prompt_tokens * model_pricing["prompt"] / 1000
    completion_cost = total_completion_tokens * model_pricing["completion"] / 1000
    total_tokens = total_prompt_tokens + total_completion_tokens
    total_cost_usd = prompt_cost + completion_cost

    token_consumption_dict = {
        "prompt_tokens": total_prompt_tokens,
        "completion_tokens": total_completion_tokens,
        "total_tokens": total_tokens,
        "total_Cost_usd": round(total_cost_usd, 4),
    }
    return token_consumption_dict

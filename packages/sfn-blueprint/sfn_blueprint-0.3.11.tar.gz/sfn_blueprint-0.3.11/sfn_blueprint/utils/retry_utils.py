from typing import Callable, Any
import logging
from functools import wraps

def with_retry(
    max_attempts: int = 3,
    logger: logging.Logger = None
) -> Callable:
    """
    Simple retry decorator that retries a function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        logger: Logger instance for logging retry attempts
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        if logger:
                            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                        continue
                    raise
            return None
        return wrapper
    return decorator
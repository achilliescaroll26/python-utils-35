import functools
import logging
from typing import Callable, Any, Type, Union

logger = logging.getLogger(__name__)

def resilient_execution(default_value: Any = None, exceptions: Union[Type[Exception], tuple] = (Exception,)):
    """Decorator for graceful failure handling using functional trapping."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                logger.error(f"caught {type(e).__name__} in {func.__name__}: {e}")
                return default_value
        return wrapper
    return decorator

def safe_dict_get(data: dict, path: str, default: Any = None):
    """Deep key retrieval with path-based traversal and fallback."""
    keys = path.split('.')
    try:
        current = data
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError, AttributeError):
        return default

class EdgeCaseHandler:
    """Context manager for suppressing specific execution edge cases."""
    def __init__(self, suppress: Union[Type[Exception], tuple] = Exception):
        self.suppress = suppress

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.suppress):
            return True
        return False
import functools
import logging
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

logger = logging.getLogger(__name__)

def resilient_wrapper(default: Any = None) -> Callable[[Callable[P, R]], Callable[P, Any]]:
    def decorator(func: Callable[P, R]) -> Callable[P, Any]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, AttributeError) as e:
                logger.error(f'Edge case caught in {func.__name__}: {e}')
                return default
            except Exception as e:
                logger.critical(f'Unexpected runtime failure: {e}')
                raise
        return wrapper
    return decorator

@resilient_wrapper(default=0)
def safe_division(numerator: Any, denominator: Any) -> float:
    return float(numerator) / float(denominator)

@resilient_wrapper(default=[])
def extract_first_element(data: Any) -> Any:
    return list(data)[0]

class DataSanitizer:
    @staticmethod
    def strip_and_lower(value: Any) -> str:
        if not isinstance(value, str):
            return str(value).strip().lower() if value is not None else ''
        return value.strip().lower()
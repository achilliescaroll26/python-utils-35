import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)

class ExecutionContext:
    def __init__(self, name: str):
        self.name = name
        self.start = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start
        logger.info(f"context {self.name} finished in {duration:.4f}s")

def silent_retry(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def compose(*funcs: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), funcs)

def memoize_path(func: Callable) -> Callable:
    cache = {}
    @functools.wraps(func)
    def memoizer(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memoizer
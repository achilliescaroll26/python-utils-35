import functools
import time
import logging

logger = logging.getLogger(__name__)

def memoize_with_expiry(expiration):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < expiration:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def batch_iterable(iterable, size):
    iterator = iter(iterable)
    while True:
        batch = [item for _, item in zip(range(size), iterator)]
        if not batch:
            break
        yield batch

def safe_get(nested_dict, *keys, default=None):
    current = nested_dict
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

class DynamicNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        items = f"{k}={v!r}" for k, v in self.__dict__.items()
        return f"DynamicNamespace({', '.join(items)})"

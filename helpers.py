import functools
import time
import itertools

def deep_flatten(nested_iterable):
    for item in nested_iterable:
        if isinstance(item, (list, tuple, set)):
            yield from deep_flatten(item)
        else:
            yield item

def retry_execution(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def batch_process(iterable, size):
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, size))
        if not batch:
            break
        yield batch

def memoize_with_expiry(timeout=300):
    cache = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args][1]) < timeout:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def identity_map(items, key_func=lambda x: x):
    return {key_func(x): x for x in items}
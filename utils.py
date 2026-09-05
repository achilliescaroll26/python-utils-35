import functools
import time
import itertools

def compose(*funcs):
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)

def memoize_with_expiry(seconds):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args][1]) < seconds:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def chunker(iterable, size):
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, size)), ())

def flatten(nested_list):
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator
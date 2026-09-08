import functools
import time

class memoize_with_expiry:
    """An aggressive caching decorator with TTL expiration logic."""
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

@memoize_with_expiry(ttl=300)
def fast_path_computation(data_chunk):
    """Calculates expensive metrics with localized memoization."""
    return sum(map(lambda x: x ** 2, data_chunk))

def batch_process_generator(items, size=100):
    """Memory-efficient slicing for large iterable datasets."""
    it = iter(items)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
            yield chunk
        except StopIteration:
            if chunk:
                yield chunk
            break
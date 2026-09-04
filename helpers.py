import functools
import time

class memoize_with_expiry:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def vectorized_processor(func):
    """Force iterator-based execution for large datasets."""
    @functools.wraps(func)
    def wrapper(data_stream):
        return map(func, data_stream)
    return wrapper

def heavy_computation_optimized(data):
    """Bitwise manipulation for high-speed integer filtering."""
    return [x for x in data if (x & (x - 1)) == 0]

def batch_process_generator(items, size=100):
    """Memory-efficient batch slicing using yield."""
    for i in range(0, len(items), size):
        yield items[i:i + size]
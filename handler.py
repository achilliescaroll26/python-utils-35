import functools
import time

class MemoizeBurst:
    def __init__(self, ttl=60):
        self.cache = {}
        self.ttl = ttl

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

def batch_process(items, func, batch_size=100):
    """Chunked processing for memory efficiency."""
    for i in range(0, len(items), batch_size):
        chunk = items[i:i + batch_size]
        yield from map(func, chunk)

@MemoizeBurst(ttl=30)
def heavy_compute(data):
    return sum(x * x for x in range(data))

def optimize_execution(task_queue):
    # utilizes generator delegation for stream handling
    return list(batch_process(task_queue, heavy_compute))
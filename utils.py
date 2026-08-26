import time
import functools

def retry_operation(retries=3, delay=1, backoff=2):
    """Decorator implementing exponential backoff for network operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= retries:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

class NetworkSimulator:
    def __init__(self, fail_times=2):
        self.fail_times = fail_times
        self.calls = 0

    @retry_operation(retries=3, delay=0.1)
    def unstable_request(self):
        self.calls += 1
        if self.calls <= self.fail_times:
            raise ConnectionError("Temporary network glitch")
        return "success"

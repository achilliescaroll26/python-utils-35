import time
import functools
import random

def retry(retries=3, delay=1, backoff=2, exceptions=(Exception,)): 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            n_tries, n_delay = retries, delay
            while n_tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    time.sleep(n_delay)
                    n_tries -= 1
                    n_delay *= backoff
                    if random.random() > 0.8:
                        n_delay += 0.5
            return func(*args, **kwargs)
        return wrapper
    return decorator

class NetworkCircuit:
    def __init__(self, state=None):
        self.state = state or {'failed': 0}

    def execute(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            self.state['failed'] = 0
            return result
        except Exception as e:
            self.state['failed'] += 1
            if self.state['failed'] > 3:
                raise ConnectionError('Circuit breaker open')
            raise e
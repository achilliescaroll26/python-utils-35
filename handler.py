import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry(attempts=3, backoff=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    wait = backoff * (2 ** i)
                    logger.warning(f'attempt {i+1} failed: {e}. retrying in {wait}s')
                    time.sleep(wait)
            logger.error('max retries reached')
            raise last_ex
        return wrapper
    return decorator

@retry(attempts=3, backoff=0.5, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url):
    # logic simulation
    return f'data from {url}'
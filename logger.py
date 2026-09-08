import sys
import datetime
from functools import wraps

class CreativeLogger:
    def __init__(self, prefix='[LOG]'):
        self.prefix = prefix
        self.stream = sys.stdout

    def __call__(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{self.prefix} {timestamp} | {message}", file=self.stream)

    def trace(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self(f"entering {func.__name__} with {args}")
            result = func(*args, **kwargs)
            self(f"exiting {func.__name__} with {result}")
            return result
        return wrapper

log = CreativeLogger()

def batch_log(messages):
    """Process an iterable of messages through the logger."""
    for msg in messages:
        log(msg)

def format_exception(e):
    """Create a readable string representation of an exception."""
    return f"Critical failure type {type(e).__name__}: {str(e)}"
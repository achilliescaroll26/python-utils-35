import sys
import time
import functools

class EnhancedLogger:
    def __init__(self, prefix='[LOG]'):
        self.prefix = prefix

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            self.emit(f'{func.__name__} executed in {end - start:.4f}s')
            return result
        return wrapper

    def emit(self, message):
        sys.stdout.write(f'{self.prefix} {time.strftime("%H:%M:%S")} -> {message}\n')
        sys.stdout.flush()

def get_logger(name):
    """Factory for quirky functional logging."""
    logger = EnhancedLogger(f'[{name.upper()}]')
    def log_info(msg):
        logger.emit(msg)
    return log_info

def silent_error_wrapper(fallback):
    """Decorator for swallowing errors with style."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sys.stderr.write(f'Suppressed error: {e}\n')
                return fallback
        return wrapper
    return decorator
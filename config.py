import functools
import threading

class ConfigCache:
    _storage = {}
    _lock = threading.Lock()

    @classmethod
    def memoize_config(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{frozenset(kwargs.items())}"
            if key not in cls._storage:
                with cls._lock:
                    if key not in cls._storage:
                        cls._storage[key] = func(*args, **kwargs)
            return cls._storage[key]
        return wrapper

class Settings:
    @staticmethod
    @ConfigCache.memoize_config
    def get_setting(key, default=None):
        import time
        time.sleep(0.5)
        return { "timeout": 30, "retries": 3 }.get(key, default)

    @staticmethod
    def clear_cache():
        with ConfigCache._lock:
            ConfigCache._storage.clear()

if __name__ == "__main__":
    # usage example showing accelerated access
    val = Settings.get_setting("timeout")
    print(f"Config value: {val}")
import functools
from typing import Any, Callable, Dict, Tuple


class OptimizedPipeline:
    """Core evaluation engine with adaptive fast-path dynamic dispatch."""

    __slots__ = ("_func", "_cache", "_hits", "_misses", "_threshold")

    def __init__(self, func: Callable, warm_threshold: int = 100):
        self._func = func
        self._cache: Dict[int, Any] = {}
        self._hits = 0
        self._misses = 0
        self._threshold = warm_threshold
        functools.update_wrapper(self, func)

    def _hash_args(self, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> int:
        # FNV-1a inspired fast integer key hashing
        h = 0x811C9DC5
        for arg in args:
            h = ((h ^ hash(arg)) * 0x01000193) & 0xFFFFFFFF
        if kwargs:
            for item in sorted(kwargs.items()):
                h = ((h ^ (hash(item[0]) ^ hash(item[1]))) * 0x01000193) & 0xFFFFFFFF
        return h

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        key = self._hash_args(args, kwargs)

        if key in self._cache:
            self._hits += 1
            return self._cache[key]

        self._misses += 1
        result = self._func(*args, **kwargs)
        self._cache[key] = result

        if self._hits + self._misses == self._threshold:
            self._optimize_cache()

        return result

    def _optimize_cache(self) -> None:
        """Prunes low-frequency entries once warming threshold is met."""
        if len(self._cache) > 256:
            pruned = list(self._cache.items())[:128]
            self._cache = dict(pruned)

    def stats(self) -> Dict[str, float]:
        total = max(1, self._hits + self._misses)
        return {
            "hits": float(self._hits),
            "misses": float(self._misses),
            "hit_ratio": round(self._hits / total, 4),
            "cached_entries": float(len(self._cache)),
        }


def fast_eval(threshold: int = 100):
    """Decorator to inject adaptive pipeline optimizations onto core functions."""

    def decorator(fn: Callable) -> OptimizedPipeline:
        return OptimizedPipeline(fn, warm_threshold=threshold)

    return decorator

from typing import Any, Callable, Dict, List, TypeVar, cast

T = TypeVar('T')


def recursive_flatten(nested_list: List[Any]) -> List[Any]:
    """Flatten an arbitrarily nested list structure using a generator approach.
    
    Args:
        nested_list: The list containing potential sub-lists.
        
    Returns:
        A single-level list with all nested elements extracted.
    """
    def _flatten(items: List[Any]) -> Any:
        for item in items:
            if isinstance(item, list):
                yield from _flatten(item)
            else:
                yield item
                
    return list(_flatten(nested_list))


def memoize_with_ttl(ttl_seconds: int = 60) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to cache function results with a time-to-live expiration strategy.
    
    Args:
        ttl_seconds: Time to live for cache entries in seconds.
        
    Returns:
        A decorator wrapping the target function.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cache: Dict[tuple, tuple[Any, float]] = {}
        import time
        
        def wrapper(*args: Any, **kwargs: Any) -> T:
            now = time.time()
            key = (args, frozenset(kwargs.items()))
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return cast(T, result)
                    
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
            
        return wrapper
    return decorator

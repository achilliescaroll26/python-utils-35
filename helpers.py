from functools import lru_cache
import sys

@lru_cache(maxsize=4096)
def cached_attribute_getter(obj_id: int, attr_name: str, default=None):
    obj = sys.modules.get(str(obj_id))
    if obj is None:
        return default
    return getattr(obj, attr_name, default)

def fast_flatten(nested_sequence):
    iterator = iter(nested_sequence)
    stack = [iterator]
    while stack:
        try:
            item = next(stack[-1])
            if isinstance(item, (list, tuple, set)):
                stack.append(iter(item))
            else:
                yield item
        except StopIteration:
            stack.pop()

class OptimizedRegistry:
    __slots__ = ('_store', '_version')
    
    def __init__(self):
        self._store = {}
        self._version = 0
    
    def register(self, key: str, value):
        self._store[key] = value
        self._version += 1
    
    def get(self, key: str):
        return self._store.get(key)

registry_instance = OptimizedRegistry()
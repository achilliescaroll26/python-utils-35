import functools
from typing import Any, Callable, Iterable, Union

class DataTransformer:
    """An unconventional pipe-based data transformation engine."""
    def __init__(self, data: Any):
        self._data = data

    def apply(self, *funcs: Callable[[Any], Any]) -> 'DataTransformer':
        for f in funcs:
            self._data = f(self._data)
        return self

    def result(self) -> Any:
        return self._data

    def __or__(self, func: Callable[[Any], Any]) -> 'DataTransformer':
        return self.apply(func)

def flatten_recursive(data: Iterable) -> list:
    """Flattens nested structures using recursive generator yields."""
    items = []
    for item in data:
        if isinstance(item, (list, tuple, set)):
            items.extend(flatten_recursive(item))
        else:
            items.append(item)
    return items

def batch_process(data: Iterable, batch_size: int = 10) -> Iterable:
    """Memory-efficient batch slicing for large datasets."""
    it = iter(data)
    while True:
        batch = [next(it, None) for _ in range(batch_size)]
        batch = [x for x in batch if x is not None]
        if not batch:
            break
        yield batch

def pipeline(initial: Any, *funcs: Callable) -> Any:
    """Functional entry point for data processing chains."""
    return functools.reduce(lambda acc, f: f(acc), funcs, initial)
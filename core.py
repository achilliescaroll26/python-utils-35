from typing import TypeVar, Callable, Any, Iterable

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Chain multiple functions together into a single pipeline."""
    def pipeline(data: Any) -> Any:
        for func in functions:
            data = func(data)
        return data
    return pipeline

def batcher(iterable: Iterable[T], size: int) -> Iterable[list[T]]:
    """Split an iterable into chunks of fixed size using slice logic."""
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
            yield chunk
        except StopIteration:
            if chunk:
                yield chunk
            break

class Registry(dict):
    """An unusual dict wrapper that auto-registers missing keys via factory."""
    def __init__(self, factory: Callable[[], Any]):
        super().__init__()
        self._factory = factory

    def __missing__(self, key: Any) -> Any:
        value = self._factory()
        self[key] = value
        return value

def identity(x: T) -> T:
    """Pass-through function for functional chains."""
    return x
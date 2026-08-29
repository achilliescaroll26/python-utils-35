import string
import functools
from typing import Any, Callable, List, Dict

class HelperRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable[[Any], Any]) -> None:
        self._registry[name] = func

    def retrieve(self, name: str) -> Callable[[Any], Any]:
        if name not in self._registry:
            raise KeyError(f"Helper '{name}' not registered")
        return self._registry[name]

    def execute(self, name: str, *args: Any, **kwargs: Any) -> Any:
        func = self.retrieve(name)
        return func(*args, **kwargs)

registry = HelperRegistry()

def _strip_lower(text: str) -> str:
    return text.strip().lower()

def _remove_punct(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))

def _count_tokens(text: str) -> int:
    return len(text.split())

registry.register("clean_text", lambda t: functools.reduce(lambda acc, f: f(acc), [_strip_lower, _remove_punct], t))
registry.register("token_count", _count_tokens)

def apply_cleanups(data: str, ops: List[str]) -> Any:
    result = data
    for op_name in ops:
        func = registry.retrieve(op_name)
        result = func(result)
    return result

def batch_process(items: List[Any], func: Callable[[Any], Any]) -> List[Any]:
    return [func(item) for item in items]

def invert_mapping(mapping: Dict[Any, Any]) -> Dict[Any, Any]:
    return {value: key for key, value in mapping.items()}

def safe_operation(op: Callable[[Any, Any], Any], a: Any, b: Any, default: Any = None) -> Any:
    try:
        return op(a, b)
    except Exception:
        return default

def deduplicate(seq: List[Any]) -> List[Any]:
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def nested_flatten(nested: List[Any]) -> List[Any]:
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(nested_flatten(item))
        else:
            flat.append(item)
    return flat
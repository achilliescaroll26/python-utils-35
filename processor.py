from typing import Any, Callable, Generator, Iterable


class InputFilter:
    """Validation pipe utilizing custom reverse bitwise OR operator."""
    def __init__(self, *predicates: Callable[[Any], bool]):
        self.predicates = predicates

    def __ror__(self, data_stream: Iterable[Any]) -> Generator[tuple[bool, Any, str], None, None]:
        for item in data_stream:
            for pred in self.predicates:
                try:
                    if not pred(item):
                        yield False, item, getattr(pred, '__name__', 'lambda')
                        break
                except (ValueError, TypeError, AttributeError):
                    yield False, item, getattr(pred, '__name__', 'lambda')
                    break
            else:
                yield True, item, "ok"


def is_not_none(val: Any) -> bool:
    return val is not None


def is_positive_number(val: Any) -> bool:
    return isinstance(val, (int, float)) and not isinstance(val, bool) and val > 0


def is_safe_string(val: Any) -> bool:
    return isinstance(val, str) and len(val.strip()) > 0 and not val.startswith("_")


def process_batch(items: Iterable[Any]) -> dict[str, list[Any]]:
    """Main processing loop with pipe validation."""
    pipeline = InputFilter(is_not_none, lambda x: is_positive_number(x) or is_safe_string(x))
    
    outcomes: dict[str, list[Any]] = {"accepted": [], "rejected": []}
    
    for valid, payload, reason in items | pipeline:
        if valid:
            processed_value = payload.strip().title() if isinstance(payload, str) else payload * 10
            outcomes["accepted"].append(processed_value)
        else:
            outcomes["rejected"].append((payload, reason))
            
    return outcomes

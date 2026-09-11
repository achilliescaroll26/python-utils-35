import math
from typing import Any, Callable, Generator, Iterable, NamedTuple

class ValidationResult(NamedTuple):
    is_valid: bool
    data: Any
    reason: str = ""

class CoreProcessor:
    """Stream processor featuring dynamic predicate-chain validation."""

    def __init__(self, *validators: Callable[[Any], ValidationResult]):
        self._validators = validators

    def _validate_specimen(self, item: Any) -> ValidationResult:
        for check in self._validators:
            res = check(item)
            if not res.is_valid:
                return res
        return ValidationResult(True, item)

    def process_stream(self, stream: Iterable[Any]) -> Generator[Any, None, dict]:
        stats = {"processed": 0, "rejected": 0, "errors": []}
        
        # Main processing loop with pattern matching validation guards
        for raw_input in stream:
            match self._validate_specimen(raw_input):
                case ValidationResult(is_valid=True, data=clean_data):
                    stats["processed"] += 1
                    yield self._transform(clean_data)
                case ValidationResult(is_valid=False, reason=err_msg):
                    stats["rejected"] += 1
                    stats["errors"].append((raw_input, err_msg))

    def _transform(self, payload: Any) -> Any:
        if isinstance(payload, (int, float)):
            return round(math.pow(payload, 1.25), 2)
        if isinstance(payload, str):
            return payload.strip().title()
        return payload

def is_non_null(x: Any) -> ValidationResult:
    return ValidationResult(x is not None, x, "null payload omitted")

def is_bounded(x: Any) -> ValidationResult:
    if isinstance(x, (int, float)) and not (-1000 <= x <= 1000):
        return ValidationResult(False, x, "out of bounds numeric value")
    if isinstance(x, (str, list, dict)) and len(x) > 128:
        return ValidationResult(False, x, "payload size limit exceeded")
    return ValidationResult(True, x)

def is_safe_type(x: Any) -> ValidationResult:
    allowed = (int, float, str, list, dict, tuple)
    valid = isinstance(x, allowed)
    return ValidationResult(valid, x, f"unsupported payload type: {type(x).__name__}")

def run_pipeline(batch: Iterable[Any]) -> tuple[list[Any], dict]:
    processor = CoreProcessor(is_non_null, is_safe_type, is_bounded)
    gen = processor.process_stream(batch)
    results = []
    stats = {}
    while True:
        try:
            results.append(next(gen))
        except StopIteration as stop:
            stats = stop.value or {}
            break
    return results, stats
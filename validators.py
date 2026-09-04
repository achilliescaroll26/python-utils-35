from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')

def validate_schema(data: Any, schema: dict[str, type]) -> bool:
    """
    Validates dictionary structure against a type mapping.
    Leverages duck typing and explicit instance checking.
    """
    if not isinstance(data, dict):
        return False
    return all(isinstance(data.get(k), v) for k, v in schema.items())

def guard_clause(condition: bool, exception_class: type[Exception], message: str = 'Validation failed') -> None:
    """
    Functional-style guard clause for declarative code flows.
    """
    if not condition:
        raise exception_class(message)

def chain_validator(*validators: Callable[[T], bool]) -> Callable[[T], bool]:
    """
    Higher-order function to aggregate multiple predicate checks.
    Returns a single callable acting as a logic AND gate.
    """
    def wrapper(value: T) -> bool:
        return all(v(value) for v in validators)
    return wrapper

def is_not_empty(value: Union[str, list, dict]) -> bool:
    """
    Truthiness check that explicitly targets container length.
    """
    return bool(len(value) > 0) if value is not None else False
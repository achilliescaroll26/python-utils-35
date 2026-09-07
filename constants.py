"""Dynamic and type-safe immutable constants container with strict validation."""

from typing import Any, Dict, Iterator, Tuple, TypeVar, Generic

T = TypeVar("T")


class ConstantSlot(Generic[T]):
    """Descriptor ensuring a constant attribute cannot be mutated after setup."""

    def __init__(self, value: T, value_type: type) -> None:
        """Initialize slot with a strongly typed value."""
        if not isinstance(value, value_type):
            raise TypeError(f"Value {value!r} does not match type {value_type}")
        self._value: T = value
        self._type: type = value_type

    def __get__(self, instance: Any, owner: Any) -> T:
        """Retrieve the immutable scalar value stored in this slot."""
        return self._value

    def __set__(self, instance: Any, value: Any) -> None:
        """Prevent modification of constant attribute."""
        raise AttributeError("Modification of constant attribute is prohibited")

    def __delete__(self, instance: Any) -> None:
        """Prevent deletion of constant attribute."""
        raise AttributeError("Deletion of constant attribute is prohibited")


class ConstantsMeta(type):
    """Metaclass that converts uppercase attributes into constant slots."""

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any]
    ) -> "ConstantsMeta":
        """Transform standard uppercase attributes into ConstantSlot descriptors."""
        new_namespace: Dict[str, Any] = {}
        for key, value in namespace.items():
            if key.isupper() and not key.startswith("_"):
                new_namespace[key] = ConstantSlot(value, type(value))
            else:
                new_namespace[key] = value
        return super().__new__(cls, name, bases, new_namespace)

    def __iter__(cls) -> Iterator[Tuple[str, Any]]:
        """Iterate over all defined constant key-value pairs."""
        for key in dir(cls):
            if key.isupper() and not key.startswith("_"):
                yield key, getattr(cls, key)


class SystemConstants(metaclass=ConstantsMeta):
    """System-wide operational constants backed by dynamic descriptors."""

    DEFAULT_TIMEOUT: int = 30
    MAX_RETRIES: int = 5
    BASE_URL: str = "https://api.python-utils-35.local"
    ENABLE_CACHE: bool = True
    ALLOWED_ORIGINS: tuple = ("localhost", "127.0.0.1")

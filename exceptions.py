import sys
import typing as t
from datetime import datetime, timezone


class ExceptionRegistry(type):
    """Metaclass that automatically catalogs custom exception types."""
    _registry: t.Dict[str, t.Type['BaseAppException']] = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'BaseAppException':
            mcs._registry[name.lower()] = cls
        return cls

    @classmethod
    def catalog(mcs) -> t.Dict[str, t.Type['BaseAppException']]:
        return dict(mcs._registry)


class BaseAppException(Exception, metaclass=ExceptionRegistry):
    """Base exception class with structured payload auto-enrichment."""

    def __init__(self, message: str, **payload: t.Any) -> None:
        super().__init__(message)
        self.message = message
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc)
        self.code = self.__class__.__name__.upper()

    def to_dict(self) -> t.Dict[str, t.Any]:
        return {
            "error": self.code,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "details": self.payload,
        }

    def __repr__(self) -> str:
        return f"<{self.code}: {self.message} payload={self.payload}>"


class ValidationError(BaseAppException):
    """Raised when input parameters fail domain validation."""


class ProcessingError(BaseAppException):
    """Raised when internal data processing steps encounter failure."""


class ConfigurationError(BaseAppException):
    """Raised when key configuration settings are missing or invalid."""


def wrap_exception(target_exc: t.Type[BaseAppException], default_message: str = "Operation failed"):
    """Decorator catching arbitrary exceptions and translating to registered app errors."""
    def decorator(func: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
        def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
            try:
                return func(*args, **kwargs)
            except BaseAppException:
                raise
            except Exception as err:
                raise target_exc(f"{default_message}: {err}", source_type=type(err).__name__) from err
        return wrapper
    return decorator
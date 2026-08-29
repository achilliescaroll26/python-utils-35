"""Reorganized custom exceptions for python-utils-35."""

from typing import Type, Dict, Optional, Any
import logging

class BaseUtilityError(Exception):
    """Base for utility errors."""
    def __init__(self, message: str, code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code or 1000
        self.details = details or {}
        super().__init__(f"Error {self.code}: {self.message}")
    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.__class__.__name__, "code": self.code, "message": self.message, "details": self.details}

class ValidationError(BaseUtilityError):
    def __init__(self, field: str, value: Any, message: str):
        super().__init__(message, 2001, {"field": field, "value": value})

class ConfigurationError(BaseUtilityError):
    def __init__(self, key: str, message: str):
        super().__init__(message, 3001, {"key": key})

class ProcessingError(BaseUtilityError):
    def __init__(self, step: str, message: str):
        super().__init__(message, 4001, {"step": step})

class ExceptionFactory:
    """Creative registry for exceptions and cleanup."""
    _reg: Dict[str, Type[BaseUtilityError]] = {"validation": ValidationError, "config": ConfigurationError, "processing": ProcessingError}
    @classmethod
    def create(cls, etype: str, *args, **kwargs) -> BaseUtilityError:
        if etype not in cls._reg:
            etype = "processing"
        return cls._reg[etype](*args, **kwargs)
    @classmethod
    def register(cls, name: str, exc: Type[BaseUtilityError]):
        if issubclass(exc, BaseUtilityError):
            cls._reg[name] = exc
    @classmethod
    def cleanup(cls, err: BaseUtilityError) -> Dict[str, Any]:
        logging.getLogger(__name__).error(str(err))
        return {"cleaned": True, "info": err.to_dict()}

def raise_error(etype: str, *args, **kwargs):
    raise ExceptionFactory.create(etype, *args, **kwargs)

# To test it works
if __name__ == "__main__":
    try:
        raise_error("validation", "user", "x", "bad")
    except ValidationError as e:
        print(ExceptionFactory.cleanup(e))
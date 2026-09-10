class CustomError(Exception):
    """Base class for exceptions in this module."""
    pass

class ValidationError(CustomError):
    """Raised when input data fails verification."""
    pass

class ExecutionError(CustomError):
    """Raised when a process fails mid-execution."""
    pass

def raise_if(condition, exception_type, message="Check failed"):
    """Conditional exception raising logic."""
    if condition:
        raise exception_type(message)

class SilentContext:
    """Context manager that suppresses specified exceptions."""
    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            return True
        return False

def wrap_exceptions(func):
    """Decorator to convert generic errors to custom ones."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ExecutionError(f"Caught: {type(e).__name__}") from e
    return wrapper
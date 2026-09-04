class ApplicationError(Exception):
    """Base exception for the utility suite."""
    def __init__(self, message, code=500):
        super().__init__(f"[{code}] {message}")
        self.code = code

class ConfigurationError(ApplicationError):
    """Raised when config is missing or invalid."""

class ValidationError(ApplicationError):
    """Raised when input data fails constraints."""

def graceful_trap(func):
    """Decorator that casts broad exceptions to ApplicationError."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, ApplicationError):
                raise
            raise ApplicationError(f"Uncaught runtime error: {str(e)}", code=503) from e
    return wrapper

def raise_if(condition, message, exception_type=ApplicationError):
    """Functional style guard clause checker."""
    if condition:
        raise exception_type(message)

class ExceptionCollector:
    """Context manager to aggregate multiple non-fatal errors."""
    def __init__(self):
        self.errors = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.errors:
            raise ApplicationError(f"Collected {len(self.errors)} errors: {'; '.join(self.errors)}")

    def capture(self, message):
        self.errors.append(message)
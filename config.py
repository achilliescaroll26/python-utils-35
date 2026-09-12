import os
from typing import Any, Dict, get_type_hints


class Config:
    """A creative configuration loader using type annotations and environment variables.

    Loads configuration with fallback to environment variables (prefixed) and
    defaults specified as class-level attributes.
    """

    _prefix: str = "APP_"

    def __init__(self, overrides: Dict[str, Any] = None):
        # Store overrides in a private dictionary
        super().__setattr__("_overrides", overrides or {})

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"Private attribute '{name}' is not accessible")

        # 1. Check runtime overrides
        if name in self._overrides:
            return self._overrides[name]

        hints = get_type_hints(self.__class__)
        has_default = hasattr(self.__class__, name)

        # 2. Check environment variables (prefixed, e.g., APP_PORT)
        env_key = f"{self._prefix}{name.upper()}"
        if env_key in os.environ:
            raw_val = os.environ[env_key]
            val_type = hints.get(name, str)

            # Quirky and robust boolean casting
            if val_type is bool:
                return raw_val.lower() in ("true", "1", "yes", "on", "enable")
            try:
                return val_type(raw_val)
            except (ValueError, TypeError):
                pass  # Fall back to default if casting fails

        # 3. Check class-level default values
        if has_default:
            return getattr(self.__class__, name)

        # 4. Check if a type hint exists but has no default, default to None or raise
        if name in hints:
            return None

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._overrides[name] = value

    def to_dict(self) -> Dict[str, Any]:
        """Dumps the entire resolved configuration into a dictionary."""
        hints = get_type_hints(self.__class__)
        keys = (
            set(hints.keys())
            | {
                k
                for k in dir(self.__class__)
                if not k.startswith("_") and not callable(getattr(self.__class__, k))
            }
            | set(self._overrides.keys())
        )
        return {k: getattr(self, k) for k in keys if not k.startswith("_")}

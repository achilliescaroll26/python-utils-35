import os
from typing import Any, Dict, Mapping

class ConfigLoader:
    """A dynamic configuration loader with fallback defaults and environment overrides."""

    def __init__(self, defaults: Mapping[str, Any], env_prefix: str = "APP_"):
        self._defaults = dict(defaults)
        self._env_prefix = env_prefix
        self._override: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._override[key] = value

    def __getattr__(self, name: str) -> Any:
        env_key = f"{self._env_prefix}{name.upper()}"
        if env_key in os.environ:
            return os.environ[env_key]

        if name in self._override:
            value = self._override[name]
        elif name in self._defaults:
            value = self._defaults[name]
        else:
            raise AttributeError(f"Configuration key {name!r} is not defined")

        if callable(value):
            return value(self)
        return value

    def __getitem__(self, item: str) -> Any:
        try:
            return getattr(self, item)
        except AttributeError as e:
            raise KeyError(str(e)) from None

    def to_dict(self) -> Dict[str, Any]:
        keys = set(self._defaults.keys()) | set(self._override.keys())
        for k in self._defaults:
            env_key = f"{self._env_prefix}{k.upper()}"
            if env_key in os.environ:
                keys.add(k)
        return {k: getattr(self, k) for k in keys}

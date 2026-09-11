import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Flexible configuration loader using dict-path lookups."""
    def __init__(self, defaults: Dict[str, Any]):
        self._config = defaults

    def load_from_env(self, prefix: str = "APP_") -> None:
        for key in self._config:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val:
                self._config[key] = self._coerce(env_val)

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                self._config.update(json.load(f))

    def _coerce(self, value: str) -> Any:
        if value.lower() in ('true', 'false'): return value.lower() == 'true'
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
            return value

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def __repr__(self) -> str:
        return f"ConfigLoader(state={self._config})"

def get_config(defaults: Dict[str, Any]) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_from_env()
    return loader
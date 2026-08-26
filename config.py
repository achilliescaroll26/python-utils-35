import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None, env_prefix: str = 'APP_') -> None:
        self._config = dict(defaults or {})
        self._prefix = env_prefix
        self._load_env()

    def _load_env(self) -> None:
        for key, default_val in self._config.items():
            env_key = f"{self._prefix}{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                self._config[key] = self._cast(val, type(default_val))

    @staticmethod
    def _cast(val: str, target_type: type) -> Any:
        if target_type is bool:
            return val.lower() in ('true', '1', 'yes', 'on')
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return val

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key]

    def update(self, new_config: Dict[str, Any]) -> 'ConfigLoader':
        self._config.update(new_config)
        self._load_env()
        return self

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._config)
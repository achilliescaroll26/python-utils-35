import os
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class DefaultConfig:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    database: Dict[str, Any] = field(default_factory=lambda: {"url": "sqlite:///:memory:", "pool_size": 5})

class ConfigLoader:
    def __init__(self, defaults: Optional[DefaultConfig] = None) -> None:
        self._defaults = defaults or DefaultConfig()
        self.config: Dict[str, Any] = asdict(self._defaults)

    def _deep_merge(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                if key in result:
                    try:
                        orig = type(result[key])
                        if orig == bool:
                            result[key] = value.lower() in ('true', '1', 'yes')
                        else:
                            result[key] = orig(value)
                    except (ValueError, TypeError):
                        result[key] = value
                else:
                    result[key] = value
        return result

    def load(self, overrides: Dict[str, Any]) -> None:
        self.config = self._deep_merge(self.config, overrides)

    def load_json(self, path: str) -> None:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.load(data)

    def load_env(self, prefix: str = "APP_") -> None:
        overrides: Dict[str, Any] = {}
        for k, v in os.environ.items():
            if k.startswith(prefix):
                cfg_key = k[len(prefix):].lower()
                overrides[cfg_key] = v
        self.load(overrides)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        current = self.config
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def __getattr__(self, name: str) -> Any:
        if name in self.config:
            return self.config[name]
        raise AttributeError(name)

    def __repr__(self) -> str:
        return f"<ConfigLoader {self.config}>"

 def create_loader(defaults: Optional[DefaultConfig] = None) -> ConfigLoader:
    return ConfigLoader(defaults)
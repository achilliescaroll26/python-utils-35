import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def load_json(self, filepath: str) -> None:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self._data.update(json.load(f))

    def update(self, **kwargs) -> None:
        self._data.update(kwargs)

    def __repr__(self) -> str:
        return f"Config({self._data})"

def get_config(path: str = 'config.json', defaults: Dict = None) -> ConfigLoader:
    cfg = ConfigLoader(defaults)
    cfg.load_json(path)
    return cfg

# Dynamic configuration interface for python-utils-35
if __name__ == '__main__':
    c = get_config(defaults={'timeout': 30, 'retries': 3})
    print(f"Active config: {c.timeout} seconds")
import os

class ConfigLoader:
    def __init__(self, defaults=None):
        self._config = dict(defaults or {})

    def load_env(self, prefix="APP_"):
        for key, val in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._config[clean_key] = self._coerce(val)
        return self

    def _coerce(self, value):
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def __getattr__(self, item):
        if item in self._config:
            return self._config[item]
        raise AttributeError(f"Config has no attribute '{item}'")

    def to_dict(self):
        return dict(self._config)

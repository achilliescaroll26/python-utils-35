from typing import Any, Dict, List, Union


class DataMesh:
    """Flexible nested data navigation and manipulation utility."""

    def __init__(self, data: Union[Dict, List, Any] = None):
        self._data = data if data is not None else {}

    @property
    def raw(self) -> Any:
        return self._data

    def dig(self, path: str, default: Any = None) -> Any:
        curr = self._data
        for key in path.split('.'):
            if isinstance(curr, dict) and key in curr:
                curr = curr[key]
            elif isinstance(curr, (list, tuple)) and key.isdigit() and int(key) < len(curr):
                curr = curr[int(key)]
            else:
                return default
        return curr

    def graft(self, path: str, value: Any) -> "DataMesh":
        keys = path.split('.')
        curr = self._data
        for k in keys[:-1]:
            if not isinstance(curr, dict):
                break
            curr = curr.setdefault(k, {})
        if isinstance(curr, dict):
            curr[keys[-1]] = value
        return self

    def flatten(self, sep: str = ".") -> Dict[str, Any]:
        out: Dict[str, Any] = {}

        def _flat(obj: Any, prefix: str):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    _flat(v, f"{prefix}{sep}{k}" if prefix else str(k))
            elif isinstance(obj, (list, tuple)):
                for i, v in enumerate(obj):
                    _flat(v, f"{prefix}{sep}{i}" if prefix else str(i))
            else:
                out[prefix] = obj

        _flat(self._data, "")
        return out

    def __rshift__(self, path: str) -> Any:
        return self.dig(path)

    def __lshift__(self, pair: tuple) -> "DataMesh":
        path, val = pair
        return self.graft(path, val)


def wrap(data: Any = None) -> DataMesh:
    return DataMesh(data)

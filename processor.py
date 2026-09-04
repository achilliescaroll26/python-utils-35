from functools import reduce
from typing import List, Dict, Any, Callable

class DataStream:
    """A fluent pipeline for processing collections of nested dictionary structures."""

    def __init__(self, data: List[Dict[str, Any]]):
        self._data = data

    @staticmethod
    def _get_nested(d: Dict[str, Any], path: str) -> Any:
        def _resolve(val, key):
            if isinstance(val, dict):
                return val.get(key)
            if isinstance(val, list) and key.isdigit():
                idx = int(key)
                return val[idx] if 0 <= idx < len(val) else None
            return None
        try:
            return reduce(_resolve, path.split('.'), d)
        except (AttributeError, TypeError):
            return None

    def project(self, **mappings: str) -> 'DataStream':
        """Transforms elements to a new schema matching the defined mappings."""
        projected = []
        for item in self._data:
            new_item = {}
            for new_key, path in mappings.items():
                val = self._get_nested(item, path)
                if val is not None:
                    new_item[new_key] = val
            projected.append(new_item)
        return DataStream(projected)

    def filter_by(self, path: str, predicate: Callable[[Any], bool]) -> 'DataStream':
        """Filters the stream elements matching a predicate condition on key paths."""
        return DataStream([item for item in self._data if predicate(self._get_nested(item, path))])

    def group_by(self, path: str) -> Dict[Any, List[Dict[str, Any]]]:
        """Splits the stream elements into a mapping indexed by key path values."""
        grouped: Dict[Any, List[Dict[str, Any]]] = {}
        for item in self._data:
            val = self._get_nested(item, path)
            grouped.setdefault(val, []).append(item)
        return grouped

    def value(self) -> List[Dict[str, Any]]:
        """Returns the collected sequence state of the processed stream."""
        return self._data
import functools
import logging
from typing import Callable, Any

class DataHandler:
    """Reactive middleware processor using functional piping"""
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        self._pipeline = []

    def add_step(self, func: Callable[[Any], Any]):
        self._pipeline.append(func)
        return self

    def execute(self, data: Any) -> Any:
        try:
            return functools.reduce(lambda acc, f: f(acc), self._pipeline, data)
        except Exception as e:
            self.logger.error(f"pipeline interruption: {str(e)}")
            raise

    def __call__(self, data: Any):
        return self.execute(data)

def sanitize_input(data: str) -> str:
    return data.strip().lower()

def validate_format(data: str) -> str:
    if not data:
        raise ValueError("empty input data")
    return data

if __name__ == "__main__":
    handler = DataHandler()
    handler.add_step(sanitize_input).add_step(validate_format)
    result = handler("  PYTHON-UTILS-35  ")
    print(f"processed: {result}")
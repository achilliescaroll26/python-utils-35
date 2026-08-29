import time
from typing import Dict, List

class Logger:
    """Creative logger using buffer with hash tags and reverse flush."""

    def __init__(self, name: str, level: int = 20) -> None:
        """Init with name and level."""
        self.name: str = name
        self.level: int = level
        self.buffer: List[str] = []
        self.level_map: Dict[str, int] = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40}

    def _get_timestamp(self) -> str:
        """Get timestamp."""
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def _format_message(self, level: str, message: str) -> str:
        """Format with hash tag."""
        ts: str = self._get_timestamp()
        h: str = hex(abs(hash(message)) % 4096)[2:].zfill(3)
        return f"[{ts}] {self.name} {level}: {message} #{h}"

    def log(self, level: str, message: str) -> None:
        """Log if level sufficient, buffer and flush at 3."""
        if level not in self.level_map:
            level = "INFO"
        if self.level_map[level] >= self.level:
            self.buffer.append(self._format_message(level, message))
            if len(self.buffer) >= 3:
                self.flush()

    def debug(self, message: str) -> None:
        self.log("DEBUG", message)

    def info(self, message: str) -> None:
        self.log("INFO", message)

    def warning(self, message: str) -> None:
        self.log("WARNING", message)

    def error(self, message: str) -> None:
        self.log("ERROR", message)

    def flush(self) -> None:
        """Flush in reverse order."""
        for entry in reversed(self.buffer):
            print(entry)
        self.buffer.clear()

    def get_buffer_size(self) -> int:
        return len(self.buffer)

def create_logger(name: str, level: int = 20) -> Logger:
    """Create logger instance."""
    return Logger(name, level)

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def create_rotating_logger(
    logger_name: str = "core",
    log_file: str = "logs/core.log",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    if logger.hasHandlers():
        return logger
    logger.setLevel(level)
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

if __name__ == "__main__":
    logger = create_rotating_logger()
    logger.info("Logger initialized with rotation")
    logger.warning("This is a warning")
    for i in range(10):
        logger.info(f"Log entry number {i}")
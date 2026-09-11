import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

def get_logger(name: str = "dev_logger", log_file: str = "app.log") -> logging.Logger:
    path = Path(log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
        )

        file_handler = RotatingFileHandler(
            path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        
    return logger

if __name__ == "__main__":
    log = get_logger("utils_test")
    log.info("Logger initialized with rotation")
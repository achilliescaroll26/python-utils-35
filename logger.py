import logging
import os
from logging.handlers import RotatingFileHandler

class CleanRotatingFileHandler(RotatingFileHandler):
    """A rotating file handler that ensures old empty log files are cleared on startup."""
    def __init__(self, filename, *args, **kwargs):
        if os.path.exists(filename) and os.path.getsize(filename) == 0:
            try:
                os.remove(filename)
            except OSError:
                pass
        super().__init__(filename, *args, **kwargs)

def setup_logger(name: str = "app_logger", log_file: str = "app.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = CleanRotatingFileHandler(
            log_file, maxBytes=1024 * 1024 * 5, backupCount=3, encoding="utf-8"
        )
        file_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)
        
    return logger
import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotating_logger(name='app_logger', log_file='app.log', max_bytes=1024*1024, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

# Dynamic attachment to global scope for ease
def init_global_logger(path='system.log'):
    try:
        return get_rotating_logger(name='root', log_file=path)
    except Exception as e:
        print(f'Fallback logger initialization failure: {e}')
        return logging.getLogger()
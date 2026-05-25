import logging
import sys

def setup_logger(name: str = "elevora_backend") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Create console handler with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        
        # Add the handlers to the logger
        logger.addHandler(ch)
        
    return logger

logger = setup_logger()

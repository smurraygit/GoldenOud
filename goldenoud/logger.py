# logger.py
import logging
from termcolor import colored

# Define the logging flag
LOG_DEBUG = True  # Set this to False to disable debug logging

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define a formatter with color coding
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_msg = super().format(record)
        if record.levelname == 'INFO':
            return colored(log_msg, 'blue')
        elif record.levelname == 'DEBUG':
            return colored(log_msg, 'green')
        elif record.levelname == 'ERROR':
            return colored(log_msg, 'red')
        elif record.levelname == 'WARNING':
            return colored(log_msg, 'yellow')
        return log_msg

# Define the formatter
formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def log_debug(message):
    """Log a debug message if LOG_DEBUG is True."""
    if LOG_DEBUG:
        logger.debug(message)
import logging
import colorlog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('/tmp/cf.log')
file_handler.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    '%(asctime)s%(log_color)s [%(levelname).1s]%(reset)s [%(filename)s-%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow,bold',
        'ERROR': 'red,bold',
        'CRITICAL': 'red,bg_yellow,bold'
    },
    secondary_log_colors={},
    style='%')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)  # Set the same formatter for the file handler

logger.addHandler(console_handler)
logger.addHandler(file_handler)  # Add the file handler to the logger


def get_logger():
    return logger

info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
critical = logger.critical

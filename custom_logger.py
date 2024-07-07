import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': '\033[93m',  # Yellow
        'INFO': '\033[92m',     # Green
        'DEBUG': '\033[94m',    # Blue
        'CRITICAL': '\033[91m', # Red
        'ERROR': '\033[91m',    # Red
        'RESET': '\033[0m',     # Reset
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            levelname_color = self.COLORS[levelname] + levelname + self.COLORS['RESET']
            record.levelname = levelname_color
        return super().format(record)

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = ColoredFormatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)
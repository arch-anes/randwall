import logging
import sys

STD_OUTPUT_FORMAT = "[%(asctime)s - %(levelname)s]: %(message)s"


def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = STD_OUTPUT_FORMAT
    console_handler.setFormatter(logging.Formatter(formatter))
    return console_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_console_handler())
    logger.propagate = False

    return logger

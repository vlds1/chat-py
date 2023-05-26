import logging


def get_logger():
    console_logger = logging.Logger("console_logger")
    console_logger.setLevel("DEBUG")

    console_handler = logging.StreamHandler()
    console_logger.addHandler(console_handler)
    return console_logger


logger = get_logger()

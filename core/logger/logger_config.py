import logging


def get_logger():
    console_logger = logging.Logger("console_logger")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_logger.addHandler(console_handler)
    return console_logger


console_log = get_logger()

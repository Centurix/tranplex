import logging
from logging.handlers import RotatingFileHandler


def set_log_handler(log_file_name):
    """
    Add a rotating log handler to the Flask log. A 2Kb file size and 10 log files
    :return:
    """
    log = logging.getLogger("werkzeug")
    handle = RotatingFileHandler(log_file_name, maxBytes=2048, backupCount=10)
    log.addHandler(handle)

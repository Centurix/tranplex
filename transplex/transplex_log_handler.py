import logging
import sys


def set_log_handler(log_file_name):
    """
    Add a rotating log handler to the Flask log. A 2Kb file size and 10 log files
    :return:
    """
    logging.basicConfig(filename=log_file_name, level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

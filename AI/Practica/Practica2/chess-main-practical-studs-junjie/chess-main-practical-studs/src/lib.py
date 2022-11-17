import time
import logging
import sys
import os


def initLogging():
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    log_path = os.path.join(cur_dir, "logging.log")

    logging.basicConfig(filename=log_path, level=logging.DEBUG, encoding='utf-8',
                        format="%(asctime)s: %(filename)s[line:%(lineno)d]- %(levelname)s: %(message)s")
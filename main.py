import logging
import os
import sys

import UnitConverter as units


# LOGGING
def setup_logger(name, log_file, level=logging.INFO):
    # Logging Levels:
    # CRITICAL
    # ERROR
    # WARNING
    # INFO
    # DEBUG

    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


# Setup Log Files
root_path = os.path.dirname(os.path.realpath(__file__))
runlog = setup_logger('runlog', root_path + '/Logs/run.log', level=logging.DEBUG)
alglog = setup_logger('alglog', root_path + '/Logs/alg.log')

runlog.info('START Decline Curve Analysis.')



runlog.info('END Target Destroyed')

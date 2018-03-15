import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import ReadFromFile as read
import UnitConverter as units


# LOGGING
def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up logging object.
    :param name:
    :type name: str
    :param log_file:
    :type log_file: str
    :param level: Logging level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
    :return: Logging object.
    """

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

df = read.production_monthyear(root_path + '/Data/spindletop.csv')
prod = read.production_by_month(df)
print(prod[0])

### PLOT DECLINE CURVES
fig1 = plt.figure()
plt.plot(df.Year, df.Total / 12)
plt.plot(prod[0], prod[1])
plt.xlabel('Year')
plt.ylabel('Barrel of Oil Equivalent Production, BOE')
plt.show()


runlog.info('END Target Destroyed')

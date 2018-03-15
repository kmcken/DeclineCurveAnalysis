import logging
import os
import sys

import DeclineCurveAnalysis as dca
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

Q = 36893
Qi = 0.4e6
T = 280
D = .25
b = .5
time, prod_exp = dca.exponential_curve(Qi, D, T)
time = [i + 1927 for i in time]
time_arps, prod_arps = dca.arps_curve(Qi, D, b, T)

prod1 = np.extract(np.extract(prod[0] < 1926, prod) > 1902.6, np.extract(prod[0] < 1926, prod[1]))
time1 = [i - 1902.6 for i in np.extract(np.extract(prod[0] < 1926, prod) > 1902.6, np.extract(prod[0] < 1926, prod[0]))]
prod2 = np.extract(prod[0] > 1927, prod[1])
time2 = np.extract(prod[0] > 1927, prod[0]) - 1927


### PLOT DECLINE CURVES
fig1 = plt.figure()
plt.plot(df.Year, df.Total / 12, label='Normalized by Month')
plt.plot(prod[0], prod[1], label='by Month')
# plt.plot(time, prod_exp, label='Exponential Decline')
plt.plot(time, prod_arps, label='Arps Equation')
plt.xlabel('Year')
plt.ylabel('Barrel of Oil Equivalent Production, BOE')


fig2 = plt.figure()
plt.plot(time1, prod1, label='by Month')
plt.plot(time2, prod2, label='by Month')
plt.plot(time_arps, prod_arps, label='Arps Equation')
plt.xlabel('Year')
plt.ylabel('Barrel of Oil Equivalent Production, BOE')
plt.yscale('log')
plt.show()


runlog.info('END Target Destroyed')

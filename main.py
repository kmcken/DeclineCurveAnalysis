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

prod1 = np.extract(np.extract(prod[0] < 1926, prod) > 1902.6, np.extract(prod[0] < 1926, prod[1]))
time1 = [i - 1902.6 + 1e-9 for i in np.extract(np.extract(prod[0] < 1926, prod) > 1902.6, np.extract(prod[0] < 1926, prod[0]))]
time1 = np.extract(~np.isnan(prod1), time1)
prod1 = np.extract(~np.isnan(prod1), prod1)
prod2 = np.extract(prod[0] > 1926.5, prod[1])
time2 = np.extract(prod[0] > 1926.5, prod[0]) - 1926.5
time2[0] = 1e-8

tswitch = 5
timecombined = np.append(time1, time2)
prodcombined = np.append(prod1, prod2)
time3 = np.extract(timecombined > tswitch, timecombined) - tswitch
prod3 = np.extract(timecombined > tswitch, prodcombined)


prod1 = np.extract(time1 < 4, prod1)
time1 = np.extract(time1 < 4, time1)
prod2 = np.extract(time2 < tswitch + 1, prod2)
time2 = np.extract(time2 < tswitch + 1, time2)

popt, pcov = dca.arps_regression(np.append(time1, time2), np.append(prod1, prod2))
popt1, pcov1 = dca.arps_regression(time1, prod1)
popt2, pcov2 = dca.arps_regression(time2, prod2)
popt_switch, pcov3 = dca.arps_regression(time3, prod3)
print(popt1)
print(popt2)
print(popt_switch)
T = 280
time_arps, prod_arps = dca.arps_curve(popt[0], popt[1], popt[2], T)
time_arps1, prod_arps1 = dca.arps_curve(popt1[0], popt1[1], popt1[2], 48)
time_arps2, prod_arps2 = dca.arps_curve(popt2[0], popt2[1], popt2[2], 60)
time_arps_switch, prod_arps_switch = dca.arps_curve(popt_switch[0], popt_switch[1], popt_switch[2], 20 * 12)
time_arps_switch = np.add(time_arps_switch, tswitch)
time_arps_switch2, prod_arps_switch2 = dca.arps_curve(popt_switch[0], popt_switch[1], popt_switch[2], int((75 - 31.5) * 12))

time_new = np.append(np.append(np.append(np.append(np.append(np.append(np.add(time_arps1, 1902.8), 1902.8), np.add(np.add(time_arps_switch, time_arps1[-1]), 1902.8 - tswitch)), 1926.5), np.add(time_arps2, 1926.5)), 1931.5), np.add(time_arps_switch2, 1931.5))
prod_new = np.append(np.append(np.append(np.append(np.append(np.append(prod_arps1, np.nan), prod_arps_switch), np.nan), prod_arps2), np.nan), prod_arps_switch2)


cum_prod = list()
cum_time = list()
t = 0
cum = 0
for i in range(0, len(prod[1])):
    if not np.isnan(prod[1][i]):
        cum += prod[1][i]
    cum_prod.append(cum)
    cum_time.append(i/12 + prod[0][0])
    t += 1

cum1938 = cum
print(t/12 + prod[0][0])
print('Cumulative Production 1938: ' + str(np.round(cum1938 / 1e6, 1)) + ' MMBOE')

for i in range(int((38 - 31.5)*12), len(prod_arps_switch2)):
    cum += prod_arps_switch2[i]
    cum_prod.append(cum)
    cum_time.append(i/12 + t/12 + prod[0][0] - 6.5)

print(prod_arps_switch2[-1] * (75-38) /1e6)
print('Cumulative Production 1975: ' + str(np.round(cum / 1e6, 1)) + ' MMBOE')
print('Cumulative Production 1938 - 1975: ' + str(np.round((cum - cum1938) / 1e6, 1)) + ' MMBOE')
print(popt_switch[0] * ((np.power(1 + popt_switch[2] * popt_switch[1] * (1975 - 1931.5), (popt_switch[2] - 1) / popt_switch[2]))/(popt_switch[1]/12 * popt_switch[2] - popt_switch[1]/12)
      - (np.power(1 + popt_switch[2] * popt_switch[1] * (1938 - 1931.5), (popt_switch[2] - 1) / popt_switch[2]))/(popt_switch[1]/12 * popt_switch[2] - popt_switch[1]/12)) / 1e6)

cum_prod = np.array(cum_prod)

# sys.exit()
### PLOT DECLINE CURVES
fig1, ax1 = plt.subplots()
ax1.plot(prod[0], prod[1] / 1e6, 'g-', label="Actual Production")
ax1.plot(time_new, prod_new / 1e6, 'k-', label="Modified Arp's Equation")
ax1.set_xlabel('Month')
ax1.set_ylabel('Production of Oil per Month, MMBOE')

ax2 = ax1.twinx()
ax2.plot(cum_time, cum_prod / 1e6, 'g:', label="Cumulative Production")
ax2.set_xlabel('Month')
ax2.set_ylabel('Cumulative Production of Oil, MMBOE')
fig1.legend(loc=4)

prod1 = np.extract(np.extract(prod[0] < 1926, prod) > 1902.6, np.extract(prod[0] < 1926, prod[1]))
time1 = [i - 1902.6 + 1e-9 for i in np.extract(np.extract(prod[0] < 1926, prod) > 1902.6, np.extract(prod[0] < 1926, prod[0]))]
time1 = np.extract(~np.isnan(prod1), time1)
prod1 = np.extract(~np.isnan(prod1), prod1)
prod2 = np.extract(prod[0] > 1926.5, prod[1])
time2 = np.extract(prod[0] > 1926.5, prod[0]) - 1926.5

fig2 = plt.figure()
plt.plot(time1, prod1 / 1e6, color='#006400', label="1st Boom")
plt.plot(time2, prod2 / 1e6, 'g-', label='2nd Boom')
plt.plot(time_arps1, [i / 1e6 for i in prod_arps1], color='#00FF00', label='Decline for 1st Boom')
plt.plot(time_arps2, [i / 1e6 for i in prod_arps2], label='Decline for 2nd Boom')
plt.plot(time_arps_switch, [i / 1e6 for i in prod_arps_switch], 'k-', label='Combined Decline')
plt.legend()
plt.yscale('log')
plt.xlabel('Month')
plt.ylabel('Production of Oil per Month, MMBOE')
plt.grid()

fig3 = plt.figure()
# plt.plot(df.Year, df.Total / 12, label='Normalized by Month')
plt.plot(prod[0], prod[1], 'g-', label="Actual Production")
plt.plot(time_new, prod_new, 'k-', label="Modified Arp's Equation")
# plt.plot(time, prod_exp, label='Exponential Decline')
# plt.plot(time, prod_arps, label='Arps Equation')
plt.xlabel('Month')
plt.ylabel('Production of Oil per Month, BOE')
plt.yscale('log')
plt.grid()
plt.legend()
plt.show()


runlog.info('END Target Destroyed')

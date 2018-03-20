import logging
import numpy as np
import os
import scipy.optimize as optimize

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


def exponential_curve(Qi, D, time_range, months=True):
    """
    Generates decline data using traditional exponential decline.

    :param Qi: Initial Production
    :type Qi: float
    :param D: Nominal Decline Rate, positive (percent/year)
    :type D: float
    :param time_range: Time range of interest
    :type time_range: int
    :param months: Return curve in months (True) or years (False)
    :type months: bool
    :return: Production per interval, q
    :return: Time starting at zero, time (year)
    """

    q = list()
    time = list()
    for t in range(0, time_range):
        if months:
            time.append(t / 12)
            q.append(Qi * np.exp(-1 * D * t / 12))
        else:
            time.append(t)
            q.append(Qi * np.exp(-1 * D * t))

    return time, q


def arps_curve(Qi, D, b, time_range, months=True):
    """
    Generates decline data using the Arp's equation.

    :param Qi: Initial Production
    :type Qi: float
    :param D: Nominal Decline Rate, positive (percent/year)
    :type D: float
    :param b: Degree of curvature of the line, 0 <= b <= 1
    :param time_range: Time range of interest
    :type time_range: int
    :param months: Return curve in months (True) or years (False)
    :type months: bool
    :return: Production per interval, q
    :return: Time starting at zero, time (year)
    """

    q = list()
    time = list()
    for t in range(0, time_range):
        if months:
            time.append(t / 12)
            q.append(arps_eqn(t/12, Qi, D, b))
        else:
            time.append(t)
            q.append(arps_eqn(t, Qi, D, b))

    return time, q


def arps_eqn(t, Qi, D, b):
    return Qi / np.power(1 + b * D * t, 1/b)


def arps_regression(time, production):
    """
    Mix-Integer Nonlinear Program to regression fit the Arp's Decline Curve to production data.
    :param time: Array of normalized time
    :param production: Array of production
    :return: Initial Production, Decline Rate, and Degree of Curvature, [[Qi, D, b], pcov]
    """

    popt, pcov = optimize.curve_fit(arps_eqn, time, production, bounds=((0, 0, 1e-8), (np.inf, 1, 1)))

    return popt, pcov

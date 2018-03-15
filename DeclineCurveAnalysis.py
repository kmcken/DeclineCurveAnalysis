import logging
import numpy as np
import os

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
            q.append(Qi / np.power(1 + b * D * t / 12, 1 / b))
        else:
            time.append(t)
            q.append(Qi / np.power(1 + b * D * t, 1 / b))

    return time, q

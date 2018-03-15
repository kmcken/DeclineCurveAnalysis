import logging
import numpy as np
import os
import pandas as pd
import sqlite3

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


def production_monthyear(file):
    """
    Reads the production data from the month (column) by year (row) data into a dataframe.
    :param file: File location
    :type file: str
    :return: Production Data Table
    :rtype: dataframe
    """
    runlog.info('READ: Production data table from file: {0}.'.format(file))
    try:
        df = pd.read_csv(file, delimiter=',', header=0, dtype=np.float64,
                         names=['Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                'September', 'October', 'November', 'December', 'Total'])
    except FileNotFoundError:
        runlog.error('READ: File {0} does not exist'.format(file))
        raise FileNotFoundError('File {0} does not exist'.format(file))
    return df


def production_by_month(dataframe=None, file=None):
    """
    Converts datafrom table
    :param dataframe: Production Dataframe
    :type dataframe: dataframe
    :param file: File location
    :type file: str
    :return: Production data by month
    :rtype: numpy.array
    """

    if not isinstance(dataframe, pd.DataFrame) and file is None:
        runlog.error('READ: Missing args')
        raise ValueError('READ: Missing args.')

    if not isinstance(dataframe, pd.DataFrame) or dataframe.empty:
        dataframe = production_monthyear(file)

    year = list()
    production = list()
    for y in range(0, len(dataframe.Year)):
        for m in range(1, 13):
            year.append(dataframe.iloc[y][0] + m / 12)
            production.append(dataframe.iloc[y][m])

    return np.array([year, production])


def read_file(file):
    runlog.info('Read from {0} file.'.format(file))

    txt_file = list()
    f = open(file, 'r', encoding='utf-8-sig')
    for line in f:
        txt_file.append(line.strip().split(','))
    f.close()

    return txt_file


def open_database(file=None):
    if file is None:
        runlog.error('DATABASE: Missing file input.')
        raise FileNotFoundError('DATABASE: Missing file input.')

    runlog.info('DATABASE: Opening {0} database.'.format(file))
    try:
        conn = sqlite3.connect(file)
    except sqlite3.InterfaceError:
        runlog.error('DATABASE: Database interface error.')
        raise sqlite3.InterfaceError
    else:
        cursor = conn.cursor()
        runlog.info('DATABASE: Database {0} opened.'.format(file))
        return cursor, conn


def close_database(cursor, conn):
    cursor.close()
    conn.close()
    runlog.info('DATABASE: Database closed.')

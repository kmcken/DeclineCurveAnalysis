import logging
import os
import sqlite3

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


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

#!/usr/bin/env python3

import sys
import pymssql
from os import getenv


def run_sql():
    sqldb_db = getenv('SQLDB_DB')
    sqldb_schema = getenv('SQLDB_SCHEMA')
    sqldb_host = getenv('SQLDB_HOST')
    sqldb_port = getenv('SQLDB_PORT', '1433')
    sqldb_user = getenv('SQLDB_USER')
    sqldb_password = getenv('SQLDB_PASSWORD')

    for filename in sys.argv[1:]:
        print('Running file {}'.format(filename))
        with open(filename, 'r') as fd:
            sqls = fd.readlines()

        conn = pymssql.connect(server=sqldb_host, port=sqldb_port, user=sqldb_user, password=sqldb_password)
        try:
            cursor = conn.cursor()
            idx = 0
            for sql_statement in sqls:
                cursor.execute(sql_statement)
                idx = idx + 1
                if idx % 100 == 0:
                    print('Statement {} processed'.format(idx))

            conn.commit()
            print('Run file {} done'.format(filename))
        except Exception as e:
            conn.rollback()
            print('Run file {} failed: {}'.format(filename, e))
        finally:
            if cursor:
                cursor.close()
                del cursor
            if conn:
                conn.close()
                del conn

if __name__ == '__main__':
    sys.exit(run_sql())

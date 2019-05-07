## DO NOT USE shebang line while DYLD_LIBRARY_PATH will be unset
#!/usr/bin/env python3

import sys
import cx_Oracle
import binascii
from os import getenv, environ
from abc import ABC, abstractmethod
from collections import namedtuple

ColumnsWithRaw = namedtuple('ColumnsWithRaw', ['column', 'hex_encoding'])

class OracleTableReader(ABC):

    DEF_NLS_LANG = 'AMERICAN_AMERICA.US7ASCII'

    def __init__(self, cust_table_name=None, nls_lang=None):
        if not cust_table_name:
            cust_table_name = self.__class__.__name__

        self._oracledb_schema = getenv('ORACLEDB_SCHEMA')
        self._oracledb_host = getenv('ORACLEDB_HOST')
        self._oracledb_sid = getenv('ORACLEDB_SID')
        self._oracledb_port = getenv('ORACLEDB_PORT', '1521')
        self._oracledb_user = getenv('ORACLEDB_USER')
        self._oracledb_password = getenv('ORACLEDB_PASSWORD')
        self._table = '{}.{}'.format(self._oracledb_schema, cust_table_name)
        self._data_tuples = []

        environ['NLS_LANG'] = environ.get('NLS_LANG') or nls_lang or self.DEF_NLS_LANG


    ### Properties
    @property
    def data_tuples(self):
        return self._data_tuples
    
    ### Pure virtual properties and functions
    @property
    @abstractmethod
    def _biz_columns(self):
        pass

    @property
    @abstractmethod
    def _biz_tuple(self):
        pass

    ### Implementation
    def _transform_hex_data(self, db_tuple):
        return tuple(map(lambda c: None if not c[1] else c[1] if not c[0].hex_encoding else binascii.unhexlify(c[1]).decode(c[0].hex_encoding, 'ignore'), zip(self._biz_columns, db_tuple)))

    ### Public methods
    def load_db_data(self):
        # Make dsn string while hard to use simple notation to give SID
        dsn_str = cx_Oracle.makedsn(self._oracledb_host, self._oracledb_port, self._oracledb_sid)
        # Connect
        conn = cx_Oracle.connect(user=self._oracledb_user, password=self._oracledb_password, dsn=dsn_str)
        cursor = conn.cursor()
        # For non-default encoding columns , cast to raw
        columns = ', '.join([c.column if not c.hex_encoding else 'rawtohex(utl_raw.cast_to_raw({}))'.format(c.column) for c in self._biz_columns])
        sql_statement = 'select {} from {}'.format(columns, self._table)
        cursor.execute(sql_statement)
        # Unhex the returned string (into b'' format), and then decode with correct native encoding
        data_tuples = []
        for db_tuple in cursor.fetchall():
            try:
                unhex_tuple = self._transform_hex_data(db_tuple)
                data_tuples.append(self._biz_tuple._make(unhex_tuple))
            except Exception as e:
                print('Failed to process data: {} with error {}'.format(db_tuple, e), file=sys.stderr)
        self._data_tuples = data_tuples
        return self

class PMC902M(OracleTableReader):
    def __init__(self):
        super().__init__()
        self._columns = [
            ColumnsWithRaw('NO_KIND', ''),
            ColumnsWithRaw('NAME_KIND', 'big5')
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple


class SFCWF30(OracleTableReader):
    def __init__(self):
        super().__init__()
        self._columns = [
            ColumnsWithRaw('PRODUCT_NO', 'big5'),
            ColumnsWithRaw('DESIGN_NO', 'big5'),
            ColumnsWithRaw('PRODUCT_DES', 'big5'),
            ColumnsWithRaw('PRODUCT_SPEC', 'big5'),
            ColumnsWithRaw('PRODUCT_SPEC1', 'big5'),            
            ColumnsWithRaw('PRODUCT_SIZE', 'big5'),
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple


class HRM010M(OracleTableReader):
    def __init__(self):
        super().__init__()
        self._columns = [
            ColumnsWithRaw('LOCACOD', ''),
            ColumnsWithRaw('CLASCOD', ''),
            ColumnsWithRaw('CLASNAME', 'big5'),
            ColumnsWithRaw('WORK_HOURS', ''),
            ColumnsWithRaw('PREWKPLU', ''),
            ColumnsWithRaw('ON_DUTY_TIME', ''),
            ColumnsWithRaw('OFF_DUTY_HALF_DAY', ''),
            ColumnsWithRaw('REST_TIME', ''),
            ColumnsWithRaw('REST_TIME_FLAG', ''),
            ColumnsWithRaw('ON_DUTY_HALF_DAY', ''),
            ColumnsWithRaw('OFF_DUTY_TIME', ''),
            ColumnsWithRaw('OVER_TIME', ''),
            ColumnsWithRaw('START_FLEXTIME', ''),
            ColumnsWithRaw('END_FLEXTIME', ''),
            ColumnsWithRaw('START_FLEXTIME_OVTIME', ''),
            ColumnsWithRaw('END_FLEXTIME_OVTIME', ''),
            ColumnsWithRaw('START_FLEXTIME_NO_OVTIME', ''),
            ColumnsWithRaw('END_FLEXTIME_NO_OVTIME', ''),
            ColumnsWithRaw('WK_LATE_FLEXTIME_START', ''),
            ColumnsWithRaw('WK_LATE_FLEXTIME_END', ''),
            ColumnsWithRaw('WK_LATE_FLEXTIME_START_1', ''),
            ColumnsWithRaw('WK_LATE_FLEXTIME_END_1', ''),
            ColumnsWithRaw('WK_LATE_FLEXTIME_START_2', ''),
            ColumnsWithRaw('WK_LATE_FLEXTIME_END_2', ''),
            ColumnsWithRaw('LVAVE_EARLY_FLXTIME_START_HF', ''),
            ColumnsWithRaw('LVAVE_EARLY_FLXTIME_END_HF', ''),
            ColumnsWithRaw('LVAVE_EARLY_FLXTIME_START', ''),
            ColumnsWithRaw('LVAVE_EARLY_FLXTIME_END', ''),
            ColumnsWithRaw('START_FLEXTIME_2', ''),
            ColumnsWithRaw('END_FLEXTIME_2', ''),
            ColumnsWithRaw('BY_CALENDAR', ''),
            ColumnsWithRaw('BY_SHIFT', ''),
            ColumnsWithRaw('DELFLAG', ''),
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple

def main():
    if len(sys.argv) < 2:
        pass
    else:
        eval(sys.argv[1])

if __name__ == '__main__':
    sys.exit(main())




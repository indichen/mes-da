## DO NOT USE shebang line while DYLD_LIBRARY_PATH will be unset
#!/usr/bin/env python3

import sys
import cx_Oracle
import binascii
import csv
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

    def _db_filter(self):
        return ""

    def _get_sql(self):
        columns = ', '.join([c.column if not c.hex_encoding else 'rawtohex(utl_raw.cast_to_raw({}))'.format(c.column) for c in self._biz_columns])
        where_condition = ' where {}'.format(self._db_filter()) if self._db_filter() else ''
        return 'select {} from {}{}'.format(columns, self._table, where_condition)

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
        sql_statement = self._get_sql()
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
            ColumnsWithRaw('SINGLE_LINE_CIR_STD', '')
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple

class SFCWF30JOINM5M4(OracleTableReader):
    def __init__(self):
        super().__init__()
        self._columns = [
            ColumnsWithRaw('PRODUCT_NO', 'big5'),
            ColumnsWithRaw('PRODUCT_DES', 'big5'),
            ColumnsWithRaw('NO_MANU', 'big5'),
            ColumnsWithRaw('SINGLE_LINE_CIR_STD', 'big5'),
            ColumnsWithRaw('NO_KIND', 'big5'),
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _get_sql(self):
        cols = [
            'sfc.SFCWF30.PRODUCT_NO',
            'sfc.SFCWF30.PRODUCT_DES',
            'm4.no_manu',
            'sfc.SFCWF30.SINGLE_LINE_CIR_STD',
            'm5.no_kind',
        ]
        columns = ', '.join(['rawtohex(utl_raw.cast_to_raw({}))'.format(c) for c in cols])

        sql = "select {} from sfc.SFCWF30, sfc.pmc904m m4 left join (select m5.no_code, case when no_type = 'P' then '5' else 'G' end no_type, m5.name_mtrl, m5.name_kind, m5.no_kind from sfc.pmc905m m5 where m5.code_status = 'C' and m5.no_kind is not null) m5 on m4.no_kind = m5.no_kind and substr(m4.no_manu, 1, 1) = m5.no_type and substr(m4.no_manu, 2, 3) = m5.no_code where sfc.SFCWF30.DESIGN_NO = m4.no_manu".format(columns)
        return sql


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


class PMC180M(OracleTableReader):
    def __init__(self):
        super().__init__()
        self._oracledb_schema = 'pmc'
        self._columns = [
            ColumnsWithRaw('DRUM_MTRLNO', ''),
            ColumnsWithRaw('DRUM_TYPENO', ''),
            ColumnsWithRaw('DRUM_NAME', 'big5'),
            ColumnsWithRaw('CIR_OUTSIDE', ''),
            ColumnsWithRaw('CIR_INSIDE', ''),
            ColumnsWithRaw('INNER_WIDTH', ''),
            ColumnsWithRaw('SPACE_WIDTH', ''),
            ColumnsWithRaw('DRUM_MATERIAL', ''),
            ColumnsWithRaw('DRUM_KIND', ''),
            ColumnsWithRaw('DRUM_WEIGHT', ''),
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _db_filter(self):
        return 'DRUM_KIND=\'S\''

class SFCMF22(OracleTableReader):
    def __init__(self):
        super().__init__()
        self._oracledb_schema = 'sfc'
        self._columns = [
            ColumnsWithRaw('AXLE_NO', ''),
            ColumnsWithRaw('MACHINE_NO', ''),
        ]
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', [c.column for c in  self._columns])

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_tuple(self):
        return self._tuple

def dump_SFCWF30JOINM5M4():
    data_tuples = SFCWF30JOINM5M4().load_db_data().data_tuples
    print(len(data_tuples))
    with open('SFCWF30JOINM5M4.csv', 'w') as fd:
        writer = csv.DictWriter(fd, fieldnames=SFCWF30JOINM5M4()._biz_tuple._fields, dialect=csv.excel_tab)
        writer.writeheader()
        for t in data_tuples:
            writer.writerow(t._asdict())

def dump_SFCWF30():
    data_tuples = SFCWF30().load_db_data().data_tuples
    print(len(data_tuples))
    with open('SFCWF30.csv', 'w') as fd:
        writer = csv.DictWriter(fd, fieldnames=SFCWF30()._biz_tuple._fields, dialect=csv.excel_tab)
        writer.writeheader()
        for t in data_tuples:
            writer.writerow(t._asdict())


def main():
    if len(sys.argv) < 2:
        pass
    else:
        eval(sys.argv[1])

if __name__ == '__main__':
    sys.exit(main())




#!/usr/bin/env python3

import sys
import pymssql
import csv
from os import getenv
from abc import ABC, abstractmethod
from collections import namedtuple
from uuid import uuid4
from decimal import Decimal
from datetime import datetime, date

from read_old_mes import PMC902M, SFCWF30, SFCWF30JOINM5M4, PMC180M, SFCMF22


class MESTableGenerator(ABC):

    COLUMNS = ['create_time', 'create_user', 'last_modified', 'last_modify_user', 'ts', 'dr', 'tenant_id', 'id']

    _make_def_data = lambda self, given_id=None: \
        self._def_tuple( \
            ['convert(varchar, getdate(), 121)'], 'U001', \
            ['convert(varchar, getdate(), 121)'], 'U001', \
            ['convert(varchar, getdate(), 121)'], 0, 'tenant', \
            given_id or str(uuid4()).replace('-', '')
        )

    _escape_sql = staticmethod(lambda  x: \
        x.replace("'", "''").replace('\n', '').strip() \
    )

    _make_sql_value = staticmethod(lambda x: \
        'null' if x is None else \
        "N'{}'".format(MESTableGenerator._escape_sql(x)) if isinstance(x, str) else \
        x[0] if isinstance(x, list) else \
        x.strftime('%Y-%m-%d %H:%M:%S') if isinstance(x, datetime) or isinstance(x, date) else \
        str(x) \
    )

    def __init__(self, cust_table_name=None):
        if not cust_table_name:
            cust_table_name = self.__class__.__name__

        self._sqldb_db = getenv('SQLDB_DB')
        self._sqldb_schema = getenv('SQLDB_SCHEMA')
        self._sqldb_host = getenv('SQLDB_HOST')
        self._sqldb_port = getenv('SQLDB_PORT', '1433')
        self._sqldb_user = getenv('SQLDB_USER')
        self._sqldb_password = getenv('SQLDB_PASSWORD')
        self._table = '{}.{}.{}'.format(self._sqldb_db, self._sqldb_schema, cust_table_name)
        self._def_tuple = namedtuple('def_tuple', self.COLUMNS)
        self._truncate_db = True
        self._data_tuples = []
        self._lookup_table = {}


    ### Properties
    @property
    def truncate_db(self):
        return self._truncate_db
    
    @truncate_db.setter
    def truncate_db(self, value):
        self._truncate_db = False if not value else True

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
    def _biz_key_columns(self):
        pass

    @property
    @abstractmethod
    def _biz_tuple(self):
        pass

    @abstractmethod
    def _gen_init_tuples(self):
        pass


    ### Implementation
    def _get_merged_tuple(self):
        # Make merged tuple class with combining all columns
        # Biz columns/tuple implemented by child class
        merged_tuple = namedtuple("merged", self._def_tuple._fields + self._biz_tuple._fields)
        merged_columns = ', '.join(merged_tuple._fields)
        return (merged_tuple, merged_columns)

    def _gen_lookup_table(self):
        key_columns = self._biz_key_columns
        self._lookup_table = { tuple(map(lambda k: getattr(t,k), key_columns)):t for t in self._data_tuples }

    ### Public methods
    def load_db_data(self):
        (merged_tuple, merged_columns) = self._get_merged_tuple()

        # Query data from DB 
        conn = pymssql.connect(server=self._sqldb_host, port=self._sqldb_port, user=self._sqldb_user, password=self._sqldb_password)
        cursor = conn.cursor()
        sql_statement = 'select {} from {}'.format(merged_columns, self._table)
        cursor.execute(sql_statement)
        self._data_tuples = list(map(merged_tuple._make, cursor.fetchall()))
        # print('Count of data retrieved: {}'.format(len(self._data_tuples)))
        ## Gen lookup table/dict implemented by child class
        self._gen_lookup_table()
        return self


    def create_data(self, keep_key_values=False):
        (merged_tuple, merged_columns) = self._get_merged_tuple()

        # Get new data tuples from child class
        biz_tuples = self._gen_init_tuples()
        if keep_key_values:
            # Replace the key column values by looking up the cache table
            key_columns = self._biz_key_columns
            lookup_key_values = [ self._lookup_table.get(tuple(map(lambda k: getattr(t,k), key_columns)), None) for t in biz_tuples ]
            def_tuples = [self._make_def_data(v.id if v else None) for v in lookup_key_values]
        else:
            # If no need to keep key values, quickly make merged data tuples the same length as biz_tuples
            def_tuples = [self._make_def_data() for _ in range(len(biz_tuples))]

        # Merge tuples

        merged_tuples = [merged_tuple._make(m[0]+m[1]) for m in list(zip(def_tuples, biz_tuples))]
        self._data_tuples = merged_tuples
        ## Gen lookup table/dict implemented by child class
        self._gen_lookup_table()
        return self

    def get_key_columns(self):
        return self._biz_key_columns

    def lookup_key(self, *key_values):
        return self._lookup_table.get(tuple(key_values), None)

    def gen_new_sql(self):
        # Trucate table if option is true
        if self._truncate_db:
            print('truncate table {};'.format(self._table))

        # Gen SQL from data
        (merged_tuple, merged_columns) = self._get_merged_tuple()

        for t in self._data_tuples:
            merged_value = ', '.join([self._make_sql_value(getattr(t, f)) for f in t._fields])
            final_sql = 'insert into {} ({}) values ({});'.format(self._table, merged_columns, merged_value)
            print(final_sql)



## fm6_機台 (fm6_equipment)
class fm6_equipment(MESTableGenerator):

    def __init__(self):
        super().__init__()
        self._columns = ['code', 'name', 'short_name', 'spec', 'is_batch_equipment', 'checkin_out_type_cd', 'factory_cd', 'factory_name', 'note']
        self._key_columns = ['code']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns

    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        return [
            self._tuple('HI01', 'HIPA-1伸押機', 'HIPA-1', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('FR10', 'FR-100製粒機', 'FR-100製粒', '', 0, 'M', 'SCV1', '化材課', ''),
            self._tuple('PVC1', '200φ', '200φ', '', 0, 'M', 'SCV1', '化材課', ''),
            self._tuple('PVC2', '180φ', '180φ', '', 0, 'M', 'SCV1', '化材課', ''),
            self._tuple('RU22', '22"滾筒', '22"滾筒', '', 0, 'M', 'SCV1', '化材課', ''),
            self._tuple('ZZ30', '電一伸線倒軸機', '電一伸線倒軸機', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('A130', 'A-13伸線機', 'A-13', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('FS13', 'FS-13伸線機', 'FS13', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('M850', 'M-85伸線機', 'M85', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('CS03', '19B銅絞機', '19B', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS04', '37B銅絞機', '37B', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS05', '61B銅絞機', '61B', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS08', '7B-1銅絞機', '7B-1', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS09', '7B銅絞機', '7B', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TN01', '1#630 PCT鍍錫機', '1#鍍錫機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TN02', '2#630 PCT鍍錫機', '2#鍍錫機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE01', 'CDCC', 'CDCC', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE02', 'CCV', 'CCV', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE03', 'HCV65 交連機', 'HCV65', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE05', 'HCV90 交連機', 'HCV90', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE06', 'RCP', 'RCP', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE07', 'HCV100 交連機', 'HCV100', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('GR03', '2.8M集合機', '2.8M', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('GR04', '84B鎧裝機', '84B', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('GR09', '1+8集合機', '1+8集合', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TN03', '3#630 拋光倒軸機', '3#拋光機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TP01', '綜合包帶機', '綜合包帶', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TP02', '中心包帶機', '中心包帶', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WR01', '密捲機', '密捲機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WE01', '115押出機', 'ψ115', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WE02', '150押出機', 'ψ150', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WE08', '120押出機', 'ψ120', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ZZ50', '電一押出倒軸機', '門型倒軸', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('PK01', '搖盤機(電力)', '搖盤機(電力)', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('PK02', '軸裝包裝(電力)', '軸裝包裝(電力)', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('DR01', '12頭伸線機', '12R', '', 0, 'S', 'SCG1', '電力二課', ''),
            self._tuple('DR02', '8頭伸線機', '8R', '', 0, 'S', 'SCG1', '電力二課', ''),
            self._tuple('DR71', 'C 17-1中伸機', 'C 17-1', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('DR72', 'C 17-2中伸機', 'C 17-2', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('DR73', 'C 17-3中伸機', 'C 17-3', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('ST02', '電鍍錫機', '電鍍錫機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('ZZ10', '電二伸線倒軸機', '電二伸線倒軸機', '', 0, 'S', 'SCG1', '電力二課', ''),
            self._tuple('BS02', '13#吉田束絞機(800Φ)', 'GBS#13', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS06', '1#束絞機', 'GBS#1', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS10', '4#束絞機', 'GBS#4', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS11', '5#束絞機', 'GBS#5', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS12', '6#束絞機', 'GBS#6', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS19', '10#束絞機', 'GBS#10', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS20', '9#束絞機', 'GBS#9', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS21', '8#束絞機', 'GBS#8', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS24', '11#束絞機', 'GBS#11', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS25', '12#束絞機', 'GBS#12', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS26', '7#束絞機', 'GBS#7', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS27', '3#束絞機', 'GBS#3', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('ZZ11', '電二束絞倒軸機', '電二束絞倒軸機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE07', '92#押出機(60+30+NOKIA)', 'G92', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE09', '61#押出機(JR65φ)', 'G61', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE10', '62#押出機(JR65φ)', 'G62', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE11', '65#押出機(65φ)', 'G65', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE12', '91#押出機(JR90φ)', 'G91', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE15', 'G93', 'G93', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE16', '90#押出機(G63)', 'G63', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE17', '64#押出機', 'G64', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE18', '66#押出機', 'G66', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE19', '67#押出機', 'G67', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE20', '68#押出機', 'G68', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('ZZ40', '電二集合倒軸機', '電二集合倒軸機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS99', '1250(昇祥束絞機)', '1250集合機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GP01', 'GP01', '小包機#1', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GP02', 'GP02', '小包機#2', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GP03', '高速小包機', '高速小包機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR01', '1.2M', '1.2M', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR05', '915MM', '915集合機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR06', '1.6M', '1.6M', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR08', '1+3弓絞機', '1+3', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('CW01', '溝槽押出機', '溝槽押出機', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('WE05', 'G94', 'G94', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE06', '95#押出機(MF90)', 'G95', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE21', 'G96', 'G96', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE22', 'G97', 'G97', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE23', 'G98', 'G98', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('PK03', '搖盤機加包膜(配線)', '搖盤機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('PK04', '軸裝包裝(配線)', '軸裝包裝', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('QS03', 'QS-3星絞機', 'QS-3', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('QS02', 'QS-2星絞機', 'QS-2', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('QS04', 'QS-4星絞機', 'QS-4', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('QS01', 'QS-1星絞機', 'QS-1', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('QS12', 'QS-12星絞機', 'QS-12', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('QS11', 'QS-11星絞機', 'QS-11', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('QS07', 'QS-7星絞機', 'QS-7', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('GR20', '20B集合機', '20B', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('SZ01', 'SZ-1集合機', 'SZ-1', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('GR12', '12B集合機', '12B', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('SZ02', 'SZ-2集合機', 'SZ-2', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('GR07', '48B', '48B', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('SZ03', 'SZ-3集合機', 'SZ-3', '', 0, 'M', 'SCT1', '通信課', ''),
            self._tuple('LE01', '束管押出機', '束管押出機', '', 0, 'M', 'SCT1', '通信課', ''),
        ]
# End of fm6_equipment

## fm6_機台狀態 (fm6_equipment_status)
class fm6_equipment_status(MESTableGenerator):

    def __init__(self):
        super().__init__()
        self._columns = ['equipment_pk', 'status_cd', 'reason']
        self._key_columns = ['equipment_pk']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        equipment_data = fm6_equipment().load_db_data().data_tuples
        return [ self._biz_tuple(e.id, 'S', '') for e in equipment_data ]

## fm8_標準工序 (fm8_basic_process)
class fm8_basic_process(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['code', 'name', 'name_en', 'is_enabled', 'is_virtual_process', 'station_pk', 'station_cd', 'station_name']
        self._key_columns = ['code']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        return [
            self._tuple('WG', '第二雲母', 'WG', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('DR', '伸線', 'DR', 1, 0, ['NULL'], 's_DR', '伸線'),
            self._tuple('L2', '第二束管', 'L2', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('TS', '束管集合', 'TS', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('CG', '波管成型', 'CG', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('WR', '包帶', 'WR', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('GX', '第二絞合', 'GX', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('RN', '印字', 'RN', 1, 1, ['NULL'], 's_Others', '其他'),
            self._tuple('WI', '內被', 'WI', 1, 0, ['NULL'], 's_WI', '押出_內被'),
            self._tuple('E1', '第一絕緣', 'E1', 1, 0, ['NULL'], 's_WE', '押出_絕緣'),
            self._tuple('RW', '倒軸', 'RW', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('B3', '第三編織(委外)', 'B3', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('W2', '第二外被', 'W2', 1, 0, ['NULL'], 's_WO', '押出_外被'),
            self._tuple('W4', '第四帶類', 'W4', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('G3', '第三絞合', 'G3', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('CS', '銅絞', 'CS', 1, 0, ['NULL'], 's_CS', '銅絞'),
            self._tuple('PT', '塗油漆', 'PT', 1, 0, ['NULL'], 's_NA', '沒使用'),
            self._tuple('X2', '交連第二絕緣', 'X2', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('PK', '包裝', 'PK', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('XX', '交連複合絕緣', 'XX', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('P2', '第二對絞', 'P2', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('IR', '照射(委外)', 'IR', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('WS', '第二帶類', 'WS', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('I2', '第二照射', 'I2', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('X4', '交連第四絕緣', 'X4', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('WU', '波紋銅被', 'WU', 1, 0, ['NULL'], 's_NA', '沒使用'),
            self._tuple('B2', '第二編織(委外)', 'B2', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('E2', '第二絕緣', 'E2', 1, 0, ['NULL'], 's_WE', '押出_絕緣'),
            self._tuple('GB', '鐵線編織', 'GB', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('GR', '絞合', 'GR', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('X3', '交連第三絕緣', 'X3', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('WP', '銅線纏繞', 'WP', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('WM', '包雲母帶', 'WM', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('LP', '積層被覆', 'LP', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('G4', '第四絞合', 'G4', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('XE', '交連押出', 'XE', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('WN', '包數字帶', 'WN', 1, 0, ['NULL'], 's_NA', '沒使用'),
            self._tuple('SE', '溝槽押出', 'SE', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('GA', '鎧裝', 'GA', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('E3', '第三絕緣', 'E3', 1, 0, ['NULL'], 's_WE', '押出_絕緣'),
            self._tuple('TN', '熱鍍', 'TN', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('W3', '第三帶類', 'W3', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('GP', '對絞', 'GP', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('CL', '著色', 'CL', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('XF', '橡膠充實押出', 'XF', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('TE', '電鍍', 'TE', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('XT', '橡膠複合內被', 'XT', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('GT', '三芯絞', 'GT', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('IN', '檢驗', 'IN', 1, 0, ['NULL'], 's_WP', '集合'),
            self._tuple('WT', '包銅帶', 'WT', 1, 0, ['NULL'], 's_WR', '包帶'),
            self._tuple('XO', '橡膠外被', 'XO', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('RX', '第二倒軸', 'RX', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('WL', '波紋鋁被', 'WL', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('BR', '編織(委外)', 'BR', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('XI', '橡膠內被', 'XI', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('LE', '束管押出', 'LE', 1, 0, ['NULL'], 's_WL', '通信'),
            self._tuple('CA', '組裝(委外)', 'CA', 1, 0, ['NULL'], 's_Others', '其他'),
            self._tuple('WO', '外被', 'WO', 1, 0, ['NULL'], 's_WO', '押出_外被'),
            self._tuple('WX', '塑膠複合絕緣', 'WX', 1, 0, ['NULL'], 's_WE', '押出_絕緣'),
            self._tuple('XC', '異形押出', 'XC', 1, 0, ['NULL'], 's_XE', '交連'),
            self._tuple('WE', '絕緣', 'WE', 1, 0, ['NULL'], 's_WE', '押出_絕緣'),
        ] # TODO: Add init data here

## fm6_機台製程對應 (fm6_equipment_process)
class fm6_equipment_process(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['equipment_pk', 'equipment_cd', 'process_pk', 'process_cd']
        self._key_columns = ['equipment_cd', 'process_cd'] # TODO: Set key columns here
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        equipments = fm6_equipment().load_db_data()
        processes = fm8_basic_process().load_db_data()
        expand_data = lambda machine_cd, process_cd: \
            (
            equipments.lookup_key(machine_cd).id if equipments.lookup_key(machine_cd) else None, \
            machine_cd, \
            processes.lookup_key(process_cd).id if processes.lookup_key(process_cd) else None, \
            process_cd
            )

        data_tuples = [
            self._tuple(*expand_data('WE06', 'XE')),
            self._tuple(*expand_data('GR06', 'WR')),
            self._tuple(*expand_data('WE01', 'XE')),
            self._tuple(*expand_data('QS01', 'GP')),
            self._tuple(*expand_data('QS02', 'GP')),
            self._tuple(*expand_data('QS04', 'GP')),
            self._tuple(*expand_data('QS05', 'GP')),
            self._tuple(*expand_data('QS06', 'GP')),
            self._tuple(*expand_data('QS07', 'GP')),
            self._tuple(*expand_data('QS08', 'GP')),
            self._tuple(*expand_data('QS09', 'GP')),
            self._tuple(*expand_data('QS10', 'GP')),
            self._tuple(*expand_data('QS11', 'GP')),
            self._tuple(*expand_data('QS12', 'GP')),
            self._tuple(*expand_data('QS13', 'GP')),
            self._tuple(*expand_data('QS14', 'GP')),
            self._tuple(*expand_data('QS15', 'GP')),
            self._tuple(*expand_data('QS16', 'GP')),
            self._tuple(*expand_data('GR09', 'GP')),
            self._tuple(*expand_data('TP01', 'W3')),
            self._tuple(*expand_data('TP02', 'GA')),
            self._tuple(*expand_data('TP02', 'GR')),
            self._tuple(*expand_data('TP02', 'W3')),
            self._tuple(*expand_data('TP02', 'WG')),
            self._tuple(*expand_data('TP02', 'WM')),
            self._tuple(*expand_data('TP02', 'WR')),
            self._tuple(*expand_data('TP02', 'WS')),
            self._tuple(*expand_data('TP02', 'WT')),
            self._tuple(*expand_data('BS11', 'PK')),
            self._tuple(*expand_data('WE16', 'XO')),
            self._tuple(*expand_data('WE15', 'XE')),
            self._tuple(*expand_data('GR09', 'WM')),
            self._tuple(*expand_data('GR09', 'WR')),
            self._tuple(*expand_data('GR09', 'WS')),
            self._tuple(*expand_data('WE21', 'WI')),
            self._tuple(*expand_data('LP01', 'WE')),
            self._tuple(*expand_data('GP03', 'GP')),
            self._tuple(*expand_data('GP03', 'WM')),
            self._tuple(*expand_data('GP03', 'WN')),
            self._tuple(*expand_data('GP03', 'WR')),
            self._tuple(*expand_data('GR04', 'WS')),
            self._tuple(*expand_data('GR04', 'G3')),
            self._tuple(*expand_data('TN03', 'TN')),
            self._tuple(*expand_data('BS21', 'PK')),
            self._tuple(*expand_data('BS27', 'PK')),
            self._tuple(*expand_data('PK02', 'RW')),
            self._tuple(*expand_data('WE22', 'R1')),
            self._tuple(*expand_data('WE16', 'WO')),
            self._tuple(*expand_data('XE02', 'R1')),
            self._tuple(*expand_data('XE03', 'X2')),
            self._tuple(*expand_data('XE03', 'X3')),
            self._tuple(*expand_data('GR20', 'G3')),
            self._tuple(*expand_data('WE02', 'W2')),
            self._tuple(*expand_data('ZZ50', 'WE')),
            self._tuple(*expand_data('SZ01', 'GA')),
            self._tuple(*expand_data('BR01', 'GB')),
            self._tuple(*expand_data('ZZ10', 'R1')),
            self._tuple(*expand_data('ZZ11', 'R1')),
            self._tuple(*expand_data('ZZ40', 'R1')),
            self._tuple(*expand_data('LE01', 'WE')),
            self._tuple(*expand_data('WE02', 'XF')),
            self._tuple(*expand_data('ZZ51', 'WO')),
            self._tuple(*expand_data('WE23', 'WE')),
            self._tuple(*expand_data('WE23', 'WI')),
            self._tuple(*expand_data('WE23', 'WO')),
            self._tuple(*expand_data('WE23', 'WX')),
            self._tuple(*expand_data('WE23', 'WY')),
            self._tuple(*expand_data('GR09', 'CS')),
            self._tuple(*expand_data('GR09', 'GR')),
            self._tuple(*expand_data('GR01', 'BR')),
            self._tuple(*expand_data('GR06', 'BR')),
            self._tuple(*expand_data('DR72', 'PK')),
            self._tuple(*expand_data('PK02', 'R1')),
            self._tuple(*expand_data('ZZ20', 'ZZ')),
            self._tuple(*expand_data('WE02', 'ZZ')),
            self._tuple(*expand_data('WE01', 'ZZ')),
            self._tuple(*expand_data('ZZ50', 'ZZ')),
            self._tuple(*expand_data('TN03', 'ZZ')),
            self._tuple(*expand_data('BS11', 'ZZ')),
            self._tuple(*expand_data('BS21', 'ZZ')),
            self._tuple(*expand_data('BS27', 'ZZ')),
            self._tuple(*expand_data('DR72', 'ZZ')),
            self._tuple(*expand_data('WE08', 'ZZ')),
            self._tuple(*expand_data('PK04', 'R1')),
            self._tuple(*expand_data('PK01', 'R1')),
            self._tuple(*expand_data('BS20', 'ZZ')),
            self._tuple(*expand_data('BS24', 'ZZ')),
            self._tuple(*expand_data('GR04', 'ZZ')),
            self._tuple(*expand_data('BS19', 'ZZ')),
            self._tuple(*expand_data('WE08', 'XF')),
            self._tuple(*expand_data('GR08', 'GT')),
            self._tuple(*expand_data('QS02', 'GR')),
            self._tuple(*expand_data('QS03', 'GR')),
            self._tuple(*expand_data('QS04', 'GR')),
            self._tuple(*expand_data('QS05', 'GR')),
            self._tuple(*expand_data('QS06', 'GR')),
            self._tuple(*expand_data('QS07', 'GR')),
            self._tuple(*expand_data('QS08', 'GR')),
            self._tuple(*expand_data('QS09', 'GR')),
            self._tuple(*expand_data('QS10', 'GR')),
            self._tuple(*expand_data('QS11', 'GR')),
            self._tuple(*expand_data('QS12', 'GR')),
            self._tuple(*expand_data('QS13', 'GR')),
            self._tuple(*expand_data('QS14', 'GR')),
            self._tuple(*expand_data('QS15', 'GR')),
            self._tuple(*expand_data('QS16', 'GR')),
            self._tuple(*expand_data('GR03', 'W3')),
            self._tuple(*expand_data('ZZ10', 'TN')),
            self._tuple(*expand_data('ZZ51', 'R1')),
            self._tuple(*expand_data('WE08', 'W2')),
            self._tuple(*expand_data('XE07', 'WE')),
            self._tuple(*expand_data('XE07', 'XE')),
            self._tuple(*expand_data('XE07', 'XI')),
            self._tuple(*expand_data('XE07', 'XO')),
            self._tuple(*expand_data('PA01', 'R1')),
            self._tuple(*expand_data('GR09', 'GT')),
            self._tuple(*expand_data('BS03', 'CS')),
            self._tuple(*expand_data('BS04', 'CS')),
            self._tuple(*expand_data('BS05', 'CS')),
            self._tuple(*expand_data('BS06', 'CS')),
            self._tuple(*expand_data('BS07', 'CS')),
            self._tuple(*expand_data('BS08', 'CS')),
            self._tuple(*expand_data('BS09', 'CS')),
            self._tuple(*expand_data('BS10', 'CS')),
            self._tuple(*expand_data('BS11', 'CS')),
            self._tuple(*expand_data('BS12', 'CS')),
            self._tuple(*expand_data('BS13', 'CS')),
            self._tuple(*expand_data('BS14', 'CS')),
            self._tuple(*expand_data('BS15', 'CS')),
            self._tuple(*expand_data('BS16', 'CS')),
            self._tuple(*expand_data('BS17', 'CS')),
            self._tuple(*expand_data('BS18', 'CS')),
            self._tuple(*expand_data('BS19', 'CS')),
            self._tuple(*expand_data('BS20', 'CS')),
            self._tuple(*expand_data('BS21', 'CS')),
            self._tuple(*expand_data('BS22', 'CS')),
            self._tuple(*expand_data('BS23', 'CS')),
            self._tuple(*expand_data('BS24', 'CS')),
            self._tuple(*expand_data('BS25', 'CS')),
            self._tuple(*expand_data('BS26', 'CS')),
            self._tuple(*expand_data('BS27', 'CS')),
            self._tuple(*expand_data('BS28', 'CS')),
            self._tuple(*expand_data('BS99', 'GR')),
            self._tuple(*expand_data('BS99', 'GP')),
            self._tuple(*expand_data('CG01', 'CG')),
            self._tuple(*expand_data('CS03', 'CS')),
            self._tuple(*expand_data('CS04', 'CS')),
            self._tuple(*expand_data('CS05', 'CS')),
            self._tuple(*expand_data('CS09', 'CS')),
            self._tuple(*expand_data('CS10', 'CS')),
            self._tuple(*expand_data('DR01', 'DR')),
            self._tuple(*expand_data('DR02', 'DR')),
            self._tuple(*expand_data('DR03', 'DR')),
            self._tuple(*expand_data('DR04', 'DR')),
            self._tuple(*expand_data('DR31', 'DR')),
            self._tuple(*expand_data('DR32', 'DR')),
            self._tuple(*expand_data('DR33', 'DR')),
            self._tuple(*expand_data('DR34', 'DR')),
            self._tuple(*expand_data('GR07', 'R1')),
            self._tuple(*expand_data('DR71', 'DR')),
            self._tuple(*expand_data('DR72', 'DR')),
            self._tuple(*expand_data('FS13', 'DR')),
            self._tuple(*expand_data('GP01', 'WR')),
            self._tuple(*expand_data('GP02', 'WR')),
            self._tuple(*expand_data('GR01', 'GR')),
            self._tuple(*expand_data('GR01', 'GP')),
            self._tuple(*expand_data('GR03', 'GR')),
            self._tuple(*expand_data('GR03', 'WR')),
            self._tuple(*expand_data('GR04', 'GA')),
            self._tuple(*expand_data('GR04', 'WR')),
            self._tuple(*expand_data('GR05', 'GR')),
            self._tuple(*expand_data('GR05', 'GP')),
            self._tuple(*expand_data('GR06', 'GR')),
            self._tuple(*expand_data('GR07', 'GR')),
            self._tuple(*expand_data('GR07', 'GA')),
            self._tuple(*expand_data('GR08', 'GR')),
            self._tuple(*expand_data('M850', 'DR')),
            self._tuple(*expand_data('TN01', 'TN')),
            self._tuple(*expand_data('TP01', 'WR')),
            self._tuple(*expand_data('WE01', 'WE')),
            self._tuple(*expand_data('WE02', 'WE')),
            self._tuple(*expand_data('WE04', 'WE')),
            self._tuple(*expand_data('WE05', 'WE')),
            self._tuple(*expand_data('WE06', 'WE')),
            self._tuple(*expand_data('WE07', 'WE')),
            self._tuple(*expand_data('WE08', 'WE')),
            self._tuple(*expand_data('WE09', 'WE')),
            self._tuple(*expand_data('WE10', 'WE')),
            self._tuple(*expand_data('WE11', 'WE')),
            self._tuple(*expand_data('WE12', 'WE')),
            self._tuple(*expand_data('WE13', 'WE')),
            self._tuple(*expand_data('WE15', 'WE')),
            self._tuple(*expand_data('WE16', 'WE')),
            self._tuple(*expand_data('WE17', 'WE')),
            self._tuple(*expand_data('WE18', 'WE')),
            self._tuple(*expand_data('WE19', 'WE')),
            self._tuple(*expand_data('WE20', 'WE')),
            self._tuple(*expand_data('WE01', 'WO')),
            self._tuple(*expand_data('WE02', 'WO')),
            self._tuple(*expand_data('PK01', 'PK')),
            self._tuple(*expand_data('WE05', 'WO')),
            self._tuple(*expand_data('WE06', 'WO')),
            self._tuple(*expand_data('WE08', 'WO')),
            self._tuple(*expand_data('WE09', 'WO')),
            self._tuple(*expand_data('WE10', 'WO')),
            self._tuple(*expand_data('WE11', 'WO')),
            self._tuple(*expand_data('WE12', 'WO')),
            self._tuple(*expand_data('WE19', 'WO')),
            self._tuple(*expand_data('WE20', 'WO')),
            self._tuple(*expand_data('WR01', 'WR')),
            self._tuple(*expand_data('XE01', 'XE')),
            self._tuple(*expand_data('XE02', 'XE')),
            self._tuple(*expand_data('XE03', 'XE')),
            self._tuple(*expand_data('XE03', 'WE')),
            self._tuple(*expand_data('XE05', 'XE')),
            self._tuple(*expand_data('XE05', 'WE')),
            self._tuple(*expand_data('XE06', 'XE')),
            self._tuple(*expand_data('WE08', 'PK')),
            self._tuple(*expand_data('WE01', 'PK')),
            self._tuple(*expand_data('WE02', 'PK')),
            self._tuple(*expand_data('GP01', 'GP')),
            self._tuple(*expand_data('GP01', 'WM')),
            self._tuple(*expand_data('GR03', 'WT')),
            self._tuple(*expand_data('GR04', 'WP')),
            self._tuple(*expand_data('TP01', 'WT')),
            self._tuple(*expand_data('WE01', 'WX')),
            self._tuple(*expand_data('WE02', 'WX')),
            self._tuple(*expand_data('WE05', 'WY')),
            self._tuple(*expand_data('WE06', 'WY')),
            self._tuple(*expand_data('WE08', 'WX')),
            self._tuple(*expand_data('WE12', 'WY')),
            self._tuple(*expand_data('XE01', 'XO')),
            self._tuple(*expand_data('XE02', 'XI')),
            self._tuple(*expand_data('XE03', 'XI')),
            self._tuple(*expand_data('XE05', 'XI')),
            self._tuple(*expand_data('WR01', 'WT')),
            self._tuple(*expand_data('GR01', 'WR')),
            self._tuple(*expand_data('GR05', 'WR')),
            self._tuple(*expand_data('GR07', 'WP')),
            self._tuple(*expand_data('TP01', 'WM')),
            self._tuple(*expand_data('WE01', 'WI')),
            self._tuple(*expand_data('WE02', 'WI')),
            self._tuple(*expand_data('WE05', 'WX')),
            self._tuple(*expand_data('WE06', 'WI')),
            self._tuple(*expand_data('WE06', 'WX')),
            self._tuple(*expand_data('WE08', 'WI')),
            self._tuple(*expand_data('WE12', 'WX')),
            self._tuple(*expand_data('XE02', 'XO')),
            self._tuple(*expand_data('XE03', 'XX')),
            self._tuple(*expand_data('XE03', 'XO')),
            self._tuple(*expand_data('XE05', 'XX')),
            self._tuple(*expand_data('XE05', 'XO')),
            self._tuple(*expand_data('GP01', 'WN')),
            self._tuple(*expand_data('GP02', 'WM')),
            self._tuple(*expand_data('GP02', 'WN')),
            self._tuple(*expand_data('GP02', 'GP')),
            self._tuple(*expand_data('ZZ01', 'XE')),
            self._tuple(*expand_data('A130', 'DR')),
            self._tuple(*expand_data('0000', 'MT')),
            self._tuple(*expand_data('ZZ10', 'DR')),
            self._tuple(*expand_data('ZZ15', 'DR')),
            self._tuple(*expand_data('ZZ20', 'DR')),
            self._tuple(*expand_data('ZZ20', 'TN')),
            self._tuple(*expand_data('BS99', 'CS')),
            self._tuple(*expand_data('BS02', 'CS')),
            self._tuple(*expand_data('BS01', 'CS')),
            self._tuple(*expand_data('CS00', 'DR')),
            self._tuple(*expand_data('CS01', 'CS')),
            self._tuple(*expand_data('DR05', 'DR')),
            self._tuple(*expand_data('GR02', 'GR')),
            self._tuple(*expand_data('ZZ40', 'DR')),
            self._tuple(*expand_data('WR01', 'WM')),
            self._tuple(*expand_data('WR01', 'GR')),
            self._tuple(*expand_data('GR04', 'WT')),
            self._tuple(*expand_data('GR04', 'WM')),
            self._tuple(*expand_data('PK03', 'R1')),
            self._tuple(*expand_data('CS03', 'GR')),
            self._tuple(*expand_data('ZZ20', 'RW')),
            self._tuple(*expand_data('CS03', 'GP')),
            self._tuple(*expand_data('GR04', 'GR')),
            self._tuple(*expand_data('BS01', 'GR')),
            self._tuple(*expand_data('BS01', 'MT')),
            self._tuple(*expand_data('WE02', 'RW')),
            self._tuple(*expand_data('WE01', 'RW')),
            self._tuple(*expand_data('WE08', 'XO')),
            self._tuple(*expand_data('GR05', 'WP')),
            self._tuple(*expand_data('GR05', 'GT')),
            self._tuple(*expand_data('GR01', 'GT')),
            self._tuple(*expand_data('GR03', 'WM')),
            self._tuple(*expand_data('TP01', 'GR')),
            self._tuple(*expand_data('GR06', 'GX')),
            self._tuple(*expand_data('WR01', 'WG')),
            self._tuple(*expand_data('XE02', 'X2')),
            self._tuple(*expand_data('CS00', 'TN')),
            self._tuple(*expand_data('WE16', 'XE')),
            self._tuple(*expand_data('ZZ30', 'DR')),
            self._tuple(*expand_data('ZZ41', 'WO')),
            self._tuple(*expand_data('ZZ41', 'GR')),
            self._tuple(*expand_data('TN02', 'TN')),
            self._tuple(*expand_data('ST02', 'TE')),
            self._tuple(*expand_data('WE02', 'XO')),
            self._tuple(*expand_data('WE12', 'XE')),
            self._tuple(*expand_data('TP01', 'GA')),
            self._tuple(*expand_data('ZZ11', 'CS')),
            self._tuple(*expand_data('GR03', 'GA')),
            self._tuple(*expand_data('ZZ50', 'RW')),
            self._tuple(*expand_data('XE02', 'WE')),
            self._tuple(*expand_data('GR06', 'WT')),
            self._tuple(*expand_data('GR08', 'GP')),
            self._tuple(*expand_data('WE21', 'WE')),
            self._tuple(*expand_data('WE21', 'WO')),
            self._tuple(*expand_data('WE21', 'WX')),
            self._tuple(*expand_data('WE21', 'WY')),
            self._tuple(*expand_data('WE02', 'RX')),
            self._tuple(*expand_data('WE01', 'RX')),
            self._tuple(*expand_data('ZZ50', 'RX')),
            self._tuple(*expand_data('GR03', 'WP')),
            self._tuple(*expand_data('TP01', 'WG')),
            self._tuple(*expand_data('TP01', 'WS')),
            self._tuple(*expand_data('XE01', 'WO')),
            self._tuple(*expand_data('GR03', 'GX')),
            self._tuple(*expand_data('CS03', 'GT')),
            self._tuple(*expand_data('LE01', 'XE')),
            self._tuple(*expand_data('LE01', 'LE')),
            self._tuple(*expand_data('PA01', 'PT')),
            self._tuple(*expand_data('ZZ50', 'PK')),
            self._tuple(*expand_data('PA01', 'WE')),
            self._tuple(*expand_data('SZ03', 'GX')),
            self._tuple(*expand_data('XE02', 'XF')),
            self._tuple(*expand_data('BS20', 'PK')),
            self._tuple(*expand_data('BS24', 'PK')),
            self._tuple(*expand_data('GR12', 'GT')),
            self._tuple(*expand_data('WE07', 'WX')),
            self._tuple(*expand_data('SZ03', 'WR')),
            self._tuple(*expand_data('ST02', 'DR')),
            self._tuple(*expand_data('ZZ50', 'WO')),
            self._tuple(*expand_data('XE07', 'XX')),
            self._tuple(*expand_data('SZ01', 'WP')),
            self._tuple(*expand_data('QS04', 'P2')),
            self._tuple(*expand_data('QS03', 'P2')),
            self._tuple(*expand_data('QS02', 'P2')),
            self._tuple(*expand_data('QS01', 'P2')),
            self._tuple(*expand_data('SZ03', 'WS')),
            self._tuple(*expand_data('CS08', 'GR')),
            self._tuple(*expand_data('GR04', 'CS')),
            self._tuple(*expand_data('GR03', 'WG')),
            self._tuple(*expand_data('CW01', 'WE')),
            self._tuple(*expand_data('CW01', 'WI')),
            self._tuple(*expand_data('CW01', 'WO')),
            self._tuple(*expand_data('CW01', 'WX')),
            self._tuple(*expand_data('GR20', 'BR')),
            self._tuple(*expand_data('PK03', 'RW')),
            self._tuple(*expand_data('WE22', 'WE')),
            self._tuple(*expand_data('WE22', 'WO')),
            self._tuple(*expand_data('WE22', 'WX')),
            self._tuple(*expand_data('WE22', 'WY')),
            self._tuple(*expand_data('WE23', 'I2')),
            self._tuple(*expand_data('ST02', 'TN')),
            self._tuple(*expand_data('ZZ11', 'PK')),
            self._tuple(*expand_data('WR01', 'WS')),
            self._tuple(*expand_data('DR72', 'TN')),
            self._tuple(*expand_data('WE22', 'WI')),
            self._tuple(*expand_data('WE01', 'W2')),
            self._tuple(*expand_data('WE15', 'WX')),
            self._tuple(*expand_data('GR12', 'GR')),
            self._tuple(*expand_data('SZ03', 'GP')),
            self._tuple(*expand_data('SZ03', 'GT')),
            self._tuple(*expand_data('GR20', 'GX')),
            self._tuple(*expand_data('WE06', 'W2')),
            self._tuple(*expand_data('ZZ40', 'RW')),
            self._tuple(*expand_data('XE03', 'XF')),
            self._tuple(*expand_data('XE02', 'XX')),
            self._tuple(*expand_data('GR03', 'WS')),
            self._tuple(*expand_data('GR07', 'WS')),
            self._tuple(*expand_data('WE16', 'WX')),
            self._tuple(*expand_data('BR02', 'GB')),
            self._tuple(*expand_data('BR03', 'GB')),
            self._tuple(*expand_data('CS08', 'CS')),
            self._tuple(*expand_data('TN03', 'RW')),
            self._tuple(*expand_data('WE05', 'WI')),
            self._tuple(*expand_data('GR20', 'GR')),
            self._tuple(*expand_data('QS01', 'GR')),
            self._tuple(*expand_data('WE08', 'XE')),
            self._tuple(*expand_data('WE10', 'XE')),
            self._tuple(*expand_data('WE17', 'LE')),
            self._tuple(*expand_data('GR07', 'WR')),
            self._tuple(*expand_data('WE10', 'WX')),
            self._tuple(*expand_data('WE17', 'E1')),
            self._tuple(*expand_data('WE17', 'E2')),
            self._tuple(*expand_data('WE17', 'E3')),
            self._tuple(*expand_data('WE10', 'E1')),
            self._tuple(*expand_data('WE10', 'E2')),
            self._tuple(*expand_data('WE10', 'E3')),
            self._tuple(*expand_data('QS03', 'GP')),
            self._tuple(*expand_data('QS11', 'WS')),
            self._tuple(*expand_data('QS12', 'WS')),
            self._tuple(*expand_data('DR73', 'DR')),
            self._tuple(*expand_data('DR73', 'PK')),
            self._tuple(*expand_data('DR73', 'TN')),
            self._tuple(*expand_data('DR73', 'ZZ')),
            self._tuple(*expand_data('QS17', 'GP')),
            self._tuple(*expand_data('QS17', 'GR')),
            self._tuple(*expand_data('ZZ50', 'W2')),
            self._tuple(*expand_data('GR03', 'BR')),
            self._tuple(*expand_data('GR04', 'PK')),
            self._tuple(*expand_data('BS19', 'PK')),
            self._tuple(*expand_data('GR12', 'GP')),
            self._tuple(*expand_data('SZ01', 'GR')),
            self._tuple(*expand_data('SZ02', 'GR')),
            self._tuple(*expand_data('SZ03', 'GR')),
            self._tuple(*expand_data('LE01', 'L2')),
            self._tuple(*expand_data('XE03', 'XT')),
            self._tuple(*expand_data('GR07', 'WM')),
            self._tuple(*expand_data('XE03', 'R1')),
            self._tuple(*expand_data('GR06', 'WM')),
        ]
        return list(filter(lambda t: t.equipment_pk and t.process_pk, data_tuples))

## fm7_物料基本分類 (fm7_material_cat)
class fm7_material_cat(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['code', 'name', 'parent_cat_pk', 'is_enabled', 'note']
        self._key_columns = ['code']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        old_tuples = PMC902M().load_db_data().data_tuples
        return [ self._tuple(o.NO_KIND, o.NAME_KIND, ['NULL'], 1, '') for o in old_tuples ]

## fm7_物料基本信息 (fm7_material)
class fm7_material(MESTableGenerator):
    def __init__(self):
        super().__init__()
        # self._columns = ['code', 'name', 'cat_pk', 'name_en', 'name_abbr', 'unit_pk', 'spec', 'spec_en', 'model', 'image_path', 'brand', 'is_enabled', 'custom_product_id', 'custom_product_name', 'barcode', 'mnemonic_code', 'version', 'application_form_id', 'attr1', 'attr2']
        self._columns = ['code', 'name', 'cat_pk', 'model', 'is_enabled', 'version', 'attr1', 'is_semiproduct']
        self._key_columns = ['code']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        sfcwf30joinm5m4 = SFCWF30JOINM5M4()
        with open('SFCWF30JOINM5M4.csv', 'r') as fd:
            reader = csv.DictReader(fd, dialect=csv.excel_tab)
            old_tuples = [sfcwf30joinm5m4._biz_tuple._make(tuple(row.values())) for row in reader]

        material_cats = fm7_material_cat().load_db_data()
        ret_tuples = []
        existing_no = set()
        for o in old_tuples:
            ret_tuples.append(self._tuple(
                code=o.PRODUCT_NO,
                name=o.PRODUCT_DES,
                cat_pk=None if not material_cats.lookup_key(o.NO_KIND) else material_cats.lookup_key(o.NO_KIND).id,
                model=o.NO_MANU,
                is_enabled=1,
                version=1,
                attr1=float(o.SINGLE_LINE_CIR_STD) if o.SINGLE_LINE_CIR_STD else None,
                is_semiproduct=1 if len(o.PRODUCT_NO)!=16 else 0
                )
            )
            existing_no.add(o.PRODUCT_NO)

        # Add extra tuples from SFCWF30
        sfcwf30 = SFCWF30()
        with open('SFCWF30.csv', 'r') as fd:
            reader = csv.DictReader(fd, dialect=csv.excel_tab)
            sfcwf30_tuples = [sfcwf30._biz_tuple._make(tuple(row.values())) for row in reader]

        for o in filter(lambda m: m.PRODUCT_NO not in existing_no, sfcwf30_tuples):
            ret_tuples.append(self._tuple(
                code=o.PRODUCT_NO,
                name=o.PRODUCT_DES,
                cat_pk=None,
                model=None,
                is_enabled=1,
                version=1,
                attr1=float(o.SINGLE_LINE_CIR_STD) if o.SINGLE_LINE_CIR_STD else None,
                is_semiproduct=1
                )
            )
        return ret_tuples

class fm6_carrier_model(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['code', 'carrier_cat_cd', 'spec', 'carcass_diameter', 'disc_diameter', 'gap_length', 'inside_width', 'material_id', 'material_cd', 'capacity', 'note']
        self._key_columns = ['code']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        old_tuples = PMC180M().load_db_data().data_tuples
        return [ self._tuple(
            o.DRUM_TYPENO, o.DRUM_KIND, o.DRUM_NAME,
            o.CIR_INSIDE, o.CIR_OUTSIDE,
            o.SPACE_WIDTH, o.INNER_WIDTH,
            ['NULL'], o.DRUM_MTRLNO, ['NULL'], '初始建立'
        ) for o in old_tuples]

class fm6_equipment_carrier(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['equipment_pk', 'equipment_cd', 'carrier_model_pk', 'carrier_model_cd', 'check_type', 'note']
        self._key_columns = ['equipment_cd', 'carrier_model_cd']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        carrier_models = fm6_carrier_model().load_db_data()
        equipments = fm6_equipment().load_db_data()
        old_tuples = SFCMF22().load_db_data().data_tuples
        ret_tuples = []
        miss_equipment = set()
        miss_carrier_model = set()
        for o in old_tuples:
            equipment = equipments.lookup_key(o.MACHINE_NO)
            carrier_model = carrier_models.lookup_key(o.AXLE_NO)
            if equipment and carrier_model:
                ret_tuples.append(self._tuple(
                    equipment.id, equipment.code,
                    carrier_model.id, carrier_model.code,
                    2, '初始建立'))
            else:
                if not equipment:
                    miss_equipment.add(o.MACHINE_NO)
                if not carrier_model:
                    miss_carrier_model.add(o.AXLE_NO)

        #if len(miss_equipment):
        #    print('Not found equipments {}'.format(','.join(map(lambda s: "'"+s+"'", list(miss_equipment)))))
        #if len(miss_carrier_model):
        #    print('Not found carrier model {}'.format(','.join(map(lambda s: "'"+s+"'", list(miss_carrier_model)))))

        return ret_tuples

class mwc_copper(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['code', 'factory_cd', 'length_origin', 'weight_origin', 'length', 'weight', 'material_pk', 'material_cd', 'status']
        self._key_columns = ['code']
        self._tuple = namedtuple(self.__class__.__name__ + '_tuple', self._columns)

    @property
    def _biz_columns(self):
        return self._columns
    
    @property
    def _biz_key_columns(self):
        return self._key_columns

    @property
    def _biz_tuple(self):
        return self._tuple

    def _gen_init_tuples(self):
        return [
            self._tuple('180210061', 'SCP1', 11200.00, 5005.00, 11200.00, 5005.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210048', 'SCP1', 11178.00, 4995.00, 11058.00, 4995.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210075', 'SCP1', 11191.00, 5001.00, 11191.00, 5001.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210042', 'SCP1', 11203.00, 5006.00, 11203.00, 5006.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210059', 'SCP1', 11198.00, 5004.00, 11198.00, 5004.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210069', 'SCP1', 11200.00, 5005.00, 11200.00, 5005.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210071', 'SCP1', 11234.00, 5020.00, 11234.00, 5020.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210074', 'SCP1', 11187.00, 4999.00, 11187.00, 4999.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210068', 'SCP1', 11205.00, 5007.00, 11205.00, 5007.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210055', 'SCP1', 11229.00, 5018.00, 11229.00, 5018.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210072', 'SCG1', 11252.00, 5028.00, 11252.00, 5028.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210046', 'SCG1', 11196.00, 5003.00, 11196.00, 5003.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210070', 'SCG1', 11214.00, 5011.00, 11214.00, 5011.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210066', 'SCG1', 11187.00, 4999.00, 11187.00, 4999.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210045', 'SCG1', 11180.00, 4996.00, 11180.00, 4996.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210077', 'SCG1', 11203.00, 5006.00, 10953.00, 5006.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
            self._tuple('180210047', 'SCG1', 11182.00, 4997.00, 11182.00, 4997.00, 'a72380700ad34d2f84949c1fae98142f', '4001800000003', 0),
        ]

def test():
    material = fm7_material().load_db_data().create_data(True)
    material.truncate_db = True
    material.gen_new_sql()

def test1():
    fm6_carrier_model().create_data().gen_new_sql()

def test2():
    fm6_equipment_carrier().create_data().gen_new_sql()

def test3():
    with open('new_machines.txt', 'r') as fd:
        file_cds = fd.read().splitlines()

    db_tuples = fm6_equipment().load_db_data().data_tuples
    db_cds = [t.code for t in db_tuples]

    print(set(file_cds) - set(db_cds))
    print(set(db_cds) - set(file_cds))

def gen_fm6_equipment():
    fm6_equipment().load_db_data().create_data(True).gen_new_sql()

def main():
    if len(sys.argv) < 2:
        test()
    else:
        eval(sys.argv[1])

if __name__ == '__main__':
    sys.exit(main())



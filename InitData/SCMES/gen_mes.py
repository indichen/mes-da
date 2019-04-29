#!/usr/bin/env python3

import sys
import pymssql
from os import getenv
from abc import ABC, abstractmethod
from collections import namedtuple
from uuid import uuid4
from decimal import Decimal

class MESTableGenerator(ABC):

    COLUMNS = ['create_time', 'create_user', 'last_modified', 'last_modify_user', 'ts', 'dr', 'tenant_id', 'id']

    _make_def_data = lambda self, given_id=None: \
        self._def_tuple( \
            ['convert(varchar, getdate(), 121)'], 'admin', \
            ['convert(varchar, getdate(), 121)'], 'admin', \
            ['convert(varchar, getdate(), 121)'], 0, 'tenant', \
            given_id or str(uuid4()).replace('-', '')
        )

    _make_sql_value = staticmethod(lambda x: \
        'null' if x is None else \
        "'{}'".format(x) if isinstance(x, str) else \
        x[0] if isinstance(x, list) else \
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
        self._columns = ['code', 'name', 'spec', 'is_batch_equipment', 'checkin_out_type_cd', 'factory_cd', 'factory_name', 'note']
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
            self._tuple('CS04', '37B銅絞機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS09', '7B銅絞機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TN03', '3#630 PCT拋光機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE01', 'CDCC', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('GR09', '1+8集合機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('A130', 'A-13伸線機', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('WE02', '150押出機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS03', '19B銅絞機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TP02', '中心包帶機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE06', 'RCP', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ZZ50', '電二押出倒軸機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE05', 'HCV90 交連機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WR01', '密捲機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('M850', 'M-85伸線機', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('XE02', 'CCV', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('XE03', 'HCV65 交連機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TN02', '2#630 PCT鍍錫機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TP01', '綜合包帶機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('TN01', '1#630 PCT鍍錫機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS08', '7B-1銅絞機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('CS05', '61B銅絞機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('GR03', '2.8M集合機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WE01', '115押出機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('FS13', 'FS-13伸線機', '', 0, 'S', 'SCP1', '電力一課', ''),
            self._tuple('XE07', 'HCV100 交連機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('GR04', '84B鎧裝機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('WE08', '120押出機', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('DR72', 'C 17-2中伸機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE17', '64#押出機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS20', '9#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('ST02', '電鍍錫機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('DR71', 'C 17-1中伸機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE22', 'G97', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR01', '1.2M', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS25', '12#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS06', '1#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GP01', 'GP01', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS24', '11#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE11', '65#押出機(65φ)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE05', 'G94', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE07', '92#押出機(60+30+NOKIA)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR08', '1+3弓絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS02', '13#吉田束絞機(800Φ)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS11', '5#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE06', '95#押出機(MF90)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE21', 'G96', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE19', '67#押出機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE20', '68#押出機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR05', '915MM', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE18', '66#押出機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('DR02', '8頭伸線機', '', 0, 'S', 'SCG1', '電力二課', ''),
            self._tuple('DR01', '12頭伸線機', '', 0, 'S', 'SCG1', '電力二課', ''),
            self._tuple('WE23', 'G98', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE09', '61#押出機(JR65φ)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GP03', '高速小包機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE16', '90#押出機(G63)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS27', '3#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GP02', 'GP02', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS99', '1250(昇祥束絞機)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('DR73', 'C 17-3中伸機', '', 0, 'M', 'SCG1', '電力二課', ''),    
            self._tuple('BS10', '4#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS21', '8#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS19', '10#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS12', '6#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('GR06', '1.6M', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('BS26', '7#束絞機', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE10', '62#押出機(JR65φ)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE12', '91#押出機(JR90φ)', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('WE15', 'G93', '', 0, 'M', 'SCG1', '電力二課', ''),
            self._tuple('ccd', '測試機台B', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ccd1', '測試機台', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ccd3', '測試機台C', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ccd4', '測試機台1', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ccd5', '測試機台2', '', 0, 'M', 'SCP1', '電力一課', ''),
            self._tuple('ccd6', '測試機台3', '', 0, 'M', 'SCP1', '電力一課', ''),
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
        return [
            self._tuple('matcat1', '物料分類1', ['NULL'], 1, ''),
            self._tuple('matcat1', '物料分類2', ['NULL'], 1, ''),
            self._tuple('matcat1', '物料分類3', ['NULL'], 1, ''),
            self._tuple('matcat1', '物料分類4', ['NULL'], 1, ''),
            self._tuple('matcat1', '物料分類5', ['NULL'], 1, ''),
        ] # TODO: Add init data here

## fm7_物料基本信息 (fm7_material)
class fm7_material(MESTableGenerator):
    def __init__(self):
        super().__init__()
        self._columns = ['code', 'name', 'cat_pk', 'name_en', 'is_enabled', 'version']
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
        return [  ] # TODO: Add init data here


def test():
    fm7_material_cat().create_data().gen_new_sql()

def main():
    if len(sys.argv) < 2:
        test()
    else:
        eval(sys.argv[1])

if __name__ == '__main__':
    sys.exit(main())



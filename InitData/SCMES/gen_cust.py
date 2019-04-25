#!/usr/bin/env python3

import sys
from abc import ABC, abstractmethod
from collections import namedtuple
from uuid import uuid4

class CustTableGenerator(ABC):

    DEF_DB_SCHEMA = 'pap.walsindba'
    DEF_COLUMNS = ['pk_mdm', 'mdm_code', 'mdm_duplicate', 'mdm_seal', 'mdm_version', 'ts', 'dr']

    make_sql_value = lambda x: "'{}'".format(x) if isinstance(x, str) else x[0] if isinstance(x, list) else str(x)

    def __init__(self, cust_table_name=None):
        if not cust_table_name:
            cust_table_name = self.__class__.__name__
        self.table = '{}.{}'.format(CustTableGenerator.DEF_DB_SCHEMA, cust_table_name)
        self.def_tuple = namedtuple('def_tuple', CustTableGenerator.DEF_COLUMNS)
        self._truncate_db = True


    @property
    def truncate_db(self):
        return self._truncate_db
    
    @truncate_db.setter
    def truncate_db(self, value):
        self._truncate_db = False if not value else True

    @abstractmethod
    def get_biz_init_tuples(self):
        pass

    def gen_sql(self):
        biz_init_tuples = self.get_biz_init_tuples()
        assert(isinstance(biz_init_tuples, list))
        assert(len(biz_init_tuples) > 0)
        assert(hasattr(biz_init_tuples[0].__class__, '_fields'))

        biz_tuple = biz_init_tuples[0].__class__
        merged_tuple = namedtuple('merged', biz_tuple._fields + self.def_tuple._fields)

        if self._truncate_db:
            print('truncate table {};'.format(self.table))

        for index, biz in enumerate(biz_init_tuples):
            init_def_tuple = self.def_tuple(str(uuid4()), '{:010d}'.format(index+1), 0, 0, 1, ['convert(varchar, getdate(), 121)'], 0)

            final_tuple = merged_tuple(*(biz + init_def_tuple))
            final_columns = ', '.join(final_tuple._fields)
            final_values = ', '.join([CustTableGenerator.make_sql_value(getattr(final_tuple, f)) for f in final_tuple._fields])
            final_sql = 'insert into {} ({}) values ({});'.format(self.table, final_columns, final_values)
            print(final_sql)

        return 0

## c_載具類型 (c_cust_carrier_cat)
class c_cust_carrier_cat(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('S', 'S周轉軸', ''),
            biz_tuple('F', 'F成品軸', ''),
        ]
        return biz_init_tuples

## c_載具狀態 (c_cust_carrier_status)
class c_cust_carrier_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, 'I空載', ''),
            biz_tuple(20, 'U負載', ''),
            biz_tuple(30, 'A驗收', ''),
            biz_tuple(50, 'R維修', ''),
            biz_tuple(55, 'W待修', ''),
            biz_tuple(80, 'S備品', ''),
            biz_tuple(90, 'C除賬', ''),
        ]
        return biz_init_tuples

## c_生產裝備狀態 (c_cust_equip_status)
class c_cust_equip_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'is_enabled']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('S', 'S待料', 1),
            biz_tuple('D', 'D暫置', 1),
            biz_tuple('P', 'P準備工作', 1),
            biz_tuple('R', 'R生產中', 1),
            biz_tuple('F', 'F故障', 1),
            biz_tuple('A', 'A測試中', 1),
            biz_tuple('M', 'M保養', 1),
            biz_tuple('Q', 'Q不良品處理', 1),
        ]
        return biz_init_tuples

## c_LOT狀態 (c_cust_lot_status)
class c_cust_lot_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(0, '新建', ''),
            biz_tuple(10, '待產', ''),
            biz_tuple(20, '生產中', ''),
            biz_tuple(30, '完成', ''),
            biz_tuple(11, '待驗', ''),
            biz_tuple(12, '檢驗中', ''),
            biz_tuple(40, '報廢/除賬', ''),
            biz_tuple(80, '待重工', ''),
            biz_tuple(90, '暫停', ''),
        ]
        return biz_init_tuples

## c_LOT產生原因 (c_cust_lot_source_code)
class c_cust_lot_source_code(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '產出', ''),
            biz_tuple(20, '載具交換', ''),
            biz_tuple(30, '委外接收', ''),
        ]
        return biz_init_tuples

## c_組織與工廠對照表 (c_cust_org_factory_map)
class c_cust_org_factory_map(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['org_code', 'factory_code', 'org_name', 'factory_name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('WC1900', 'SCP1', '電力製造部', '電力製造一課', '部級資料存取'),
            biz_tuple('WC1900', 'SCG1', '電力製造部', '電力製造二課', '部級資料存取'),
            biz_tuple('WC1910', 'SCP1', '電力製造一課', '電力製造一課', ''),
            biz_tuple('WC1910', 'SCG1', '電力製造一課', '電力製造二課', '跨課資料存取'),
            biz_tuple('WC1911', 'SCP1', '伸線站(P1DR)', '電力製造一課', ''),
            biz_tuple('WC1912', 'SCP1', '銅絞站(P1CS)', '電力製造一課', ''),
            biz_tuple('WC1913', 'SCP1', '熱鍍站(P1TN)', '電力製造一課', ''),
            biz_tuple('WC1914', 'SCP1', '交連站(P1XE)', '電力製造一課', ''),
            biz_tuple('WC1915', 'SCP1', 'RCP站(P1RC)', '電力製造一課', ''),
            biz_tuple('WC1921', 'SCP1', '集合站(P1GR)', '電力製造一課', ''),
            biz_tuple('WC1922', 'SCP1', '押出站(P1WE)', '電力製造一課', ''),
            biz_tuple('WC1923', 'SCP1', '包裝站(P1PK)', '電力製造一課', ''),
            biz_tuple('WC1924', 'SCP1', '噴漆站', '電力製造一課', ''),
            biz_tuple('WC1B10', 'SCP1', '電力製造二課', '電力製造一課', '跨課資料存取'),
            biz_tuple('WC1B10', 'SCG1', '電力製造二課', '電力製造二課', ''),
            biz_tuple('WC1B11', 'SCG1', '伸線站(P2DR)', '電力製造二課', ''),
            biz_tuple('WC1B12', 'SCG1', '銅絞站(P2CS)', '電力製造二課', ''),
            biz_tuple('WC1B13', 'SCG1', '集合站(P2GR)', '電力製造二課', ''),
            biz_tuple('WC1B14', 'SCG1', '押出站(P2WE)', '電力製造二課', ''),
            biz_tuple('WC1B15', 'SCG1', '包裝站(P2PK)', '電力製造二課', ''),
            biz_tuple('WC1B16', 'SCG1', '被覆站(P2WO)', '電力製造二課', ''),
            biz_tuple('WC1B17', 'SCG1', '編織站', '電力製造二課', ''),
        ]
        return biz_init_tuples

## c_製令優先序 (c_cust_mo_priority)
class c_cust_mo_priority(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(90, '緊急', ''),
            biz_tuple(30, '高', ''),
            biz_tuple(20, '中', ''),
            biz_tuple(10, '低', ''),
        ]
        return biz_init_tuples

## c_品質碼 (c_cust_quality_code)
class c_cust_quality_code(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['categories', 'code', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('A嚴重缺失', 'A03', '芯線內有水'),
            biz_tuple('A嚴重缺失', 'A05', '芯線混線'),
            biz_tuple('A嚴重缺失', 'A06', '芯線斷線'),
            biz_tuple('A嚴重缺失', 'A07', '包帶不符'),
            biz_tuple('A嚴重缺失', 'A10', '芯線排列不符'),
            biz_tuple('A嚴重缺失', 'A11', '接地軟銅線錯誤'),
            biz_tuple('A嚴重缺失', 'A12', '絞線不符'),
            biz_tuple('A嚴重缺失', 'A13', '電線結構不符'),
            biz_tuple('B導體類', 'B02', '導體直徑大'),
            biz_tuple('B導體類', 'B03', '導體直徑小'),
            biz_tuple('B導體類', 'B10', '導體壓傷'),
            biz_tuple('B導體類', 'B13', '導體不潔'),
            biz_tuple('B導體類', 'B15', '導體股數不符'),
            biz_tuple('B導體類', 'B20', '導體滲料'),
            biz_tuple('B導體類', 'B22', '導體鍍錫不良'),
            biz_tuple('B導體類', 'B24', '導體變色'),
            biz_tuple('B導體類', 'B25', '鍍錫銅線直徑小'),
            biz_tuple('C絕緣類', 'C07', '絕緣厚度不均'),
            biz_tuple('C絕緣類', 'C08', '絕緣麻點死料'),
            biz_tuple('C絕緣類', 'C11', '絕緣外觀粗糙'),
            biz_tuple('C絕緣類', 'C12', '絕緣外觀刮痕'),
            biz_tuple('C絕緣類', 'C15', '絕緣不潔'),
            biz_tuple('C絕緣類', 'C16', '絕緣外觀凹凸不平'),
            biz_tuple('C絕緣類', 'C18', '絕緣與被覆相粘'),
            biz_tuple('C絕緣類', 'C19', '絕緣與導體鬆動'),
            biz_tuple('D內被類', 'D1', '內被外徑大'),
            biz_tuple('F外被類', 'F04', '外被最小厚度薄'),
            biz_tuple('G外導類', 'G11', '外導外觀擦傷'),
            biz_tuple('G外導類', 'G14', '外導外觀縱狀凸起'),
            biz_tuple('H纏繞類', 'H20', '纏繞銅線直徑小'),
            biz_tuple('H纏繞類', 'H24', '纏繞鍍錫銅線刮傷'),
            biz_tuple('J結構類', 'J15', '集合絞距大'),
            biz_tuple('K外觀類', 'K01', '外觀刮傷'),
            biz_tuple('K外觀類', 'K02', '外觀波紋'),
            biz_tuple('K外觀類', 'K03', '外觀破洞'),
            biz_tuple('K外觀類', 'K05', '外觀凹凸不平'),
            biz_tuple('K外觀類', 'K06', '外觀凹痕'),
            biz_tuple('K外觀類', 'K08', '外觀不潔'),
            biz_tuple('K外觀類', 'K09', '外觀粗糙'),
            biz_tuple('K外觀類', 'K11', '外觀麻點死料'),
            biz_tuple('K外觀類', 'K12', '外觀節狀'),
            biz_tuple('K外觀類', 'K17', '外觀排線不良'),
            biz_tuple('L印字類', 'L01', '印字不良'),
            biz_tuple('L印字類', 'L02', '外觀帶印條'),
            biz_tuple('L印字類', 'L03', '外觀無印字'),
            biz_tuple('L印字類', 'L04', '絕緣帶印條'),
            biz_tuple('正常', '00', '品質正常'),
        ]
        return biz_init_tuples

## c_工單帬組狀態 (c_cust_po_group_status)
class c_cust_po_group_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '新建', ''),
            biz_tuple(15, '處理中', ''),
            biz_tuple(20, '處理成功', ''),
            biz_tuple(30, '處理失敗', ''),
        ]
        return biz_init_tuples

## c_製令狀態 (c_cust_mo_status)
class c_cust_mo_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '新建', ''),
            biz_tuple(20, '待產', ''),
            biz_tuple(30, '生產中', ''),
            biz_tuple(40, '結案', ''),
            biz_tuple(80, '暫停', ''),
            biz_tuple(90, '終止', ''),
        ]
        return biz_init_tuples

## c_製程工單狀態 (c_cust_process_po_status)
class c_cust_process_po_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '新建', ''),
            biz_tuple(11, '待手工開立製令', ''),
            biz_tuple(20, '已開立製令', ''),
            biz_tuple(30, '結案', ''),
        ]
        return biz_init_tuples

## c_製程工單類型 (c_cust_process_po_type)
class c_cust_process_po_type(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '一般', ''),
            biz_tuple(50, '重工', ''),
            biz_tuple(20, '計劃無主', ''),
            biz_tuple(30, '生產無主', ''),
            biz_tuple(40, '計劃餘尺', ''),
        ]
        return biz_init_tuples

## c_SAP工單工廠 (c_cust_sap_po_factory)
class c_cust_sap_po_factory(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('SCP1', '電力製造一課', ''),
            biz_tuple('SCG1', '電力製造二課', ''),
        ]
        return biz_init_tuples

## c_SAP工單下載處理狀態 (c_cust_sappo_proc_status)
class c_cust_sappo_proc_status(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '新建', ''),
            biz_tuple(15, '處理中', ''),
            biz_tuple(20, '完成', ''),
            biz_tuple(30, '失敗', ''),
        ]
        return biz_init_tuples        

## c_製令產生類別 (c_cust_mo_type)
class c_cust_mo_type(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple(10, '系統', ''),
            biz_tuple(20, '手動', ''),
        ]
        return biz_init_tuples        


def main():
    if len(sys.argv) < 2:
        return -1
    return getattr(sys.modules['__main__'], sys.argv[1])().gen_sql()

if __name__ == '__main__':
    sys.exit(main())


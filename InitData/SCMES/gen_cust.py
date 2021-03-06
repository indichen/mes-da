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
            biz_tuple(10, 'I空載', '閒置中'),
            biz_tuple(20, 'U負載', '使用中'),
            biz_tuple(30, 'A驗收', '等待驗收'),
            biz_tuple(50, 'R維修', '維修中'),
            biz_tuple(55, 'W待修', '等待維修'),
            biz_tuple(80, 'S備品', '備用'),
            biz_tuple(90, 'C除賬', '無法使用'),
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

## c_生產裝備投產類型 (c_name)
class c_cust_equip_prod_type(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'name', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('M', 'M手動', '手動機台'),
            biz_tuple('S', 'S半自動', '半自動機台'),
            biz_tuple('A', 'A自動', '全自動機台'),
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
            biz_tuple(40, '例外處理', ''),
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
            biz_tuple(30, '待產', ''),
            biz_tuple(40, '生產中', ''),
            biz_tuple(50, '結案', ''),
            biz_tuple(80, '暫停', ''),
            biz_tuple(90, '中止', ''),
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

## c_參數配置 (c_cust_config)
class c_cust_config(CustTableGenerator):
    def get_biz_init_tuples(self):
        biz_columns = ['code', 'value_int', 'value_str', 'note']
        biz_tuple = namedtuple(self.__class__.__name__ + '_tuple', biz_columns)
        biz_init_tuples = [
            biz_tuple('WG_checkin_check_level', 1, ['null'], '第二雲母 刷投入檢核開關'),
            biz_tuple('WG_checkout_check_level', 1, ['null'], '第二雲母 刷產出檢核開關'),
            biz_tuple('WG_production_check_level', 1, ['null'], '第二雲母 開始生產檢核開關'),

            biz_tuple('DR_checkin_check_level', 1, ['null'], '伸線 刷投入檢核開關'),
            biz_tuple('DR_checkout_check_level', 1, ['null'], '伸線 刷產出檢核開關'),
            biz_tuple('DR_production_check_level', 1, ['null'], '伸線 開始生產檢核開關'),

            biz_tuple('L2_checkin_check_level', 1, ['null'], '第二束管 刷投入檢核開關'),
            biz_tuple('L2_checkout_check_level', 1, ['null'], '第二束管 刷產出檢核開關'),
            biz_tuple('L2_production_check_level', 1, ['null'], '第二束管 開始生產檢核開關'),

            biz_tuple('TS_checkin_check_level', 1, ['null'], '束管集合 刷投入檢核開關'),
            biz_tuple('TS_checkout_check_level', 1, ['null'], '束管集合 刷產出檢核開關'),
            biz_tuple('TS_production_check_level', 1, ['null'], '束管集合 開始生產檢核開關'),

            biz_tuple('CG_checkin_check_level', 1, ['null'], '波管成型 刷投入檢核開關'),
            biz_tuple('CG_checkout_check_level', 1, ['null'], '波管成型 刷產出檢核開關'),
            biz_tuple('CG_production_check_level', 1, ['null'], '波管成型 開始生產檢核開關'),

            biz_tuple('WR_checkin_check_level', 1, ['null'], '包帶 刷投入檢核開關'),
            biz_tuple('WR_checkout_check_level', 1, ['null'], '包帶 刷產出檢核開關'),
            biz_tuple('WR_production_check_level', 1, ['null'], '包帶 開始生產檢核開關'),

            biz_tuple('GX_checkin_check_level', 1, ['null'], '第二絞合 刷投入檢核開關'),
            biz_tuple('GX_checkout_check_level', 1, ['null'], '第二絞合 刷產出檢核開關'),
            biz_tuple('GX_production_check_level', 1, ['null'], '第二絞合 開始生產檢核開關'),

            biz_tuple('RN_checkin_check_level', 1, ['null'], '印字 刷投入檢核開關'),
            biz_tuple('RN_checkout_check_level', 1, ['null'], '印字 刷產出檢核開關'),
            biz_tuple('RN_production_check_level', 1, ['null'], '印字 開始生產檢核開關'),

            biz_tuple('WI_checkin_check_level', 1, ['null'], '內被 刷投入檢核開關'),
            biz_tuple('WI_checkout_check_level', 1, ['null'], '內被 刷產出檢核開關'),
            biz_tuple('WI_production_check_level', 1, ['null'], '內被 開始生產檢核開關'),

            biz_tuple('E1_checkin_check_level', 1, ['null'], '第一絕緣 刷投入檢核開關'),
            biz_tuple('E1_checkout_check_level', 1, ['null'], '第一絕緣 刷產出檢核開關'),
            biz_tuple('E1_production_check_level', 1, ['null'], '第一絕緣 開始生產檢核開關'),

            biz_tuple('RW_checkin_check_level', 1, ['null'], '倒軸 刷投入檢核開關'),
            biz_tuple('RW_checkout_check_level', 1, ['null'], '倒軸 刷產出檢核開關'),
            biz_tuple('RW_production_check_level', 1, ['null'], '倒軸 開始生產檢核開關'),

            biz_tuple('B3_checkin_check_level', 1, ['null'], '第三編織(委外) 刷投入檢核開關'),
            biz_tuple('B3_checkout_check_level', 1, ['null'], '第三編織(委外) 刷產出檢核開關'),
            biz_tuple('B3_production_check_level', 1, ['null'], '第三編織(委外) 開始生產檢核開關'),

            biz_tuple('W2_checkin_check_level', 1, ['null'], '第二外被 刷投入檢核開關'),
            biz_tuple('W2_checkout_check_level', 1, ['null'], '第二外被 刷產出檢核開關'),
            biz_tuple('W2_production_check_level', 1, ['null'], '第二外被 開始生產檢核開關'),

            biz_tuple('W4_checkin_check_level', 1, ['null'], '第四帶類 刷投入檢核開關'),
            biz_tuple('W4_checkout_check_level', 1, ['null'], '第四帶類 刷產出檢核開關'),
            biz_tuple('W4_production_check_level', 1, ['null'], '第四帶類 開始生產檢核開關'),

            biz_tuple('G3_checkin_check_level', 1, ['null'], '第三絞合 刷投入檢核開關'),
            biz_tuple('G3_checkout_check_level', 1, ['null'], '第三絞合 刷產出檢核開關'),
            biz_tuple('G3_production_check_level', 1, ['null'], '第三絞合 開始生產檢核開關'),

            biz_tuple('CS_checkin_check_level', 1, ['null'], '銅絞 刷投入檢核開關'),
            biz_tuple('CS_checkout_check_level', 1, ['null'], '銅絞 刷產出檢核開關'),
            biz_tuple('CS_production_check_level', 1, ['null'], '銅絞 開始生產檢核開關'),

            biz_tuple('PT_checkin_check_level', 1, ['null'], '塗油漆 刷投入檢核開關'),
            biz_tuple('PT_checkout_check_level', 1, ['null'], '塗油漆 刷產出檢核開關'),
            biz_tuple('PT_production_check_level', 1, ['null'], '塗油漆 開始生產檢核開關'),

            biz_tuple('X2_checkin_check_level', 1, ['null'], '交連第二絕緣 刷投入檢核開關'),
            biz_tuple('X2_checkout_check_level', 1, ['null'], '交連第二絕緣 刷產出檢核開關'),
            biz_tuple('X2_production_check_level', 1, ['null'], '交連第二絕緣 開始生產檢核開關'),

            biz_tuple('PK_checkin_check_level', 1, ['null'], '包裝 刷投入檢核開關'),
            biz_tuple('PK_checkout_check_level', 1, ['null'], '包裝 刷產出檢核開關'),
            biz_tuple('PK_production_check_level', 1, ['null'], '包裝 開始生產檢核開關'),

            biz_tuple('XX_checkin_check_level', 1, ['null'], '交連複合絕緣 刷投入檢核開關'),
            biz_tuple('XX_checkout_check_level', 1, ['null'], '交連複合絕緣 刷產出檢核開關'),
            biz_tuple('XX_production_check_level', 1, ['null'], '交連複合絕緣 開始生產檢核開關'),

            biz_tuple('P2_checkin_check_level', 1, ['null'], '第二對絞 刷投入檢核開關'),
            biz_tuple('P2_checkout_check_level', 1, ['null'], '第二對絞 刷產出檢核開關'),
            biz_tuple('P2_production_check_level', 1, ['null'], '第二對絞 開始生產檢核開關'),

            biz_tuple('IR_checkin_check_level', 1, ['null'], '照射(委外) 刷投入檢核開關'),
            biz_tuple('IR_checkout_check_level', 1, ['null'], '照射(委外) 刷產出檢核開關'),
            biz_tuple('IR_production_check_level', 1, ['null'], '照射(委外) 開始生產檢核開關'),

            biz_tuple('WS_checkin_check_level', 1, ['null'], '第二帶類 刷投入檢核開關'),
            biz_tuple('WS_checkout_check_level', 1, ['null'], '第二帶類 刷產出檢核開關'),
            biz_tuple('WS_production_check_level', 1, ['null'], '第二帶類 開始生產檢核開關'),

            biz_tuple('I2_checkin_check_level', 1, ['null'], '第二照射 刷投入檢核開關'),
            biz_tuple('I2_checkout_check_level', 1, ['null'], '第二照射 刷產出檢核開關'),
            biz_tuple('I2_production_check_level', 1, ['null'], '第二照射 開始生產檢核開關'),

            biz_tuple('X4_checkin_check_level', 1, ['null'], '交連第四絕緣 刷投入檢核開關'),
            biz_tuple('X4_checkout_check_level', 1, ['null'], '交連第四絕緣 刷產出檢核開關'),
            biz_tuple('X4_production_check_level', 1, ['null'], '交連第四絕緣 開始生產檢核開關'),

            biz_tuple('WU_checkin_check_level', 1, ['null'], '波紋銅被 刷投入檢核開關'),
            biz_tuple('WU_checkout_check_level', 1, ['null'], '波紋銅被 刷產出檢核開關'),
            biz_tuple('WU_production_check_level', 1, ['null'], '波紋銅被 開始生產檢核開關'),

            biz_tuple('B2_checkin_check_level', 1, ['null'], '第二編織(委外) 刷投入檢核開關'),
            biz_tuple('B2_checkout_check_level', 1, ['null'], '第二編織(委外) 刷產出檢核開關'),
            biz_tuple('B2_production_check_level', 1, ['null'], '第二編織(委外) 開始生產檢核開關'),

            biz_tuple('E2_checkin_check_level', 1, ['null'], '第二絕緣 刷投入檢核開關'),
            biz_tuple('E2_checkout_check_level', 1, ['null'], '第二絕緣 刷產出檢核開關'),
            biz_tuple('E2_production_check_level', 1, ['null'], '第二絕緣 開始生產檢核開關'),

            biz_tuple('GB_checkin_check_level', 1, ['null'], '鐵線編織 刷投入檢核開關'),
            biz_tuple('GB_checkout_check_level', 1, ['null'], '鐵線編織 刷產出檢核開關'),
            biz_tuple('GB_production_check_level', 1, ['null'], '鐵線編織 開始生產檢核開關'),

            biz_tuple('GR_checkin_check_level', 1, ['null'], '絞合 刷投入檢核開關'),
            biz_tuple('GR_checkout_check_level', 1, ['null'], '絞合 刷產出檢核開關'),
            biz_tuple('GR_production_check_level', 1, ['null'], '絞合 開始生產檢核開關'),

            biz_tuple('X3_checkin_check_level', 1, ['null'], '交連第三絕緣 刷投入檢核開關'),
            biz_tuple('X3_checkout_check_level', 1, ['null'], '交連第三絕緣 刷產出檢核開關'),
            biz_tuple('X3_production_check_level', 1, ['null'], '交連第三絕緣 開始生產檢核開關'),

            biz_tuple('WP_checkin_check_level', 1, ['null'], '銅線纏繞 刷投入檢核開關'),
            biz_tuple('WP_checkout_check_level', 1, ['null'], '銅線纏繞 刷產出檢核開關'),
            biz_tuple('WP_production_check_level', 1, ['null'], '銅線纏繞 開始生產檢核開關'),

            biz_tuple('WM_checkin_check_level', 1, ['null'], '包雲母帶 刷投入檢核開關'),
            biz_tuple('WM_checkout_check_level', 1, ['null'], '包雲母帶 刷產出檢核開關'),
            biz_tuple('WM_production_check_level', 1, ['null'], '包雲母帶 開始生產檢核開關'),

            biz_tuple('LP_checkin_check_level', 1, ['null'], '積層被覆 刷投入檢核開關'),
            biz_tuple('LP_checkout_check_level', 1, ['null'], '積層被覆 刷產出檢核開關'),
            biz_tuple('LP_production_check_level', 1, ['null'], '積層被覆 開始生產檢核開關'),

            biz_tuple('G4_checkin_check_level', 1, ['null'], '第四絞合 刷投入檢核開關'),
            biz_tuple('G4_checkout_check_level', 1, ['null'], '第四絞合 刷產出檢核開關'),
            biz_tuple('G4_production_check_level', 1, ['null'], '第四絞合 開始生產檢核開關'),

            biz_tuple('XE_checkin_check_level', 1, ['null'], '交連押出 刷投入檢核開關'),
            biz_tuple('XE_checkout_check_level', 1, ['null'], '交連押出 刷產出檢核開關'),
            biz_tuple('XE_production_check_level', 1, ['null'], '交連押出 開始生產檢核開關'),

            biz_tuple('WN_checkin_check_level', 1, ['null'], '包數字帶 刷投入檢核開關'),
            biz_tuple('WN_checkout_check_level', 1, ['null'], '包數字帶 刷產出檢核開關'),
            biz_tuple('WN_production_check_level', 1, ['null'], '包數字帶 開始生產檢核開關'),

            biz_tuple('SE_checkin_check_level', 1, ['null'], '溝槽押出 刷投入檢核開關'),
            biz_tuple('SE_checkout_check_level', 1, ['null'], '溝槽押出 刷產出檢核開關'),
            biz_tuple('SE_production_check_level', 1, ['null'], '溝槽押出 開始生產檢核開關'),

            biz_tuple('GA_checkin_check_level', 1, ['null'], '鎧裝 刷投入檢核開關'),
            biz_tuple('GA_checkout_check_level', 1, ['null'], '鎧裝 刷產出檢核開關'),
            biz_tuple('GA_production_check_level', 1, ['null'], '鎧裝 開始生產檢核開關'),

            biz_tuple('E3_checkin_check_level', 1, ['null'], '第三絕緣 刷投入檢核開關'),
            biz_tuple('E3_checkout_check_level', 1, ['null'], '第三絕緣 刷產出檢核開關'),
            biz_tuple('E3_production_check_level', 1, ['null'], '第三絕緣 開始生產檢核開關'),

            biz_tuple('TN_checkin_check_level', 1, ['null'], '熱鍍 刷投入檢核開關'),
            biz_tuple('TN_checkout_check_level', 1, ['null'], '熱鍍 刷產出檢核開關'),
            biz_tuple('TN_production_check_level', 1, ['null'], '熱鍍 開始生產檢核開關'),

            biz_tuple('W3_checkin_check_level', 1, ['null'], '第三帶類 刷投入檢核開關'),
            biz_tuple('W3_checkout_check_level', 1, ['null'], '第三帶類 刷產出檢核開關'),
            biz_tuple('W3_production_check_level', 1, ['null'], '第三帶類 開始生產檢核開關'),

            biz_tuple('GP_checkin_check_level', 1, ['null'], '對絞 刷投入檢核開關'),
            biz_tuple('GP_checkout_check_level', 1, ['null'], '對絞 刷產出檢核開關'),
            biz_tuple('GP_production_check_level', 1, ['null'], '對絞 開始生產檢核開關'),

            biz_tuple('CL_checkin_check_level', 1, ['null'], '著色 刷投入檢核開關'),
            biz_tuple('CL_checkout_check_level', 1, ['null'], '著色 刷產出檢核開關'),
            biz_tuple('CL_production_check_level', 1, ['null'], '著色 開始生產檢核開關'),

            biz_tuple('XF_checkin_check_level', 1, ['null'], '橡膠充實押出 刷投入檢核開關'),
            biz_tuple('XF_checkout_check_level', 1, ['null'], '橡膠充實押出 刷產出檢核開關'),
            biz_tuple('XF_production_check_level', 1, ['null'], '橡膠充實押出 開始生產檢核開關'),

            biz_tuple('TE_checkin_check_level', 1, ['null'], '電鍍 刷投入檢核開關'),
            biz_tuple('TE_checkout_check_level', 1, ['null'], '電鍍 刷產出檢核開關'),
            biz_tuple('TE_production_check_level', 1, ['null'], '電鍍 開始生產檢核開關'),

            biz_tuple('XT_checkin_check_level', 1, ['null'], '橡膠複合內被 刷投入檢核開關'),
            biz_tuple('XT_checkout_check_level', 1, ['null'], '橡膠複合內被 刷產出檢核開關'),
            biz_tuple('XT_production_check_level', 1, ['null'], '橡膠複合內被 開始生產檢核開關'),

            biz_tuple('GT_checkin_check_level', 1, ['null'], '三芯絞 刷投入檢核開關'),
            biz_tuple('GT_checkout_check_level', 1, ['null'], '三芯絞 刷產出檢核開關'),
            biz_tuple('GT_production_check_level', 1, ['null'], '三芯絞 開始生產檢核開關'),

            biz_tuple('IN_checkin_check_level', 1, ['null'], '檢驗 刷投入檢核開關'),
            biz_tuple('IN_checkout_check_level', 1, ['null'], '檢驗 刷產出檢核開關'),
            biz_tuple('IN_production_check_level', 1, ['null'], '檢驗 開始生產檢核開關'),

            biz_tuple('WT_checkin_check_level', 1, ['null'], '包銅帶 刷投入檢核開關'),
            biz_tuple('WT_checkout_check_level', 1, ['null'], '包銅帶 刷產出檢核開關'),
            biz_tuple('WT_production_check_level', 1, ['null'], '包銅帶 開始生產檢核開關'),

            biz_tuple('XO_checkin_check_level', 1, ['null'], '橡膠外被 刷投入檢核開關'),
            biz_tuple('XO_checkout_check_level', 1, ['null'], '橡膠外被 刷產出檢核開關'),
            biz_tuple('XO_production_check_level', 1, ['null'], '橡膠外被 開始生產檢核開關'),

            biz_tuple('RX_checkin_check_level', 1, ['null'], '第二倒軸 刷投入檢核開關'),
            biz_tuple('RX_checkout_check_level', 1, ['null'], '第二倒軸 刷產出檢核開關'),
            biz_tuple('RX_production_check_level', 1, ['null'], '第二倒軸 開始生產檢核開關'),

            biz_tuple('WL_checkin_check_level', 1, ['null'], '波紋鋁被 刷投入檢核開關'),
            biz_tuple('WL_checkout_check_level', 1, ['null'], '波紋鋁被 刷產出檢核開關'),
            biz_tuple('WL_production_check_level', 1, ['null'], '波紋鋁被 開始生產檢核開關'),

            biz_tuple('BR_checkin_check_level', 1, ['null'], '編織(委外) 刷投入檢核開關'),
            biz_tuple('BR_checkout_check_level', 1, ['null'], '編織(委外) 刷產出檢核開關'),
            biz_tuple('BR_production_check_level', 1, ['null'], '編織(委外) 開始生產檢核開關'),

            biz_tuple('XI_checkin_check_level', 1, ['null'], '橡膠內被 刷投入檢核開關'),
            biz_tuple('XI_checkout_check_level', 1, ['null'], '橡膠內被 刷產出檢核開關'),
            biz_tuple('XI_production_check_level', 1, ['null'], '橡膠內被 開始生產檢核開關'),

            biz_tuple('LE_checkin_check_level', 1, ['null'], '束管押出 刷投入檢核開關'),
            biz_tuple('LE_checkout_check_level', 1, ['null'], '束管押出 刷產出檢核開關'),
            biz_tuple('LE_production_check_level', 1, ['null'], '束管押出 開始生產檢核開關'),

            biz_tuple('CA_checkin_check_level', 1, ['null'], '組裝(委外) 刷投入檢核開關'),
            biz_tuple('CA_checkout_check_level', 1, ['null'], '組裝(委外) 刷產出檢核開關'),
            biz_tuple('CA_production_check_level', 1, ['null'], '組裝(委外) 開始生產檢核開關'),

            biz_tuple('WO_checkin_check_level', 1, ['null'], '外被 刷投入檢核開關'),
            biz_tuple('WO_checkout_check_level', 1, ['null'], '外被 刷產出檢核開關'),
            biz_tuple('WO_production_check_level', 1, ['null'], '外被 開始生產檢核開關'),

            biz_tuple('WX_checkin_check_level', 1, ['null'], '塑膠複合絕緣 刷投入檢核開關'),
            biz_tuple('WX_checkout_check_level', 1, ['null'], '塑膠複合絕緣 刷產出檢核開關'),
            biz_tuple('WX_production_check_level', 1, ['null'], '塑膠複合絕緣 開始生產檢核開關'),

            biz_tuple('XC_checkin_check_level', 1, ['null'], '異形押出 刷投入檢核開關'),
            biz_tuple('XC_checkout_check_level', 1, ['null'], '異形押出 刷產出檢核開關'),
            biz_tuple('XC_production_check_level', 1, ['null'], '異形押出 開始生產檢核開關'),

            biz_tuple('WE_checkin_check_level', 1, ['null'], '絕緣 刷投入檢核開關'),
            biz_tuple('WE_checkout_check_level', 1, ['null'], '絕緣 刷產出檢核開關'),
            biz_tuple('WE_production_check_level', 1, ['null'], '絕緣 開始生產檢核開關'),
        ]
        return biz_init_tuples        

def main():
    if len(sys.argv) < 2:
        return -1
    return getattr(sys.modules['__main__'], sys.argv[1])().gen_sql()

if __name__ == '__main__':
    sys.exit(main())


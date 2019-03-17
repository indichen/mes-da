/*==============================================================*/
/* Database name:  SCMES                                        */
/* DBMS name:      Microsoft SQL Server 2017 (iuap)             */
/* Created on:     2019/3/17 下午 09:11:08                        */
/*==============================================================*/


use SCMES
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_copper_size')
            and   type = 'U')
   drop table mlo_copper_size
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_mo')
            and   type = 'U')
   drop table mlo_mo
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_po_group')
            and   type = 'U')
   drop table mlo_po_group
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_po_group_map')
            and   type = 'U')
   drop table mlo_po_group_map
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_process_po')
            and   type = 'U')
   drop table mlo_process_po
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_sap_po')
            and   type = 'U')
   drop table mlo_sap_po
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_sap_po_process')
            and   type = 'U')
   drop table mlo_sap_po_process
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mlo_sap_po_process_batch')
            and   type = 'U')
   drop table mlo_sap_po_process_batch
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mw_common_checkin')
            and   type = 'U')
   drop table mw_common_checkin
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mw_common_checkout')
            and   type = 'U')
   drop table mw_common_checkout
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mw_common_checkout_quality')
            and   type = 'U')
   drop table mw_common_checkout_quality
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mw_common_history')
            and   type = 'U')
   drop table mw_common_history
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mw_common_lot')
            and   type = 'U')
   drop table mw_common_lot
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mw_common_lot_piece')
            and   type = 'U')
   drop table mw_common_lot_piece
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_checkin_copper')
            and   type = 'U')
   drop table mwc_checkin_copper
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_checkin_lot')
            and   type = 'U')
   drop table mwc_checkin_lot
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_checkin_queue')
            and   type = 'U')
   drop table mwc_checkin_queue
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_checkout')
            and   type = 'U')
   drop table mwc_checkout
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_checkout_operator')
            and   type = 'U')
   drop table mwc_checkout_operator
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_copper')
            and   type = 'U')
   drop table mwc_copper
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mwc_lot_po_map')
            and   type = 'U')
   drop table mwc_lot_po_map
go

if exists (select 1
            from  sysobjects
           where  id = object_id('wm_common_source_lot')
            and   type = 'U')
   drop table wm_common_source_lot
go

if exists (select 1
            from  sysobjects
           where  id = object_id('wmc_checkout_queue')
            and   type = 'U')
   drop table wmc_checkout_queue
go

if exists (select 1
            from  sysobjects
           where  id = object_id('wmc_copper_history')
            and   type = 'U')
   drop table wmc_copper_history
go

if exists (select 1
            from  sysobjects
           where  id = object_id('wmc_lot_detail')
            and   type = 'U')
   drop table wmc_lot_detail
go

if exists (select 1
            from  sysobjects
           where  id = object_id('wmc_lot_history')
            and   type = 'U')
   drop table wmc_lot_history
go

if exists(select 1 from systypes where name='type_boolean')
   drop type type_boolean
go

if exists(select 1 from systypes where name='type_date')
   drop type type_date
go

if exists(select 1 from systypes where name='type_datetime')
   drop type type_datetime
go

if exists(select 1 from systypes where name='type_decimal')
   drop type type_decimal
go

if exists(select 1 from systypes where name='type_diameter')
   drop type type_diameter
go

if exists(select 1 from systypes where name='type_enum_val')
   drop type type_enum_val
go

if exists(select 1 from systypes where name='type_hours')
   drop type type_hours
go

if exists(select 1 from systypes where name='type_id')
   drop type type_id
go

if exists(select 1 from systypes where name='type_length')
   drop type type_length
go

if exists(select 1 from systypes where name='type_memo')
   drop type type_memo
go

if exists(select 1 from systypes where name='type_name')
   drop type type_name
go

if exists(select 1 from systypes where name='type_number')
   drop type type_number
go

if exists(select 1 from systypes where name='type_pk')
   drop type type_pk
go

if exists(select 1 from systypes where name='type_sn')
   drop type type_sn
go

if exists(select 1 from systypes where name='type_weight')
   drop type type_weight
go

/*==============================================================*/
/* Domain: type_boolean                                         */
/*==============================================================*/
create type type_boolean
   from bit
go

/*==============================================================*/
/* Domain: type_date                                            */
/*==============================================================*/
create type type_date
   from char(10)
go

/*==============================================================*/
/* Domain: type_datetime                                        */
/*==============================================================*/
create type type_datetime
   from datetime
go

/*==============================================================*/
/* Domain: type_decimal                                         */
/*==============================================================*/
create type type_decimal
   from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_diameter                                        */
/*==============================================================*/
create type type_diameter
   from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_enum_val                                        */
/*==============================================================*/
create type type_enum_val
   from int
go

/*==============================================================*/
/* Domain: type_hours                                           */
/*==============================================================*/
create type type_hours
   from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_id                                              */
/*==============================================================*/
create type type_id
   from varchar(40)
go

/*==============================================================*/
/* Domain: type_length                                          */
/*==============================================================*/
create type type_length
   from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_memo                                            */
/*==============================================================*/
create type type_memo
   from national char varying(Max)
go

/*==============================================================*/
/* Domain: type_name                                            */
/*==============================================================*/
create type type_name
   from national char varying(20)
go

/*==============================================================*/
/* Domain: type_number                                          */
/*==============================================================*/
create type type_number
   from int
go

/*==============================================================*/
/* Domain: type_pk                                              */
/*==============================================================*/
create type type_pk
   from char(32)
go

/*==============================================================*/
/* Domain: type_sn                                              */
/*==============================================================*/
create type type_sn
   from int
go

/*==============================================================*/
/* Domain: type_weight                                          */
/*==============================================================*/
create type type_weight
   from decimal(10,3)
go

/*==============================================================*/
/* Table: mlo_copper_size                                       */
/*==============================================================*/
create table mlo_copper_size (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   "id (導體尺寸索引檔PK)"     type_pk              not null,
   copper_size_cd       type_id              not null,
   constraint PK_MLO_COPPER_SIZE primary key ("id (導體尺寸索引檔PK)")
)
go

/*==============================================================*/
/* Table: mlo_mo                                                */
/*==============================================================*/
create table mlo_mo (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   mo_id                type_id              not null,
   mo_type              type_enum_val        null,
   priority             type_enum_val        null,
   factory_id           type_id              null,
   workshop             type_name            null,
   machine_pk           type_pk              null,
   recipe_pk            type_pk              null,
   process_code         type_id              null,
   process_name         type_name            null,
   next_process         type_id              null,
   next_process_name    type_name            null,
   copper_size          type_id              null,
   total_qty            type_decimal         null,
   total_qty_unit       type_name            null,
   total_copper_weight  type_weight          null,
   production_qty       type_decimal         null,
   semi_product_spec    type_memo            null,
   semi_product_part_no type_id              null,
   carrier_type         type_id              null,
   outer_diameter       type_length          null,
   carrier_qty          type_number          null,
   operator_qty         type_number          null,
   production_date_est  type_date            null,
   working_hour_est     type_hours           null,
   group_qty            type_number          null,
   group_count          type_number          null,
   note                 type_memo            null,
   start_ts             type_datetime        null,
   end_ts               type_datetime        null,
   working_hour         type_hours           null,
   status               type_enum_val        null,
   constraint PK_MLO_MO primary key nonclustered (id)
)
go

/*==============================================================*/
/* Table: mlo_po_group                                          */
/*==============================================================*/
create table mlo_po_group (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   "id (工單群組PK)"        type_pk              not null,
   po_group_cd          type_id              not null,
   status               type_enum_val        null,
   note                 type_memo            null,
   constraint PK_MLO_PO_GROUP primary key ("id (工單群組PK)")
)
go

/*==============================================================*/
/* Table: mlo_po_group_map                                      */
/*==============================================================*/
create table mlo_po_group_map (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   po_group_pk          type_pk              not null,
   po_pk                type_pk              not null,
   constraint PK_MLO_PO_GROUP_MAP primary key (id)
)
go

/*==============================================================*/
/* Table: mlo_process_po                                        */
/*==============================================================*/
create table mlo_process_po (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   process_po           type_id              null,
   process_po_type      type_enum_val        null,
   part_no              type_id              null,
   sap_po_pk            type_pk              not null,
   next_process_code    type_id              null,
   next_process_name    type_name            null,
   seq_route            type_sn              null,
   process_code         type_id              null,
   process_name         type_name            null,
   semi_product_spec    type_memo            null,
   semi_product_part_no type_id              null,
   def_macheine_pk      type_pk              null,
   qty                  type_number          null,
   unit                 type_name            null,
   qty_planned          type_number          null,
   copper_weight_planned type_weight          null,
   semi_product_weight  type_weight          null,
   production_qty       type_decimal         null,
   po_qty               type_number          null,
   outer_diameter       type_diameter        null,
   mo_pk                type_pk              null,
   status               type_enum_val        null,
   constraint PK_MLO_PROCESS_PO primary key (id)
)
go

/*==============================================================*/
/* Table: mlo_sap_po                                            */
/*==============================================================*/
create table mlo_sap_po (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   po_id                type_id              not null,
   so_id                type_id              not null,
   customer_id          type_id              null,
   customer_name        type_name            null,
   product_partno       type_id              null,
   product_spec         type_memo            null,
   route_id             type_id              null,
   so_qty               type_decimal         null,
   unit_length          type_length          null,
   so_unit              type_name            null,
   shipment_date        type_date            null,
   sales_name           type_name            null,
   production_date_est  type_date            null,
   start_date_est       type_date            null,
   end_date_est         type_date            null,
   is_closed            type_boolean         null,
   batch_no             type_id              null,
   conti_symbol         type_name            null,
   production_date      type_date            null,
   unit_weight          type_weight          null,
   unit_weight_unit     type_name            null,
   storage_qty          type_decimal         null,
   not_storage_qty      type_decimal         null,
   last_storage_qty     type_decimal         null,
   lead_time            type_number          null,
   factory_id           type_id              null,
   department           type_name            null,
   pmc_production_code  type_id              null,
   pmc_production_name  type_name            null,
   po_create_date       type_date            null,
   po_update_date       type_date            null,
   core_wire_color      type_memo            null,
   last_process_code    type_id              null,
   last_process_name    type_name            null,
   carrier_type         type_id              null,
   commit_qty           type_decimal         null,
   copper_size_cd       type_id              null,
   constraint PK_MLO_SAP_PO primary key (id)
)
go

/*==============================================================*/
/* Table: mlo_sap_po_process                                    */
/*==============================================================*/
create table mlo_sap_po_process (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   cd                   type_pk              null,
   po_id                type_id              not null,
   so_id                type_id              not null,
   customer_id          type_id              null,
   customer_name        type_name            null,
   product_partno       type_id              null,
   so_qty               type_decimal         null,
   shipment_date        type_date            null,
   sales_name           type_name            null,
   start_date_est       type_date            null,
   end_date_est         type_date            null,
   is_closed            type_boolean         null,
   batch_no             type_id              null,
   conti_symbol         type_name            null,
   production_date      type_date            null,
   storage_qty          type_decimal         null,
   not_storage_qty      type_decimal         null,
   factory_id           type_id              null,
   po_create_date       type_date            null,
   po_update_date       type_date            null,
   commit_qty           type_decimal         null,
   status               type_enum_val        null,
   note                 type_memo            null,
   constraint PK_MLO_SAP_PO_PROCESS primary key (id)
)
go

/*==============================================================*/
/* Table: mlo_sap_po_process_batch                              */
/*==============================================================*/
create table mlo_sap_po_process_batch (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   cd                   type_id              null,
   constraint PK_MLO_SAP_PO_PROCESS_BATCH primary key (id)
)
go

/*==============================================================*/
/* Table: mw_common_checkin                                     */
/*==============================================================*/
create table mw_common_checkin (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   checkout_pk          type_pk              null,
   machine_pk           type_pk              null,
   process_code         type_id              null,
   process_name         type_name            null,
   checkin_ts           type_datetime        null,
   checkin_type         type_enum_val        null,
   constraint PK_MW_COMMON_CHECKIN primary key (id)
)
go

/*==============================================================*/
/* Table: mw_common_checkout                                    */
/*==============================================================*/
create table mw_common_checkout (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   mo_id                type_id              null,
   machine_pk           type_pk              null,
   process_code         type_id              null,
   process_name         type_name            null,
   check_ts             type_datetime        null,
   production_ts        type_datetime        null,
   checkout_ts          type_datetime        null,
   batch_id             type_id              null,
   is_batch             type_boolean         null,
   working_hour_real    type_hours           null,
   working_hour_calc    type_hours           null,
   lot_pk               type_pk              null,
   lot_id               type_id              null,
   carrier_id           type_id              null,
   weight               type_weight          null,
   quality              type_boolean         null,
   production_date      type_date            null,
   constraint PK_MW_COMMON_CHECKOUT primary key (id)
)
go

/*==============================================================*/
/* Table: mw_common_checkout_quality                            */
/*==============================================================*/
create table mw_common_checkout_quality (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   checkout_pk          type_pk              null,
   lot_id               type_id              null,
   quality_code         type_id              null,
   constraint PK_MW_COMMON_CHECKOUT_QUALITY primary key (id)
)
go

/*==============================================================*/
/* Table: mw_common_history                                     */
/*==============================================================*/
create table mw_common_history (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_pk               type_pk              not null,
   lot_id               type_id              not null,
   event_ts             type_datetime        null,
   type                 type_pk              null,
   action               type_enum_val        null,
   field                type_name            null,
   value_old            type_memo            null,
   value_new            type_memo            null,
   constraint PK_MW_COMMON_HISTORY primary key (id)
)
go

/*==============================================================*/
/* Table: mw_common_lot                                         */
/*==============================================================*/
create table mw_common_lot (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_id               type_id              null,
   vehicle_id           type_id              not null,
   factory_id           type_id              null,
   workshop             type_name            null,
   partno               type_id              null,
   status               type_enum_val        null,
   production_date      type_date            null,
   constraint PK_MW_COMMON_LOT primary key (id)
)
go

/*==============================================================*/
/* Table: mw_common_lot_piece                                   */
/*==============================================================*/
create table mw_common_lot_piece (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_id               type_id              null,
   carrier_pos_id       type_id              null,
   status               type_enum_val        null,
   production_date      type_date            null,
   constraint PK_MW_COMMON_LOT_PIECE primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_checkin_copper                                    */
/*==============================================================*/
create table mwc_checkin_copper (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   checkin_pk           type_pk              not null,
   copper_id            type_id              null,
   feeding_point_id     type_id              null,
   weight               type_weight          null,
   constraint PK_MWC_CHECKIN_COPPER primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_checkin_lot                                       */
/*==============================================================*/
create table mwc_checkin_lot (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   checkin_pk           type_pk              not null,
   checkin_lot_id       type_id              null,
   feeding_point_id     type_id              null,
   length               type_length          null,
   constraint PK_MWC_CHECKIN_LOT primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_checkin_queue                                     */
/*==============================================================*/
create table mwc_checkin_queue (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   machine_pk           type_pk              null,
   lot_pk               type_pk              null,
   lot_id               type_id              null,
   copper_pk            type_pk              null,
   copper_id            type_id              null,
   feeding_point_id     type_id              null,
   queue_ts             type_datetime        null,
   constraint PK_MWC_CHECKIN_QUEUE primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_checkout                                          */
/*==============================================================*/
create table mwc_checkout (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   checkout_pk          type_pk              null,
   length_intouch       type_length          null,
   length_real          type_length          null,
   length_extra_est     type_length          null,
   length_extra_real    type_length          null,
   weight_copper        type_weight          null,
   outer_diameter       type_length          null,
   wire_type            type_name            null,
   is_welded            type_boolean         null,
   constraint PK_MWC_CHECKOUT primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_checkout_operator                                 */
/*==============================================================*/
create table mwc_checkout_operator (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   checkout_pk          type_pk              null,
   operator_id          type_id              null,
   team_id              type_id              null,
   shift_id             type_id              null,
   batch_id             type_id              null,
   constraint PK_MWC_CHECKOUT_OPERATOR primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_copper                                            */
/*==============================================================*/
create table mwc_copper (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   copper_id            type_id              null,
   factory_id           type_id              null,
   workshop             type_name            null,
   length_origin        type_length          null,
   weight_origin        type_weight          null,
   length               type_length          null,
   weight               type_weight          null,
   status               type_enum_val        null,
   constraint PK_MWC_COPPER primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_lot_po_map                                        */
/*==============================================================*/
create table mwc_lot_po_map (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_pk               type_pk              null,
   lot_id               type_id              null,
   po_id                type_id              null,
   constraint PK_MWC_LOT_PO_MAP primary key (id)
)
go

/*==============================================================*/
/* Table: wm_common_source_lot                                  */
/*==============================================================*/
create table wm_common_source_lot (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_pk               type_pk              not null,
   source_lotPK         type_pk              not null,
   constraint PK_WM_COMMON_SOURCE_LOT primary key (id)
)
go

/*==============================================================*/
/* Table: wmc_checkout_queue                                    */
/*==============================================================*/
create table wmc_checkout_queue (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   machine_pk           type_pk              null,
   vehicle_id           type_id              null,
   queue_ts             type_datetime        null,
   constraint PK_WMC_CHECKOUT_QUEUE primary key (id)
)
go

/*==============================================================*/
/* Table: wmc_copper_history                                    */
/*==============================================================*/
create table wmc_copper_history (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   copper_id            type_id              null,
   event_ts             type_datetime        null,
   factory_id           type_id              null,
   workshop             type_name            null,
   length_origin        type_length          null,
   weight_origin        type_weight          null,
   length               type_length          null,
   weight               type_weight          null,
   status               type_enum_val        null,
   constraint PK_WMC_COPPER_HISTORY primary key (id)
)
go

/*==============================================================*/
/* Table: wmc_lot_detail                                        */
/*==============================================================*/
create table wmc_lot_detail (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_pk               type_pk              not null,
   lot_id               type_id              null,
   length_origin        type_length          null,
   weight_origin        type_weight          null,
   weight_origin_copper type_weight          null,
   length               type_length          null,
   length_intouch       type_length          null,
   weight               type_weight          null,
   weight_copper        type_weight          null,
   quality              type_boolean         null,
   is_melded            type_boolean         null,
   color                type_enum_val        null,
   constraint PK_WMC_LOT_DETAIL primary key (id)
)
go

/*==============================================================*/
/* Table: wmc_lot_history                                       */
/*==============================================================*/
create table wmc_lot_history (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,

   id                   type_pk              not null,
   lot_id               type_id              null,
   event_ts             type_datetime        null,
   factory_id           type_id              null,
   workshop             type_name            null,
   partno               type_id              null,
   status               type_enum_val        null,
   production_date      type_date            null,
   vehicle_id           type_id              null,
   length_origin        type_length          null,
   weight_origin        type_weight          null,
   weight_origin_copper type_weight          null,
   length               type_length          null,
   length_intouch       type_length          null,
   weight               type_weight          null,
   weight_copper        type_weight          null,
   quality              type_boolean         null,
   is_melded            type_boolean         null,
   source_lot           type_pk              null,
   color                type_enum_val        null,
   constraint PK_WMC_LOT_HISTORY primary key (id)
)
go


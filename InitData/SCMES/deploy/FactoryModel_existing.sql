/*==============================================================*/
/* DBMS name:      Microsoft SQL Server 2017 (iuap)             */
/* Created on:     5/14/2019 10:17:21 AM                        */
/*==============================================================*/

use SCMES
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm1_func_template')
            and   type = 'U')
   drop table walsindba.fm1_func_template
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm1_param_template')
            and   type = 'U')
   drop table walsindba.fm1_param_template
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm1_params')
            and   type = 'U')
   drop table walsindba.fm1_params
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm1_unit')
            and   type = 'U')
   drop table walsindba.fm1_unit
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm3_team')
            and   type = 'U')
   drop table walsindba.fm3_team
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm4_shift')
            and   type = 'U')
   drop table walsindba.fm4_shift
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm4_teamcalendar')
            and   type = 'U')
   drop table walsindba.fm4_teamcalendar
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm4_teamcalendar_person')
            and   type = 'U')
   drop table walsindba.fm4_teamcalendar_person
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_carrier_model')
            and   type = 'U')
   drop table walsindba.fm6_carrier_model
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_carrierbaseinfo')
            and   type = 'U')
   drop table walsindba.fm6_carrierbaseinfo
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_equipment')
            and   type = 'U')
   drop table walsindba.fm6_equipment
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_equipment_carrier')
            and   type = 'U')
   drop table walsindba.fm6_equipment_carrier
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_equipment_op_point')
            and   type = 'U')
   drop table walsindba.fm6_equipment_op_point
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_equipment_process')
            and   type = 'U')
   drop table walsindba.fm6_equipment_process
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_equipment_status')
            and   type = 'U')
   drop table walsindba.fm6_equipment_status
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_equipment_status_history')
            and   type = 'U')
   drop table walsindba.fm6_equipment_status_history
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_store')
            and   type = 'U')
   drop table walsindba.fm6_store
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm6_warehouse')
            and   type = 'U')
   drop table walsindba.fm6_warehouse
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm7_material')
            and   type = 'U')
   drop table walsindba.fm7_material
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm7_material_cat')
            and   type = 'U')
   drop table walsindba.fm7_material_cat
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm7_material_unit')
            and   type = 'U')
   drop table walsindba.fm7_material_unit
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm8_basic_process')
            and   type = 'U')
   drop table walsindba.fm8_basic_process
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm8_qc_enum')
            and   type = 'U')
   drop table walsindba.fm8_qc_enum
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm8_qc_items')
            and   type = 'U')
   drop table walsindba.fm8_qc_items
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm8_qc_items_formula')
            and   type = 'U')
   drop table walsindba.fm8_qc_items_formula
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm8_qc_plan')
            and   type = 'U')
   drop table walsindba.fm8_qc_plan
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.fm8_qc_plan_detail')
            and   type = 'U')
   drop table walsindba.fm8_qc_plan_detail
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.mwc_carrier_common')
            and   type = 'U')
   drop table walsindba.mwc_carrier_common
go

if exists (select 1
            from  sysobjects
           where  id = object_id('walsindba.mwc_carrierlog')
            and   type = 'U')
   drop table walsindba.mwc_carrierlog
go


/*==============================================================*/
/* Domain: type_boolean                                         */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_boolean')
    create type type_boolean
       from bit
go

/*==============================================================*/
/* Domain: type_cd                                              */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_cd')
    create type type_cd
       from char varying(40)
go

/*==============================================================*/
/* Domain: type_date                                            */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_date')
    create type type_date
       from char(10)
go

/*==============================================================*/
/* Domain: type_datetime                                        */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_datetime')
    create type type_datetime
       from datetime
go

/*==============================================================*/
/* Domain: type_decimal                                         */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_decimal')
    create type type_decimal
       from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_diameter                                        */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_diameter')
    create type type_diameter
       from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_enum_val                                        */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_enum_val')
    create type type_enum_val
       from int
go

/*==============================================================*/
/* Domain: type_hours                                           */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_hours')
    create type type_hours
       from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_length                                          */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_length')
    create type type_length
       from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_lng_lat                                         */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_lng_lat')
    create type type_lng_lat
       from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_long_name                                       */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_long_name')
    create type type_long_name
       from national char varying(40)
go

/*==============================================================*/
/* Domain: type_memo                                            */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_memo')
    create type type_memo
       from national char varying(Max)
go

/*==============================================================*/
/* Domain: type_name                                            */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_name')
    create type type_name
       from national char varying(20)
go

/*==============================================================*/
/* Domain: type_number                                          */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_number')
    create type type_number
       from int
go

/*==============================================================*/
/* Domain: type_path                                            */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_path')
    create type type_path
       from national char varying(255)
go

/*==============================================================*/
/* Domain: type_pk                                              */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_pk')
    create type type_pk
       from char(32)
go

/*==============================================================*/
/* Domain: type_short_text                                      */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_short_text')
    create type type_short_text
       from national char varying(50)
go

/*==============================================================*/
/* Domain: type_sn                                              */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_sn')
    create type type_sn
       from int
go

/*==============================================================*/
/* Domain: type_version_dec                                     */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_version_dec')
    create type type_version_dec
       from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_version_int                                     */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_version_int')
    create type type_version_int
       from int
go

/*==============================================================*/
/* Domain: type_weight                                          */
/*==============================================================*/
if not exists(select 1 from systypes where name='type_weight')
    create type type_weight
       from decimal(10,3)
go

/*==============================================================*/
/* Table: fm1_func_template                                     */
/*==============================================================*/
create table walsindba.fm1_func_template (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   template_user        type_cd              null,
   code                 type_cd              null,
   name                 type_name            null,
   module_cd            type_cd              null,
   function_cd          type_cd              null,
   content              type_memo            null,
   sort_order           type_sn              null,
   constraint PK_FM1_FUNC_TEMPLATE primary key (id)
)
go

/*==============================================================*/
/* Table: fm1_param_template                                    */
/*==============================================================*/
create table walsindba.fm1_param_template (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_name            null,
   note                 type_memo            null,
   data_type            type_enum_val        null,
   def_value            type_short_text      null,
   range                type_memo            null,
   edit_style           type_enum_val        null,
   reference_class      type_short_text      null,
   group_code           type_cd              null,
   group_name           type_name            null,
   module_id            type_pk              null,
   level                type_enum_val        null,
   is_enabled           type_boolean         null,
   biz_type_id          type_enum_val        null,
   constraint PK_FM1_PARAM_TEMPLATE primary key (id)
)
go

/*==============================================================*/
/* Table: fm1_params                                            */
/*==============================================================*/
create table walsindba.fm1_params (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   factory_pk           type_pk              not null,
   param_template_pk    type_pk              null,
   value                type_short_text      null,
   constraint PK_FM1_PARAMS primary key (id)
)
go

/*==============================================================*/
/* Table: fm1_unit                                              */
/*==============================================================*/
create table walsindba.fm1_unit (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_name            null,
   is_fundamental_unit  type_boolean         null,
   fundamental_unit_pk  type_pk              null,
   exchange_rate        type_decimal         null,
   decimal              type_number          null,
   name_en              type_name            null,
   name_en_plural       type_name            null,
   is_enabled           type_boolean         null,
   constraint PK_FM1_UNIT primary key (id)
)
go

/*==============================================================*/
/* Table: fm3_team                                              */
/*==============================================================*/
create table walsindba.fm3_team (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_name            null,
   leader_cd            type_cd              null,
   type                 type_enum_val        null,
   is_enabled           type_boolean         null,
   constraint PK_FM3_TEAM primary key (id)
)
go

/*==============================================================*/
/* Table: fm4_shift                                             */
/*==============================================================*/
create table walsindba.fm4_shift (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   shift_system_cd      type_cd              null,
   datetime_start       type_datetime        null,
   datetime_end         type_datetime        null,
   working_hours        type_hours           null,
   constraint PK_FM4_SHIFT primary key (id)
)
go

/*==============================================================*/
/* Table: fm4_teamcalendar                                      */
/*==============================================================*/
create table walsindba.fm4_teamcalendar (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   date                 type_date            null,
   shift_pk             type_pk              null,
   team_pk              type_pk              null,
   constraint PK_FM4_TEAMCALENDAR primary key (id)
)
go

/*==============================================================*/
/* Table: fm4_teamcalendar_person                               */
/*==============================================================*/
create table walsindba.fm4_teamcalendar_person (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   team_calendar_pk     type_pk              null,
   operator_cd          type_cd              null,
   is_transferred       type_boolean         null,
   constraint PK_FM4_TEAMCALENDAR_PERSON primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_carrier_model                                     */
/*==============================================================*/
create table walsindba.fm6_carrier_model (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   carrier_cat_cd       type_cd              null,
   spec                 type_memo            null,
   carcass_diameter     type_number          null,
   disc_diameter        type_number          null,
   gap_length           type_number          null,
   inside_width         type_number          null,
   material_id          type_pk              null,
   material_cd          type_cd              null,
   capacity             type_weight          null,
   piece_count          type_number          null,
   note                 type_memo            null,
   constraint PK_FM6_CARRIER_MODEL primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_carrierbaseinfo                                   */
/*==============================================================*/
create table walsindba.fm6_carrierbaseinfo (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   factory_cd           type_cd              null,
   carrier_model_pk     type_pk              null,
   carrier_model_cd     type_cd              null,
   note                 type_memo            null,
   tag1                 type_name            null,
   tag2                 type_name            null,
   tag3                 type_name            null,
   tag4                 type_name            null,
   constraint PK_FM6_CARRIERBASEINFO primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_equipment                                         */
/*==============================================================*/
create table walsindba.fm6_equipment (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_long_name       null,
   short_name           type_name            null,
   spec                 type_memo            null,
   process_pk           type_pk              null,
   process_cd           type_cd              null,
   is_batch_equipment   type_boolean         null,
   base_type_cd         type_enum_val        null,
   level_cd             type_enum_val        null,
   checkin_out_type_cd  type_cd              null,
   factory_pk           type_pk              null,
   factory_cd           type_cd              null,
   factory_name         type_name            null,
   dep_pk               type_pk              null,
   dep_cd               type_cd              null,
   dep_name             type_name            null,
   warehouse_pk         type_pk              null,
   warehouse_cd         type_cd              null,
   warehouse_name       type_name            null,
   parent_pk            type_pk              null,
   longitude            type_lng_lat         null,
   latitude             type_lng_lat         null,
   capacity             type_decimal         null,
   unit_capacity_pk     type_pk              null,
   unit_capacity_cd     type_cd              null,
   unit_capacity_name   type_name            null,
   is_critical          type_boolean         null,
   note                 type_memo            null,
   constraint PK_FM6_EQUIPMENT primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_equipment_carrier                                 */
/*==============================================================*/
create table walsindba.fm6_equipment_carrier (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   equipment_pk         type_pk              null,
   equipment_cd         type_cd              null,
   carrier_model_pk     type_pk              null,
   carrier_model_cd     type_cd              null,
   check_type           type_enum_val        null,
   note                 type_memo            null,
   constraint PK_FM6_EQUIPMENT_CARRIER primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_equipment_op_point                                */
/*==============================================================*/
create table walsindba.fm6_equipment_op_point (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   equiment_pk          type_pk              null,
   op_point_type_cd     type_cd              null,
   name                 type_memo            null,
   note                 type_memo            null,
   constraint PK_FM6_EQUIPMENT_OP_POINT primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_equipment_process                                 */
/*==============================================================*/
create table walsindba.fm6_equipment_process (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   equipment_pk         type_pk              not null,
   equipment_cd         type_cd              null,
   process_pk           type_pk              not null,
   process_cd           type_cd              null,
   constraint PK_FM6_EQUIPMENT_PROCESS primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_equipment_status                                  */
/*==============================================================*/
create table walsindba.fm6_equipment_status (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   equipment_pk         type_pk              not null,
   status_cd            type_cd              null,
   reason               type_memo            null,
   constraint PK_FM6_EQUIPMENT_STATUS primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_equipment_status_history                          */
/*==============================================================*/
create table walsindba.fm6_equipment_status_history (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   equipment_pk         type_pk              not null,
   status_cd            type_cd              null,
   reason               type_memo            null,
   constraint PK_FM6_EQUIPMENT_STATUS_HISTOR primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_store                                             */
/*==============================================================*/
create table walsindba.fm6_store (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_name            null,
   warehouse_pk         type_pk              null,
   in_priority          type_number          null,
   out_priority         type_number          null,
   ppl_in_charge        type_pk              null,
   volume               type_weight          null,
   is_inspection_store  type_boolean         null,
   is_enabled           type_boolean         null,
   constraint PK_FM6_STORE primary key (id)
)
go

/*==============================================================*/
/* Table: fm6_warehouse                                         */
/*==============================================================*/
create table walsindba.fm6_warehouse (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_name            null,
   is_store_mgt         type_boolean         null,
   is_enabled           type_boolean         null,
   is_scrap_wh          type_boolean         null,
   is_outsource_wh      type_boolean         null,
   is_bonded_wh         type_boolean         null,
   is_production_wh     type_boolean         null,
   converter            type_pk              null,
   phone_no             type_short_text      null,
   ppl_in_charge        type_pk              null,
   addr                 type_memo            null,
   longitute            type_lng_lat         null,
   latitude             type_lng_lat         null,
   constraint PK_FM6_WAREHOUSE primary key (id)
)
go

/*==============================================================*/
/* Table: fm7_material                                          */
/*==============================================================*/
create table walsindba.fm7_material (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              null,
   name                 type_long_name       null,
   cat_pk               type_pk              null,
   name_en              type_long_name       null,
   name_abbr            type_cd              null,
   unit_pk              type_pk              null,
   spec                 type_memo            null,
   spec_en              type_memo            null,
   model                type_name            null,
   image_path           type_path            null,
   brand                type_name            null,
   is_enabled           type_boolean         null,
   custom_product_id    type_cd              null,
   custom_product_name  type_name            null,
   barcode              type_memo            null,
   mnemonic_code        type_memo            null,
   version              type_version_int     null,
   application_form_id  type_cd              null,
   is_semiproduct       type_boolean         null,
   attr1                type_decimal         null,
   attr2                type_short_text      null,
   constraint PK_FM7_MATERIAL primary key (id)
)
go

/*==============================================================*/
/* Table: fm7_material_cat                                      */
/*==============================================================*/
create table walsindba.fm7_material_cat (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              not null,
   name                 type_long_name       not null,
   parent_cat_pk        type_pk              null,
   is_enabled           type_boolean         not null,
   note                 type_memo            null,
   constraint PK_FM7_MATERIAL_CAT primary key (id)
)
go

/*==============================================================*/
/* Table: fm7_material_unit                                     */
/*==============================================================*/
create table walsindba.fm7_material_unit (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   material_pk          type_pk              null,
   unit_pk              type_pk              null,
   exchange_rate        type_decimal         null,
   is_fixed_exchange    type_boolean         null,
   constraint PK_FM7_MATERIAL_UNIT primary key (id)
)
go

/*==============================================================*/
/* Table: fm8_basic_process                                     */
/*==============================================================*/
create table walsindba.fm8_basic_process (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              not null,
   name                 type_name            not null,
   name_en              type_pk              null,
   is_enabled           type_boolean         not null,
   is_virtual_process   type_boolean         null,
   station_pk           type_pk              null,
   station_cd           type_cd              null,
   station_name         type_name            null,
   constraint PK_FM8_BASIC_PROCESS primary key (id)
)
go

/*==============================================================*/
/* Table: fm8_qc_enum                                           */
/*==============================================================*/
create table walsindba.fm8_qc_enum (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   item_pk              type_pk              not null,
   sn                   type_sn              not null,
   description          type_name            not null,
   is_enabled           type_boolean         not null,
   constraint PK_FM8_QC_ENUM primary key (id)
)
go

/*==============================================================*/
/* Table: fm8_qc_items                                          */
/*==============================================================*/
create table walsindba.fm8_qc_items (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              not null,
   name                 type_name            not null,
   type_cd              type_enum_val        not null,
   unit_pk              type_pk              not null,
   display_sn           type_number          null,
   is_formula           type_boolean         not null,
   value_type_cd        type_enum_val        null,
   digits               type_number          null,
   decimals             type_number          null,
   group_name           type_name            null,
   note                 type_memo            null,
   constraint PK_FM8_QC_ITEMS primary key (id)
)
go

/*==============================================================*/
/* Table: fm8_qc_items_formula                                  */
/*==============================================================*/
create table walsindba.fm8_qc_items_formula (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   item_pk              type_pk              not null,
   formula              type_memo            not null,
   formula_description  type_memo            null,
   version              type_decimal         not null,
   is_current           type_boolean         not null,
   constraint PK_FM8_QC_ITEMS_FORMULA primary key (id)
)
go

/*==============================================================*/
/* Table: fm8_qc_plan                                           */
/*==============================================================*/
create table walsindba.fm8_qc_plan (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_cd              not null,
   name                 type_name            not null,
   plan_type_cd         type_cd              not null,
   spec_cd              type_cd              not null,
   material_pk          type_pk              null,
   grade_cd             type_cd              null,
   process_pk           type_pk              null,
   sample_point_pk      type_pk              null,
   is_cycle             type_boolean         not null,
   cycle_time           type_decimal         null,
   cycle_unit           type_enum_val        null,
   version              type_decimal         not null,
   is_current_ver       type_boolean         not null,
   report_template      type_memo            null,
   note                 type_memo            null,
   constraint PK_FM8_QC_PLAN primary key (id)
)
go

/*==============================================================*/
/* Table: fm8_qc_plan_detail                                    */
/*==============================================================*/
create table walsindba.fm8_qc_plan_detail (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   plan_pk              type_pk              null,
   item_pk              type_pk              null,
   std                  type_short_text      null,
   upper_bound          type_short_text      null,
   is_upper_bound_closed type_boolean         null,
   lower_bound          type_short_text      null,
   is_lower_bound_closed type_boolean         null,
   value_type           type_enum_val        null,
   decimals             type_number          null,
   digits               type_number          null,
   data_source          type_enum_val        null,
   formula              type_memo            null,
   def_lab_pk           type_pk              null,
   def_qc_site_pk       type_pk              null,
   method_pk            type_pk              null,
   condition_1          type_memo            null,
   condition_2          type_memo            null,
   condition_3          type_memo            null,
   condition_4          type_memo            null,
   condition_5          type_memo            null,
   constraint PK_FM8_QC_PLAN_DETAIL primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_carrier_common                                    */
/*==============================================================*/
create table walsindba.mwc_carrier_common (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   carrier_pk           type_pk              not null,
   carrier_cd           type_cd              null,
   status               type_enum_val        null,
   carrier_model_pk     type_pk              null,
   carrier_model_cd     type_cd              null,
   lot_pk               type_pk              null,
   lot_cd               type_cd              null,
   equipment_pk         type_pk              null,
   warehouse_pk         type_pk              null,
   store_place_pk       type_pk              null,
   note                 type_memo            null,
   constraint PK_MWC_CARRIER_COMMON primary key (id)
)
go

/*==============================================================*/
/* Table: mwc_carrierlog                                        */
/*==============================================================*/
create table walsindba.mwc_carrierlog (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   carrier_pk           type_pk              not null,
   carrier_cd           type_cd              null,
   status               type_enum_val        null,
   carrier_model_pk     type_pk              null,
   carrier_model_cd     type_cd              null,
   lot_pk               type_pk              null,
   lot_cd               type_cd              null,
   equipment_pk         type_pk              null,
   warehouse_pk         type_pk              null,
   store_place_pk       type_pk              null,
   note                 type_memo            null,
   constraint PK_MWC_CARRIERLOG primary key (id)
)
go


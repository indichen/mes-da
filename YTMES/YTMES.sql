/*==============================================================*/
/* Database name:  YTMES                                        */
/* DBMS name:      Microsoft SQL Server 2017 (iuap)             */
/* Created on:     2019/3/25 下午 07:38:01                        */
/*==============================================================*/


use YTMES
go

if exists (select 1
            from  sysobjects
           where  id = object_id('cust_product_type')
            and   type = 'U')
   drop table cust_product_type
go

if exists (select 1
            from  sysobjects
           where  id = object_id('cust_quality_code')
            and   type = 'U')
   drop table cust_quality_code
go

if exists (select 1
            from  sysobjects
           where  id = object_id('cust_spec')
            and   type = 'U')
   drop table cust_spec
go

if exists (select 1
            from  sysobjects
           where  id = object_id('cust_usage_code')
            and   type = 'U')
   drop table cust_usage_code
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaa_application')
            and   type = 'U')
   drop table mtaa_application
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaa_application_exterior')
            and   type = 'U')
   drop table mtaa_application_exterior
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaa_application_mechanical')
            and   type = 'U')
   drop table mtaa_application_mechanical
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaa_application_others')
            and   type = 'U')
   drop table mtaa_application_others
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaa_application_recipe')
            and   type = 'U')
   drop table mtaa_application_recipe
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaa_material')
            and   type = 'U')
   drop table mtaa_material
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_grade_no')
            and   type = 'U')
   drop table mtad_grade_no
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_grade_qc_plan')
            and   type = 'U')
   drop table mtad_grade_qc_plan
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_grade_tag')
            and   type = 'U')
   drop table mtad_grade_tag
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_scrap_type')
            and   type = 'U')
   drop table mtad_scrap_type
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_scrap_type_color')
            and   type = 'U')
   drop table mtad_scrap_type_color
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_steel_color')
            and   type = 'U')
   drop table mtad_steel_color
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_steel_grade')
            and   type = 'U')
   drop table mtad_steel_grade
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtad_steel_series')
            and   type = 'U')
   drop table mtad_steel_series
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaf_material_mechanical')
            and   type = 'U')
   drop table mtaf_material_mechanical
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaf_material_mechanical_spec')
            and   type = 'U')
   drop table mtaf_material_mechanical_spec
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaf_material_status')
            and   type = 'U')
   drop table mtaf_material_status
go

if exists (select 1
            from  sysobjects
           where  id = object_id('mtaf_material_status_product_type')
            and   type = 'U')
   drop table mtaf_material_status_product_type
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

if exists(select 1 from systypes where name='type_short_text')
   drop type type_short_text
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
/* Domain: type_short_text                                      */
/*==============================================================*/
create type type_short_text
   from national char varying(50)
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
/* Table: cust_product_type                                     */
/*==============================================================*/
create table cust_product_type (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   code                 type_id              null,
   name                 type_name            null,
   name_en              type_name            null,
   note                 type_memo            null,
   id                   type_pk              not null,
   constraint PK_CUST_PRODUCT_TYPE primary key (id)
)
go

/*==============================================================*/
/* Table: cust_quality_code                                     */
/*==============================================================*/
create table cust_quality_code (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   code                 type_id              null,
   name                 type_name            null,
   name_en              type_name            null,
   note                 type_memo            null,
   id                   type_pk              not null,
   constraint PK_CUST_QUALITY_CODE primary key (id)
)
go

/*==============================================================*/
/* Table: cust_spec                                             */
/*==============================================================*/
create table cust_spec (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   code                 type_id              null,
   abbr                 type_name            null,
   name                 type_name            null,
   name_en              type_name            null,
   note                 type_memo            null,
   id                   type_pk              not null,
   constraint PK_CUST_SPEC primary key (id)
)
go

/*==============================================================*/
/* Table: cust_usage_code                                       */
/*==============================================================*/
create table cust_usage_code (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   code                 type_id              null,
   name                 type_name            null,
   name_en              type_name            null,
   note                 type_memo            null,
   id                   type_pk              not null,
   constraint PK_CUST_USAGE_CODE primary key (id)
)
go

/*==============================================================*/
/* Table: mtaa_application                                      */
/*==============================================================*/
create table mtaa_application (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   cd                   type_id              not null,
   factory_cd           type_id              null,
   part_no              type_id              null,
   grade_pk             type_pk              null,
   usage                type_memo            null,
   size_description     type_short_text      null,
   bpm_cd               type_id              null,
   constraint PK_MTAA_APPLICATION primary key (id)
)
go

/*==============================================================*/
/* Table: mtaa_application_exterior                             */
/*==============================================================*/
create table mtaa_application_exterior (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   application_pk       type_pk              not null,
   exterior             type_short_text      null,
   min                  type_decimal         null,
   max                  type_decimal         null,
   constraint PK_MTAA_APPLICATION_EXTERIOR primary key (id)
)
go

/*==============================================================*/
/* Table: mtaa_application_mechanical                           */
/*==============================================================*/
create table mtaa_application_mechanical (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   application_pk       type_pk              not null,
   mechanical           type_pk              null,
   min                  type_decimal         null,
   max                  type_decimal         null,
   constraint PK_MTAA_APPLICATION_MECHANICAL primary key (id)
)
go

/*==============================================================*/
/* Table: mtaa_application_others                               */
/*==============================================================*/
create table mtaa_application_others (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   application_pk       type_pk              not null,
   others               type_decimal         null,
   description          type_decimal         null,
   constraint PK_MTAA_APPLICATION_OTHERS primary key (id)
)
go

/*==============================================================*/
/* Table: mtaa_application_recipe                               */
/*==============================================================*/
create table mtaa_application_recipe (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   application_pk       type_pk              not null,
   qc_item_pk           type_pk              null,
   min                  type_decimal         null,
   max                  type_decimal         null,
   standard             type_decimal         null,
   constraint PK_MTAA_APPLICATION_RECIPE primary key (id)
)
go

/*==============================================================*/
/* Table: mtaa_material                                         */
/*==============================================================*/
create table mtaa_material (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   cd                   type_id              not null,
   description          type_memo            null,
   product_type_cd      type_id              null,
   status_cd            type_id              null,
   grade_cd             type_id              null,
   spec_cd              type_id              null,
   quality_code_cd      type_id              null,
   mechanical_cd        type_id              null,
   produce_stage_cd     type_id              null,
   constraint PK_MTAA_MATERIAL primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_grade_no                                         */
/*==============================================================*/
create table mtad_grade_no (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   steel_grade_pk       type_pk              null,
   code                 type_id              null,
   scrap_type_pk        type_pk              null,
   analytic_process     type_short_text      null,
   constraint PK_MTAD_GRADE_NO primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_grade_qc_plan                                    */
/*==============================================================*/
create table mtad_grade_qc_plan (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   qc_plan_main         type_pk              not null,
   grade_pk             type_pk              null,
   grade_cd             type_id              null,
   ver                  type_decimal         not null,
   is_current_ver       type_boolean         not null,
   qc_plan1             type_pk              null,
   qc_plan2             type_pk              null,
   qc_plan3             type_pk              null,
   note                 type_memo            null,
   constraint PK_MTAD_GRADE_QC_PLAN primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_grade_tag                                        */
/*==============================================================*/
create table mtad_grade_tag (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_id              null,
   grade_pk             type_pk              null,
   spec_pk              type_pk              null,
   spec_description     type_memo            null,
   tag_description      type_memo            null,
   constraint PK_MTAD_GRADE_TAG primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_scrap_type                                       */
/*==============================================================*/
create table mtad_scrap_type (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_id              null,
   description          type_memo            null,
   bucket_no            type_number          null,
   constraint PK_MTAD_SCRAP_TYPE primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_scrap_type_color                                 */
/*==============================================================*/
create table mtad_scrap_type_color (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   cd                   type_id              null,
   type_pk              type_pk              null,
   color_pk             type_pk              null,
   constraint PK_MTAD_SCRAP_TYPE_COLOR primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_steel_color                                      */
/*==============================================================*/
create table mtad_steel_color (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_id              null,
   description          type_memo            null,
   constraint PK_MTAD_STEEL_COLOR primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_steel_grade                                      */
/*==============================================================*/
create table mtad_steel_grade (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   steel_series_pk      type_pk              null,
   code                 type_id              null,
   name                 type_short_text      null,
   color_pk             type_pk              null,
   color_type_cd        type_id              null,
   by_product           type_short_text      null,
   constraint PK_MTAD_STEEL_GRADE primary key (id)
)
go

/*==============================================================*/
/* Table: mtad_steel_series                                     */
/*==============================================================*/
create table mtad_steel_series (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   code                 type_id              null,
   name                 type_name            null,
   constraint PK_MTAD_STEEL_SERIES primary key (id)
)
go

/*==============================================================*/
/* Table: mtaf_material_mechanical                              */
/*==============================================================*/
create table mtaf_material_mechanical (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   cd                   type_id              null,
   grade_pk             type_pk              null,
   status_pk            type_pk              null,
   size_min             type_decimal         null,
   size_max             type_decimal         null,
   type                 type_short_text      null,
   cust_abbr            type_short_text      null,
   constraint PK_MTAF_MATERIAL_MECHANICAL primary key (id)
)
go

/*==============================================================*/
/* Table: mtaf_material_mechanical_spec                         */
/*==============================================================*/
create table mtaf_material_mechanical_spec (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   cd                   type_id              null,
   code                 type_pk              null,
   min                  type_decimal         null,
   max                  type_decimal         null,
   constraint PK_MTAF_MATERIAL_MECHANICAL_SP primary key (id)
)
go

/*==============================================================*/
/* Table: mtaf_material_status                                  */
/*==============================================================*/
create table mtaf_material_status (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   cd                   type_id              null,
   name                 type_name            null,
   abbr                 type_id              null,
   status_cat_cd        type_id              null,
   process_cd           type_id              null,
   constraint PK_MTAF_MATERIAL_STATUS primary key (id)
)
go

/*==============================================================*/
/* Table: mtaf_material_status_product_type                     */
/*==============================================================*/
create table mtaf_material_status_product_type (
   create_time varchar(64) null,
   create_user varchar(64) null,
   last_modified varchar(64) null,
   last_modify_user varchar(64) null,
   bpm_state decimal(11) null,
   ts varchar(64) null,
   dr decimal(11) null,
   tenant_id varchar(64) null,

   id                   type_pk              not null,
   status_pk            type_pk              null,
   product_type_cd      type_id              null,
   constraint PK_MTAF_MATERIAL_STATUS_PRODUC primary key (id)
)
go


/*==============================================================*/
/* DBMS name:      Microsoft SQL Server 2017 (iuap)             */
/* Created on:     2019/2/18 下午 03:00:55                        */
/*==============================================================*/


if exists (select 1
            from  sysobjects
           where  id = object_id('fm1_unit')
            and   type = 'U')
   drop table fm1_unit
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm3_team')
            and   type = 'U')
   drop table fm3_team
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm4_shift')
            and   type = 'U')
   drop table fm4_shift
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm4_teamcalendar')
            and   type = 'U')
   drop table fm4_teamcalendar
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm4_teamcalendar_person')
            and   type = 'U')
   drop table fm4_teamcalendar_person
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('fm7_material')
            and   name  = 'R09_FK'
            and   indid > 0
            and   indid < 255)
   drop index fm7_material.R09_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('fm7_material')
            and   name  = 'R03_FK'
            and   indid > 0
            and   indid < 255)
   drop index fm7_material.R03_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm7_material')
            and   type = 'U')
   drop table fm7_material
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm7_material_cat')
            and   type = 'U')
   drop table fm7_material_cat
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('fm7_material_unit')
            and   name  = 'R20_FK'
            and   indid > 0
            and   indid < 255)
   drop index fm7_material_unit.R20_FK
go

if exists (select 1
            from  sysindexes
           where  id    = object_id('fm7_material_unit')
            and   name  = 'R04_FK'
            and   indid > 0
            and   indid < 255)
   drop index fm7_material_unit.R04_FK
go

if exists (select 1
            from  sysobjects
           where  id = object_id('fm7_material_unit')
            and   type = 'U')
   drop table fm7_material_unit
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

if exists(select 1 from systypes where name='type_path')
   drop type type_path
go

if exists(select 1 from systypes where name='type_pk')
   drop type type_pk
go

if exists(select 1 from systypes where name='type_sn')
   drop type type_sn
go

if exists(select 1 from systypes where name='type_version_dec')
   drop type type_version_dec
go

if exists(select 1 from systypes where name='type_version_int')
   drop type type_version_int
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
/* Domain: type_path                                            */
/*==============================================================*/
create type type_path
   from national char varying(255)
go

/*==============================================================*/
/* Domain: type_pk                                              */
/*==============================================================*/
create type type_pk
   from char(36)
go

/*==============================================================*/
/* Domain: type_sn                                              */
/*==============================================================*/
create type type_sn
   from int
go

/*==============================================================*/
/* Domain: type_version_dec                                     */
/*==============================================================*/
create type type_version_dec
   from decimal(10,3)
go

/*==============================================================*/
/* Domain: type_version_int                                     */
/*==============================================================*/
create type type_version_int
   from int
go

/*==============================================================*/
/* Domain: type_weight                                          */
/*==============================================================*/
create type type_weight
   from decimal(10,3)
go

/*==============================================================*/
/* Table: fm1_unit                                              */
/*==============================================================*/
create table fm1_unit (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   unit_id              type_id              null,
   unit_name            type_name            null,
   is_fundamental_unit  type_boolean         null,
   fundamental_unit_pk  type_pk              null,
   exchange_rate        type_decimal         null,
   decimal              type_number          null,
   unit_name_en         type_name            null,
   unit_name_en_plural  type_name            null,
   is_enabled           type_boolean         null,
   constraint PK_FM1_UNIT primary key (id)
)
go

/*==============================================================*/
/* Table: fm3_team                                              */
/*==============================================================*/
create table fm3_team (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   team_id              type_id              null,
   team_name            type_name            null,
   team_leader_id       type_id              null,
   team_type            type_enum_val        null,
   is_enabled           type_boolean         null,
   constraint PK_FM3_TEAM primary key (id)
)
go

/*==============================================================*/
/* Table: fm4_shift                                             */
/*==============================================================*/
create table fm4_shift (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   shift_system_id      type_id              null,
   shift_id             type_id              null,
   datetime_start       type_datetime        null,
   datetime_end         type_datetime        null,
   working_hours        type_hours           null,
   constraint PK_FM4_SHIFT primary key (id)
)
go

/*==============================================================*/
/* Table: fm4_teamcalendar                                      */
/*==============================================================*/
create table fm4_teamcalendar (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

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
create table fm4_teamcalendar_person (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   team_calendar_pk     type_pk              null,
   operator_id          type_id              null,
   is_transferred       type_boolean         null,
   constraint PK_FM4_TEAMCALENDAR_PERSON primary key (id)
)
go

/*==============================================================*/
/* Table: fm7_material                                          */
/*==============================================================*/
create table fm7_material (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   cat_pk               type_pk              null,
   material_id          type_id              null,
   material_name        type_name            null,
   material_name_en     type_name            null,
   material_name_abbr   type_id              null,
   unit_pk              type_pk              null,
   spec                 type_memo            null,
   spec_en              type_memo            null,
   model                type_name            null,
   image_path           type_path            null,
   brand                type_name            null,
   is_enabled           type_boolean         null,
   custom_product_id    type_id              null,
   custom_product_name  type_name            null,
   barcode              type_memo            null,
   mnemonic_code        type_memo            null,
   version              type_version_int     null,
   application_form_id  type_id              null,
   constraint PK_FM7_MATERIAL primary key (id)
)
go

/*==============================================================*/
/* Index: R03_FK                                                */
/*==============================================================*/




create nonclustered index R03_FK on fm7_material (cat_pk ASC)
go

/*==============================================================*/
/* Index: R09_FK                                                */
/*==============================================================*/




create nonclustered index R09_FK on fm7_material (unit_pk ASC)
go

/*==============================================================*/
/* Table: fm7_material_cat                                      */
/*==============================================================*/
create table fm7_material_cat (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   cat_id               type_id              not null,
   cat_name             type_name            not null,
   parent_cat_pk        type_pk              null,
   is_enabled           type_boolean         not null,
   note                 type_memo            null,
   constraint PK_FM7_MATERIAL_CAT primary key (id)
)
go

/*==============================================================*/
/* Table: fm7_material_unit                                     */
/*==============================================================*/
create table fm7_material_unit (
   create_time char(19) null,
   create_user char(36) null,
   last_modified char(19) null,
   last_modify_user char(36) null,
   ts datetime null,
   dr bit null,

   id                   type_pk              not null,
   material_pk          type_pk              null,
   unit_pk              type_pk              null,
   unit_name            type_name            null,
   exchange_rate        type_decimal         null,
   is_fixed_exchange    type_boolean         null,
   constraint PK_FM7_MATERIAL_UNIT primary key (id)
)
go

/*==============================================================*/
/* Index: R04_FK                                                */
/*==============================================================*/




create nonclustered index R04_FK on fm7_material_unit (material_pk ASC)
go

/*==============================================================*/
/* Index: R20_FK                                                */
/*==============================================================*/




create nonclustered index R20_FK on fm7_material_unit (unit_pk ASC)
go


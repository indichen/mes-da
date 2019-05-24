truncate table pap.walsindba.c_cust_mo_type;
insert into pap.walsindba.c_cust_mo_type (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (10, N'系統', N'', N'32f08a4f-7acc-440d-aed0-15d95fadfc1c', N'0000000001', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_mo_type (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (20, N'手動', N'', N'60bbf6a1-7784-4d3a-970b-a116de1bf65f', N'0000000002', 0, 0, 1, convert(varchar, getdate(), 121), 0);

truncate table pap.walsindba.c_cust_sap_po_factory;
insert into pap.walsindba.c_cust_sap_po_factory (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values ('SCP1', '電力製造一課', '', '216093cd-453a-4e38-9a04-83a0a27f5737', '0000000001', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_sap_po_factory (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values ('SCG1', '電力製造二課', '', 'b78804d4-03d4-46f8-9e13-844fdac65d5a', '0000000002', 0, 0, 1, convert(varchar, getdate(), 121), 0);

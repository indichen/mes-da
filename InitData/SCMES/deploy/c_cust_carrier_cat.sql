truncate table pap.walsindba.c_cust_carrier_cat;
insert into pap.walsindba.c_cust_carrier_cat (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (N'S', N'S周轉軸', N'', N'5562523f-425a-40b3-87a6-28a852b7e1cf', N'0000000001', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_carrier_cat (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (N'F', N'F成品軸', N'', N'88059c1f-ae59-43ea-9604-a01d29278f2e', N'0000000002', 0, 0, 1, convert(varchar, getdate(), 121), 0);

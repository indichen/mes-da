truncate table pap.walsindba.c_cust_lot_status;
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (0, N'新建', N'', N'34aed771-f6b7-4662-8dcf-37c36cb7417c', N'0000000001', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (10, N'待產', N'', N'33c84cfe-4d15-4a17-8f6e-09d88012a406', N'0000000002', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (20, N'生產中', N'', N'9649ff0f-ec71-4182-930d-08287d1bccc9', N'0000000003', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (30, N'完成', N'', N'b7e0be27-7b4d-45ce-99da-e151a5337e7a', N'0000000004', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (11, N'待驗', N'', N'5ea439df-320a-4881-8aed-97ef2a90f5ad', N'0000000005', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (12, N'檢驗中', N'', N'b61f956d-383f-4d7d-b11d-f54a98dbbe97', N'0000000006', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (40, N'報廢/除賬', N'', N'ef8b299a-c3b0-4933-a9d7-fc0d3c7ef938', N'0000000007', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (80, N'待重工', N'', N'6eb6d8ce-93f4-4eb5-ae01-d52c9e6792b3', N'0000000008', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_lot_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (90, N'暫停', N'', N'6c55fe6b-f9c6-489e-9d31-5155b19fe057', N'0000000009', 0, 0, 1, convert(varchar, getdate(), 121), 0);

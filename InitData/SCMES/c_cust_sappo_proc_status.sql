truncate table pap.walsindba.c_cust_sappo_proc_status;
insert into pap.walsindba.c_cust_sappo_proc_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (10, '新建', '', '5d8a8f04-29a0-4e48-bb8d-4fdc812eb728', '0000000001', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_sappo_proc_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (15, '處理中', '', '148eda9f-1f10-44ae-894d-d1e3a639ecd2', '0000000002', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_sappo_proc_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (20, '完成', '', '3d09465b-3279-4a4a-a40d-8835c3e5068c', '0000000003', 0, 0, 1, convert(varchar, getdate(), 121), 0);
insert into pap.walsindba.c_cust_sappo_proc_status (code, name, note, pk_mdm, mdm_code, mdm_duplicate, mdm_seal, mdm_version, ts, dr) values (30, '失敗', '', '26005638-49fc-4c63-9dd8-12861ea12085', '0000000004', 0, 0, 1, convert(varchar, getdate(), 121), 0);

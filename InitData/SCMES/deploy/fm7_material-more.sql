update scmes.walsindba.fm7_material set is_semiproduct=0 where len(code)=16;
update scmes.walsindba.fm7_material set is_semiproduct=1 where len(code)<>16;
go

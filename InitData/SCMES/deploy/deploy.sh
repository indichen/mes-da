#!/usr/bin/env bash

if [ -z "${SQLDB_HOST}" ]; then
    echo "!!! PLEASE SETUP DB INFO BEFORE RUNNING THIS SCRIPT."
    exit 1
fi

read -p "Initializing database server ${SQLDB_HOST}:${SQLDB_PORT}... Are you sure? " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
fi

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "${VIRTUAL_ENV}" ]; then
    source ${script_dir}/../venv/bin/activate
fi

script_run_sql=${script_dir}/../run_sql.py

pushd ${script_dir}

sql_list=""
sql_list+=" fm8_basic_process.sql"
sql_list+=" fm6_equipment.sql"
sql_list+=" fm6_equipment_status.sql"
sql_list+=" fm6_equipment_process.sql"
sql_list+=" fm6_carrier_model.sql"
sql_list+=" fm6_equipment_carrier.sql"
sql_list+=" fm7_material.sql"
sql_list+=" fm7_material-more.sql"
sql_list+=" fm7_material_cat.sql"
sql_list+=" mwc_copper.sql"

for sql_file in ${sql_list}; do
	python3 ${script_run_sql} ${sql_file} || exit 1
done

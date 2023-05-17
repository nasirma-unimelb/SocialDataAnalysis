#!/usr/bin/env sh

python ./back_end_exposer_dummy.py --couchdb_master_ip ${MASTERNODE} --couchdb_username ${DB_USERNAME} --couchdb_password ${DB_PASSWORD}

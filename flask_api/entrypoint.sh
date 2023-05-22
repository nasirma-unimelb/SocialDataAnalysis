#!/usr/bin/env sh

python ./back_end_exposer.py --couchdb_master_ip ${MASTERNODE} --couchdb_user ${DB_USERNAME} --couchdb_password ${DB_PASSWORD}


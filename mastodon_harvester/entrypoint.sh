#!/usr/bin/env sh

python ./mastodon_harvester.py --ado_api_key ${ADO_API_KEY} --ado_login_url ${ADO_LOGIN} --ado_text_search_mastodon_url ${ADO_SEARCH} --mastodon_api_key ${MASTODON_KEY} --couchdb_master_ip ${COUCHDB_IP} --couchdb_user ${COUCHDB_USER} --couchdb_password ${COUCHDB_PASSWORD}

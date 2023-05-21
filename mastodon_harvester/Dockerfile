# Docker file to run Mastodon Harvester

FROM python:3

ENV ADO_API_KEY, ADO_LOGIN, ADO_SEARCH, MASOTDON_KEY, COUCHDB_IP, COUCHDB_USER, COUCHDB_PASSWORD

ADD . /

RUN pip install -r requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
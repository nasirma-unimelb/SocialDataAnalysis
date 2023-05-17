# Docker file to run Mastodon Harvester

FROM python:3

ENV MASTERNODE DB_USERNAME DB_PASSWORD

ADD . /

RUN pip install -r requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
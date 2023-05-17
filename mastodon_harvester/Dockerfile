# Docker file to run Mastodon Harvester

FROM python:3

ENV TEST1='not-post'

RUN echo $TEST1

ADD . /

RUN pip install -r requirements.txt

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
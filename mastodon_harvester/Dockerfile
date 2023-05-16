# Docker file to run Mastodon Harvester

FROM python:3

ENV TEST1='not-post'

ADD . /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py", echo $TEST1]
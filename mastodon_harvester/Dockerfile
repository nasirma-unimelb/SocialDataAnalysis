# Docker file to run Mastodon Harvester

FROM python:3

ARG TEST1='not-post'

RUN  echo "The default variable value for TEST1 is $TEST1"

ADD . /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]
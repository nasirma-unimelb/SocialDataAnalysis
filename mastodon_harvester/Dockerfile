# Docker file to run Mastodon Harvester

FROM python:3

ARG arg1='not-post'

RUN  echo "The default variable value for arg1 is $arg1"

ADD . /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]
FROM python:3-alpine

MAINTAINER Marko Miskovic <misko23@gmail.com>

COPY app/ /app

RUN \
  pip install -r /app/requirements.txt && \
  mkdir /log

ENTRYPOINT ["python3", "/app/script.py"]

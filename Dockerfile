FROM python:3-alpine

MAINTAINER Marko Miskovic <misko23@gmail.com>

COPY requirements.txt /

RUN \
  pip install -r /requirements.txt && \
  mkdir /log

COPY app/ /app


ENTRYPOINT ["python3", "/app/script.py"]

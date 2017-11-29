FROM python:3.5-alpine
MAINTAINER Luis Boscan <luife642@gmail.com>

ARG DJANGO_DEBUG

ENV PYTHONUNBUFFERED 1

VOLUME /root/.cache/pip/

# Update pip to its latest release
RUN apk update \
    && apk add \
        ca-certificates \
        openssl \
        openssl-dev	\
        gcc \
        libc-dev \
        libxml2-dev \
        libxslt-dev \
        libffi-dev \
    && pip install -U pip \
    && rm -rf /var/cache/apk/*

ADD . /app

WORKDIR /app

RUN sh /app/docker/prepare.sh

EXPOSE 8000

CMD sh /app/docker/run.sh

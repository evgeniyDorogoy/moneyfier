FROM python:3.7-alpine

RUN apk update \
    && apk add --virtual build-dependencies \
        build-base \
        gcc \
        wget \
        git \
        musl-dev \
        postgresql-dev \
        openssl-dev \
        libffi-dev \
    && apk add --no-cache postgresql-libs \
    && apk add \
        bash

WORKDIR /usr/src/moneyfier

COPY . /usr/src/moneyfier


RUN set -xe \
    && pip install pipenv \
    && pipenv --python 3.7 \
    && pipenv install --skip-lock \
    && apk del build-dependencies \
    && rm -rf /var/cache/apk/*

RUN mkdir downloads

EXPOSE 8000

CMD ["pipenv", "run", "python3", "manage.py", "-s"]
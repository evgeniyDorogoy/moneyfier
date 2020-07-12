FROM python:3.7-alpine as dev
COPY ./requirements.txt /usr/src/moneyfier/
WORKDIR /usr/src/moneyfier/
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
    && apk add bash \
    && apk add supervisor\
    && set -xe \
    && pip install -r requirements.txt \
    && apk del build-dependencies \
    && rm -rf /var/cache/apk/*
EXPOSE 8000
CMD ["supervisord", "-c", "supervisord.conf"]

FROM dev as prod
COPY . /usr/src/moneyfier/
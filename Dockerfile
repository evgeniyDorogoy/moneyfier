FROM python:3.6

WORKDIR /usr/src/moneyfier

COPY . /usr/src/moneyfier

RUN set -xe && \
    pip install pipenv && \
    pipenv install --system --dev

EXPOSE 8000

CMD ["python3.6", "manage.py"]
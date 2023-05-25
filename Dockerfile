FROM python:3.11 AS flask

RUN pip install poetry

COPY .env pyproject.toml poetry.lock /core/
WORKDIR /core

RUN poetry install --no-root

COPY /core /core/

CMD ["poetry", "run", "python", "app.py"]

FROM python:3.11 AS rabbitmq

RUN pip install poetry

COPY .env pyproject.toml poetry.lock /core/
WORKDIR /core

RUN poetry install --no-root

COPY /rabbitmq /core/

CMD ["poetry", "run", "python", "consumer.py"]
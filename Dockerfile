FROM python:3.11 as client

RUN pip install poetry

COPY poetry.lock pyproject.toml .env /code/

WORKDIR /code/

COPY /core .

RUN poetry install --no-root

CMD ["poetry", "run", "python", "client.py"]

FROM python:3.11 as server

RUN pip install poetry

COPY poetry.lock pyproject.toml .env /code/

WORKDIR /code/

COPY /core .

RUN poetry install --no-root

CMD ["poetry", "run", "python", "main.py"]
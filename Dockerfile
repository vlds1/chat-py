FROM python:3.11


RUN pip install poetry


COPY .env pyproject.toml poetry.lock /core/
WORKDIR /core

RUN poetry add python-socketio
RUN poetry install --no-root

COPY /core /core/

CMD ["poetry", "run", "python", "app.py"]
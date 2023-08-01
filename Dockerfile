FROM python:3.11

COPY requirements.txt /app/
COPY .env /app/

WORKDIR /app/

RUN pip install -r requirements.txt

COPY /src /app/src/

WORKDIR /app/src/

CMD [ "python", "main.py" ]
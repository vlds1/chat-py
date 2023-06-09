FROM python:3.11
WORKDIR /dev
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.main:app", "--reload"]

# syntax=docker/dockerfile:1

FROM python:3.8.6-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

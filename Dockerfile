# syntax=docker/dockerfile:1

FROM python:3.8.6-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt

#RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]

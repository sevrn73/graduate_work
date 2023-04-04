FROM python:3.9-alpine

WORKDIR /opt/cinema_api

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && \
     pip install -r requirements.txt --no-cache-dir

COPY . .
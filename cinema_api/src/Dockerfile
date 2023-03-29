FROM python:3.9-alpine

WORKDIR /opt/app

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && \
     pip install -r requirements.txt --no-cache-dir

COPY . .
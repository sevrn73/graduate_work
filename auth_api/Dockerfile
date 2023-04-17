FROM python:3.9-alpine


WORKDIR /opt/auth_api

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip && \
     pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8001

RUN chmod +x /opt/auth_api/docker-entrypoint.sh

ENTRYPOINT [ "/opt/auth_api/docker-entrypoint.sh" ]
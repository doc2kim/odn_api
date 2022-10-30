# syntax=docker/dockerfile:1
FROM python:latest

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

COPY . /django
WORKDIR /django

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get upgrade -y && apt-get install -y gdal-bin libgdal-dev

RUN python manage.py collectstatic --noinput 


COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
VOLUME ["/django"]

ENTRYPOINT [ "sh", "./docker-entrypoint.sh" ]

# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.9.14

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

WORKDIR /odn_api

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y && apt-get install -y gdal-bin libgdal-dev


COPY requirements.txt /odn_api/

ADD . /odn_api


RUN pip install -r requirements.txt

# COPY ./entrypoint.sh /

# ENTRYPOINT ["sh", "/entrypoint.sh"]
FROM python:3.11-slim as builder

RUN pip install --no-cache-dir flake8
RUN apt-get update && apt-get install -y \
	libcairo2-dev \
	libjpeg-dev \
	libpango1.0-dev \
	libgif-dev \
	libpng-dev \
	build-essential \
	g++

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM builder as installer

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM installer as application

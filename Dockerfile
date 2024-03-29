# Pull base image
FROM python:3.8

RUN pip install --upgrade pip setuptools

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 5000
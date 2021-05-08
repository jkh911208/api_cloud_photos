# Pull base image
FROM python:3.9

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 5000
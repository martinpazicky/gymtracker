FROM python:3.10.8-slim-buster

ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/


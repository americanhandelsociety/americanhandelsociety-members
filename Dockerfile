# Credit: https://github.com/datamade/how-to/blob/master/docker/templates/python-docker-env/%7B%7Bcookiecutter.directory_name%7D%7D/Dockerfile
# Extend the base Python image
# https://hub.docker.com/_/python
FROM python:3.9.5-slim-buster

LABEL maintainer "Regina Compton <reginafcompton@gmail.com>"

WORKDIR /app

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
RUN pip install pipenv && pipenv install --system && pipenv install --dev --system

# Copy entrypoint script (runs migrations and server).
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app

ENTRYPOINT [ "/app/entrypoint.sh" ]
# Credit: https://github.com/datamade/how-to/blob/master/docker/templates/python-docker-env/%7B%7Bcookiecutter.directory_name%7D%7D/Dockerfile
# Extend the base Python image
# https://hub.docker.com/_/python
FROM python:3.9

LABEL maintainer "Regina Compton <reginafcompton@gmail.com>"

WORKDIR /app

RUN apt-get update && \
    apt-get install curl

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock
RUN pip install pipenv && pipenv install --system && pipenv install --dev --system

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
# Copy the contents of the current host directory (i.e., our app code) into
# the container.
COPY . /app

# Add a bogus env var for the Django secret key in order to allow us to run
# the 'collectstatic' management command
ENV DJANGO_SECRET_KEY 'foobar'
# Add a bogus env var for Debug to make sure that Django compressor can run
ENV DJANGO_DEBUG 'False'

# Build static files into the container
RUN python manage.py collectstatic --noinput

ENTRYPOINT [ "/app/entrypoint.sh" ]
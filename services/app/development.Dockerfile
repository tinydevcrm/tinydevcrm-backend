# Dockerized development environment.

# pull official base image
FROM python:3.8.0

# set work directory
ARG BASEDIR='/usr/src/app'

WORKDIR ${BASEDIR}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get -y update && \
    apt-get -y install postgresql-server-dev-all gcc python3-dev libc-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./conf/requirements.txt ${BASEDIR}/requirements.txt
RUN pip install -r requirements.txt

# Install netcat for entrypoint.
RUN apt-get -y install netcat

# copy entrypoint.sh
COPY ./conf/entrypoint.development.sh /usr/entrypoint.sh

# copy project
COPY . ${BASEDIR}

# run entrypoint.sh
#
# NOTE: Neither 'ARG' nor 'ENV' will be recognized by ENTRYPOINT.
ENTRYPOINT [ "/usr/entrypoint.sh" ]

#!/usr/bin/env bash
#
# Run development environment locally.
#
# Assumptions:
#
# The following dependencies are installed and available in $PATH:
#
# - `git` (I am using v2.25.2)
# - `docker` (I am using v19.03.6, build 369ce74a3c)
# - `docker-compose` (I am using v1.23.2, build 1110ad01)
#
# No other containers are currently running that assume ports taken up by
# $GIT_REPO_ROOT/services/docker-compose.development.yaml.
#
# `docker volume ls` does not have service-specific dependencies.
#
# `docker network ls` does not have service-specific dependencies.
#
# If you're not sure, run `docker system prune -a` in order to clear all
# `docker` context on local.

# Print out commands to the terminal as they run.
set -x

GIT_REPO_ROOT=$(git rev-parse --show-toplevel)

$(which docker-compose) \
    -f $GIT_REPO_ROOT/services/docker-compose.development.yaml \
    --verbose up -d --build

xdg-open http://localhost:8000/admin

# That should be it. Here's some commands that could come in useful:

# `docker-compose -f $GIT_REPO_ROOT/services/docker-compose.development.yaml
# down -v` tears down the containers and the persistent volumes.

# `docker logs {service_web_1|service_db_1}` prints out the docker logs for PID
# 1 to stdout for the given container, as noted in `docker ps`.

# `docker-compose -f $GIT_REPO_ROOT/services/docker-compose.development.yaml
# exec $CONTAINER_ALIAS "$@"` executes a command '$@' within a container denoted
# with alias $CONTAINER_ALIAS. For example:

# `docker-compose -f $GIT_REPO_ROOT/services/docker-compose.development.yaml
# exec web python manage.py collectstatic --no-input --clear` collects static
# files and places them into the Django context.

# `docker-compose -f services/docker-compose.development.yaml exec db psql
# --username=tinydevcrm --dbname=tinydevcrm_api_prod` enters into the `psql`
# context for the PostgreSQL database.

# `docker-compose -f services/docker-compose.development.yaml exec web python
# manage.py migrate --noinput` runs a Django migration.

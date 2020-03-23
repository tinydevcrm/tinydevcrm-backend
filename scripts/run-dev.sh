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
    up -d --build

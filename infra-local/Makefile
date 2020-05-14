#!/usr/bin/env make

.PHONY: version run-dev clean-dev

export APP_VERSION ?= $(shell git rev-parse --short HEAD)
export GIT_REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

# NOTE: Don't run the web Docker container in detached mode, since `python -m
# ipdb` will hook within `settings.py` and cause the container to fail to start.
run-dev:
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-local/docker-compose.development.yaml --verbose up -d --build db
	@echo "Open http://localhost:8000 to see results."
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-local/docker-compose.development.yaml --verbose run --service-ports web

clean-dev:
	docker-compose -f ${GIT_REPO_ROOT}/infra-local/docker-compose.development.yaml down -v
	docker images -q -f dangling=true -f label=application=todobackend | xargs -I ARGS docker rmi -f --no-prune ARGS

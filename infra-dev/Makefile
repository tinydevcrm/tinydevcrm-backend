#!/usr/bin/env make

export APP_VERSION ?= $(shell git rev-parse --short HEAD)
export GIT_REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

# For building libraries required for PostgreSQL.
export NUM_PHYSICAL_CPUS ?= $(shell nproc)
export PHYSICAL_MEMORY_KILOBYTES ?= $(shell cat /proc/meminfo | grep MemTotal | awk '{print $$2}')K

version:
	@ echo '{"Version": "$(APP_VERSION)"}'

numcpus:
	@ echo $(NUM_PHYSICAL_CPUS)

memkb:
	@ echo $(PHYSICAL_MEMORY_KILOBYTES)

# NOTE: Don't run the web Docker container in detached mode, since `python -m
# ipdb` will hook within `settings.py` and cause the container to fail to start.
dev-up:
	GIT_REPO_ROOT=${GIT_REPO_ROOT} NUM_PHYSICAL_CPUS=$(NUM_PHYSICAL_CPUS) PHYSICAL_MEMORY_KILOBYTES=$(PHYSICAL_MEMORY_KILOBYTES) docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml build db-builder
	GIT_REPO_ROOT=${GIT_REPO_ROOT} NUM_PHYSICAL_CPUS=$(NUM_PHYSICAL_CPUS) PHYSICAL_MEMORY_KILOBYTES=$(PHYSICAL_MEMORY_KILOBYTES) docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose up -d --build db
	@echo "Open http://localhost:8000 to see results."
	GIT_REPO_ROOT=${GIT_REPO_ROOT} NUM_PHYSICAL_CPUS=$(NUM_PHYSICAL_CPUS) PHYSICAL_MEMORY_KILOBYTES=$(PHYSICAL_MEMORY_KILOBYTES) docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose run --service-ports web

dev-down:
	docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml down -v
	docker images -q -f dangling=true -f label=application=todobackend | xargs -I ARGS docker rmi -f --no-prune ARGS

# Change PGPASSWORD, --username, and --db values to match those in
# db/conf/.env.dev
dev-psql:
	PGPASSWORD=tinydevcrm docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml exec db psql --username=tinydevcrm --db=tinydevcrm_api_dev

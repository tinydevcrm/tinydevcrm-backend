#!/usr/bin/env make

export APP_VERSION ?= $(shell git rev-parse --short HEAD)
export GIT_REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

version:
	@ echo '{"Version": "$(APP_VERSION)"}'

# NOTE: Don't run the web Docker container in detached mode, since `python -m
# ipdb` will hook within `settings.py` and cause the container to fail to start.
dev-up:
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose up -d --build db pushpin
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml build web
	# NOTE: Moved manage.py actions in order to avoid Django lifecycle
	# management problems; see 'channels_app/apps.py'.
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose run web python3 manage.py flush --no-input
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose run web python3 manage.py migrate
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose run web python3 manage.py collectstatic --no-input
	# Start the broker b/w separate PostgreSQL and Pushpin channels as a
	# separate Docker container.
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose up -d --build broker
	# NOTE: Setting the hardcoded hostname alias is important for configuring
	# /etc/pushpin/routes, which is important for sending the response to the
	# appropriate location.
	GIT_REPO_ROOT=${GIT_REPO_ROOT} docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml --verbose run --name web --service-ports web

dev-down:
	docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml down -v
	docker images -q -f dangling=true -f label=application=todobackend | xargs -I ARGS docker rmi -f --no-prune ARGS

# Change PGPASSWORD, --username, and --db values to match those in
# db/conf/.env.dev
dev-psql:
	PGPASSWORD=tinydevcrm docker-compose -f ${GIT_REPO_ROOT}/infra-dev/docker-compose.development.yaml exec db psql --username=tinydevcrm --db=tinydevcrm_api_dev

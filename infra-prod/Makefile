#!/usr/bin/env make

export APP_VERSION ?= $(shell git rev-parse --short HEAD)
export GIT_REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

version:
	@ echo '{"Version": "$(APP_VERSION)"}'

export AWS_PROFILE=tinydevcrm-user
export AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text)
export AWS_REGION ?= $(shell aws configure get region)
export AWS_ECR_APP_REPOSITORY_NAME=tinydevcrm-ecr/app
export AWS_ECR_DB_REPOSITORY_NAME=tinydevcrm-ecr/db
export AWS_ECR_NGINX_REPOSITORY_NAME=tinydevcrm-ecr/nginx

prod-config:
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml config

prod-up:
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml --verbose up -d --build db
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml --verbose up --build --abort-on-container-exit migrate
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml --verbose run app python3 manage.py collectstatic --no-input
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml --verbose run app python3 manage.py createcustomsuperuser --no-input --primary_email 'test@test.com' --password 'test'
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml --verbose up -d --build
	sleep 5
	xdg-open http://localhost:1337/admin

prod-down:
	docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml down -v
	docker images -q -f dangling=true -f label=application=tinydevcrm | xargs -I ARGS docker rmi -f --no-prune ARGS

# Change PGPASSWORD, --username, and --db values to match those in
# db/conf/.env.aws
local-psql:
	PGPASSWORD=tinydevcrm docker-compose -f ${GIT_REPO_ROOT}/infra-prod/docker-compose.aws.yaml exec db psql --username=tinydevcrm --db=tinydevcrm_api_prod

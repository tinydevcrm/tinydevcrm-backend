#!/usr/bin/env make

export APP_VERSION ?= $(shell git rev-parse --short HEAD)
export GIT_REPO_ROOT ?= $(shell git rev-parse --show-toplevel)

# Change to your AWS IAM profile, set up as part of `iam.yaml`..
export AWS_PROFILE=tinydevcrm-user

export AWS_ACCOUNT_ID ?= $(shell aws sts get-caller-identity --query Account --output text)
export AWS_REGION ?= $(shell aws configure get region)
export AWS_ECR_APP_REPOSITORY_NAME=tinydevcrm-ecr/app
export AWS_ECR_DB_REPOSITORY_NAME=tinydevcrm-ecr/db
export AWS_ECR_NGINX_REPOSITORY_NAME=tinydevcrm-ecr/nginx

version:
	@ echo '{"Version": "$(APP_VERSION)"}'

login:
	$$(aws ecr get-login --no-include-email)

publish-app: login
	docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_APP_REPOSITORY_NAME}:${APP_VERSION} -f ${GIT_REPO_ROOT}/services/app/aws.Dockerfile ${GIT_REPO_ROOT}/services/app
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_APP_REPOSITORY_NAME}:${APP_VERSION}

	docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_APP_REPOSITORY_NAME}:latest -f ${GIT_REPO_ROOT}/services/app/aws.Dockerfile ${GIT_REPO_ROOT}/services/app
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_APP_REPOSITORY_NAME}:latest

publish-db: login
	docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_DB_REPOSITORY_NAME}:${APP_VERSION} -f ${GIT_REPO_ROOT}/services/db/Dockerfile ${GIT_REPO_ROOT}/services/db
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_DB_REPOSITORY_NAME}:${APP_VERSION}

	docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_DB_REPOSITORY_NAME}:latest -f ${GIT_REPO_ROOT}/services/db/Dockerfile ${GIT_REPO_ROOT}/services/db
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_DB_REPOSITORY_NAME}:latest

publish-nginx: login
	docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_NGINX_REPOSITORY_NAME}:${APP_VERSION} -f ${GIT_REPO_ROOT}/services/nginx/aws.Dockerfile ${GIT_REPO_ROOT}/services/nginx
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_NGINX_REPOSITORY_NAME}:${APP_VERSION}

	docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_NGINX_REPOSITORY_NAME}:latest -f ${GIT_REPO_ROOT}/services/nginx/aws.Dockerfile ${GIT_REPO_ROOT}/services/nginx
	docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${AWS_ECR_NGINX_REPOSITORY_NAME}:latest

# AWS remote commands #

# This operation implies you already have a set of root account credentials on
# your local compute instance, or a set of credentials with administrator
# access. If you don't, download the credentials from AWS and save using 'aws
# configure'. Then, be sure to export AWS_PROFILE env variable so that
# '--profile' doesn't need to be passed.
#
# NOTE: Copy over file://aws-iam.example.json to file://aws-iam.json and replace
# parameters in order for this command to work properly.
iam-create:
	aws cloudformation create-stack --stack-name tinydevcrm-iam --template-body file://aws-iam.yaml --parameters file://aws-iam.json --capabilities CAPABILITY_NAMED_IAM

iam-deploy:
	# Don't apply parameter overrides via '--parameter-overrides', parameters
	# should be passed during stack creation
	aws cloudformation deploy --stack-name tinydevcrm-iam --template-file aws-iam.yaml --capabilities CAPABILITY_NAMED_IAM

iam-terminate:
	aws cloudformation delete-stack --stack-name tinydevcrm-iam

vpc-create:
	aws cloudformation create-stack --stack-name tinydevcrm-ec2-networking --template-body file://aws-ec2-networking.yaml --capabilities CAPABILITY_NAMED_IAM

vpc-deploy:
	aws cloudformation deploy --stack-name tinydevcrm-ec2-networking --template-file aws-ec2-networking.yaml --capabilities CAPABILITY_NAMED_IAM

vpc-terminate:
	aws cloudformation delete-stack --stack-name tinydevcrm-ec2-networking

ecr-create:
	aws cloudformation create-stack --stack-name tinydevcrm-ecr --template-body file://ecr.yaml --capabilities CAPABILITY_NAMED_IAM

ecr-deploy:
	aws cloudformation deploy --stack-name tinydevcrm-ecr --template-file ecr.yaml --capabilities CAPABILITY_NAMED_IAM

ecr-terminate:
	aws cloudformation delete-stack --stack-name tinydevcrm-ecr

persist-create:
	aws cloudformation create-stack --stack-name tinydevcrm-persist --template-body file://persist.yaml --capabilities CAPABILITY_NAMED_IAM

persist-deploy:
	aws cloudformation deploy --stack-name tinydevcrm-persist --template-file persist.yaml --capabilities CAPABILITY_NAMED_IAM

persist-terminate:
	aws cloudformation delete-stack --stack-name tinydevcrm-persist

app-create: publish-app
	aws cloudformation create-stack --stack-name tinydevcrm-app --template-body file://app.yaml --parameters file://app-params.json --capabilities CAPABILITY_NAMED_IAM

app-deploy:
	aws cloudformation deploy --stack-name tinydevcrm-app --template-file app.yaml --capabilities CAPABILITY_NAMED_IAM

app-terminate:
	aws cloudformation delete-stack --stack-name tinydevcrm-app

db-create: publish-db
	aws cloudformation create-stack --stack-name tinydevcrm-db --template-body file://db.yaml --parameters file://db-params.json --capabilities CAPABILITY_NAMED_IAM

db-deploy:
	aws cloudformation deploy --stack-name tinydevcrm-db --template-file db.yaml --capabilities CAPABILITY_NAMED_IAM

db-terminate:
	aws cloudformation delete-stack --stack-name tinydevcrm-db

# Conditioned on having a deployed database up and running. # Credentials part
# of `db.yaml`.
#
# In order to set env variables within the same target, add env to target:
# https://stackoverflow.com/a/15230658/1497211
psql: AWS_NLB_DNS_NAME=$(shell aws cloudformation describe-stacks --stack-name tinydevcrm-db --query "Stacks[0].Outputs[?OutputKey=='DatabaseNLBDNSName'].OutputValue" --output text)
psql:
	PGPASSWORD=tinydevcrm psql -U tinydevcrm -h $(AWS_NLB_DNS_NAME) -d tinydevcrm-api-prod

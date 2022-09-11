.PHONY: all

SHELL=/bin/bash -e

.DEFAULT_GOAL := help

DC = docker-compose
EXEC_MANAGE = exec app python manage.py

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## build images
	${DC} build

up: ## start docker environment
	${DC} up -d
	${DC} ps

down: ## stop docker dev environment
	${DC} down --remove-orphans

purge: ## stop docker dev environment and remove orphans and volumes
	${DC} down --volumes --remove-orphans

migrate: ## migrate
	${DC} ${EXEC_MANAGE} migrate --noinput

makemigrations: ## makemigrations
	${DC} ${EXEC_MANAGE} makemigrations --noinput

collectstatic: ## collectstatic
	${DC} ${EXEC_MANAGE} collectstatic --noinput

createsuperuser: ## createsuperuser
	${DC} ${EXEC_MANAGE} createsuperuser --noinput &> /dev/null || true

env-cp: ## create env file from .env.example
	cp .env.example .env

initialize: env-cp build up makemigrations migrate createsuperuser
	printf "user: admin\npassword: admin\nhref: http://localhost:8080/admin\n"

logs:  ## show logs for app container
	${DC} logs -f app
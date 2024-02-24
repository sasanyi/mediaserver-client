ROOT := $(shell pwd)
IMAGE_NAME := mediaserver

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/\(.*\):.*##[ \t]*/    \1 ## /' | column -t -s '##'
	@echo

## _________________________________________
## DOCKER COMMANDS:
docker_compose = docker-compose --file ./configs/docker/docker-compose.yml
docker_compose_run = $(call docker_compose) --project-name $(IMAGE_NAME)-1 run --user=user --rm $(IMAGE_NAME)

network-create: ## Create external unique network for project
	docker network create $(IMAGE_NAME)-network

network-remove: ## Remove the project-specific network from the project
	docker network remove $(IMAGE_NAME)-network

# volume-recreate: ## Remove and create volumes
# 	- make volume-remove
# 	- make volume-create

# volume-create: ## Create volumes for docker-compose
# 	docker volume create --driver local --opt type=None --opt device=$(ROOT) --opt o=bind app_data

# volume-remove: ## Remove volumes of docker-compose
# 	docker volume rm app_data

image-rebuild: ## Remove and build again the project image
	- make image-remove
	- make image-build

image-remove: ## Remove the image
	docker rmi $(shell docker images | grep '$(IMAGE_NAME)' | awk '{print $$1}')

dependencies-up: ## Start dependencies of project up
	$(call docker_compose) up --detach --force-recreate $(IMAGE_NAME)-mysql

image-build: ## Build the app image
	$(call docker_compose) build $(IMAGE_NAME)

bash: ## Run container with bash
	$(call docker_compose_run) bash

## _________________________________________
## PROJECT COMMANDS:

venv: ## Make virtualenv under the docker_image
	$(call docker_compose_run) python3 -m venv .venv

venv-recreate: ## Remove and make again the virtualenv of project
	- make venv-remove
	- make venv

venv-remove: ## Remove virtualenv from the project
	$(call docker_compose_run) rm -rf .venv

install: ## Install project specific packages from requirements.txt
	$(call docker_compose_run) .venv/bin/pip install -r requirements.txt

## _________________________________________
## DEV COMMANDS:

test: ## Run all tests
	$(call docker_compose_run) pytest -svv tests

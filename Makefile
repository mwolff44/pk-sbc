PROJECT_NAME=pyfreebilling
export COMPOSE_FILE=local.yml

# source : https://github.com/wodby/docker4python/blob/master/docker.mk

.PHONY: up down stop prune ps shell logs

default: up

## help	:	Print commands help.
help : Makefile
	@sed -n 's/^##//p' $<

## up	:	Start up containers.
up:
	@echo "Starting up containers for for $(PROJECT_NAME)..."
	# @see:https://github.com/docker/compose/issues/6464
	#docker-compose pull
	docker-compose build
	docker-compose up -d --remove-orphans

## build	:	Build python image.
build:
	@echo "Building python image for for $(PROJECT_NAME)..."
	docker-compose build

buildev:
	@sed -i.bak s/DJANGO_SETTINGS_MODULE=config.settings.production/DJANGO_SETTINGS_MODULE=config.settings.local/g .env
	@sed -i.bak s/DJANGO_DEBUG=False/DJANGO_DEBUG=True/g .env
	@docker-compose -f local.yml up --build

buildprod:
	@sed -i.bak s/DJANGO_SETTINGS_MODULE=config.settings.local/DJANGO_SETTINGS_MODULE=config.settings.production/g .env
	@sed -i.bak s/DJANGO_DEBUG=True/DJANGO_DEBUG=False/g .env
	@docker-compose -f production.yml up --build

## down	:	Stop containers.
down: stop

## start	:	Start containers without updating.
start:
	@echo "Starting containers for $(PROJECT_NAME) from where you left off..."
	@docker-compose start

## stop	:	Stop containers.
stop:
	@echo "Stopping containers for $(PROJECT_NAME)..."
	@docker-compose stop

## prune	:	Remove containers and their volumes.
##		You can optionally pass an argument with the service name to prune single container
##		prune django	: Prune `django` container and remove its volumes.
prune:
	@echo "Removing containers for $(PROJECT_NAME)..."
	@docker-compose down -v $(filter-out $@,$(MAKECMDGOALS))

## ps	:	List running containers.
ps:
	@docker ps --filter name='$(PROJECT_NAME)*'

## manage   :	Executes `manage.ph` command.
##		To use "--flag" arguments include them in quotation marks.
##		For example: make manage "foo --type=cron"
.PHONY: manage
manage:
	docker-compose run --rm django python manage.py $(filter-out $@,$(MAKECMDGOALS))

## shell	:	Access `python` container via shell.
shell:
	docker exec -ti -e COLUMNS=$(shell tput cols) -e LINES=$(shell tput lines) $(shell docker ps --filter name='$(PROJECT_NAME)_django' --format "{{ .ID }}") sh

## logs	:	View containers logs.
##		You can optionally pass an argument with the service name to limit logs
##		logs python	: View `python` container logs.
##		logs nginx python	: View `nginx` and `python` containers logs.
logs:
	@docker-compose logs -f $(filter-out $@,$(MAKECMDGOALS))

# https://stackoverflow.com/a/6273809/1826109
%:
	@:
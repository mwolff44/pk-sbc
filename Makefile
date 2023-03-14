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

## logs	:	View containers logs.
##		You can optionally pass an argument with the service name to limit logs
##		logs python	: View `python` container logs.
##		logs nginx python	: View `nginx` and `python` containers logs.
logs:
	@docker-compose logs -f $(filter-out $@,$(MAKECMDGOALS))

# https://stackoverflow.com/a/6273809/1826109
%:
	@:
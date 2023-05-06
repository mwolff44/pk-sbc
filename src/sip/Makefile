include .envrc

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

.PHONY: confirm
confirm:
	@echo -n 'Are you sure? [y/N] ' && read ans && [ $${ans:-N} = y ]

# ==================================================================================== #
# DEVELOPMENT
# ==================================================================================== #

DOCKER_COMPOSE := docker-compose -f docker-compose.yaml

## check/proxy: check the kamailio file
.PHONY: check/proxy
check/proxy:
	docker build -f Dockerfile.test -t pks-proxy-test .
	docker run --name pks-proxy-test pks-proxy-test
	docker rm pks-proxy-test

## check/removecontainer: remove the remaining container used for checking the kamailio file
.PHONY: check/removecontainer
check/removecontainer:
	docker rm pks-proxy-test

## build/proxy: build the proxy application
.PHONY: build/proxy
build/proxy:
	@$(DOCKER_COMPOSE) build

## run/proxy: run the proxy application
.PHONY: run/proxy
run/proxy:
	@$(DOCKER_COMPOSE) up -d

## stop/proxy: stop the proxy application
.PHONY: stop/proxy
stop/proxy:
	@$(DOCKER_COMPOSE) down

## restart/proxy: restart the proxy application
.PHONY: restart/proxy
restart/proxy:
	@$(DOCKER_COMPOSE) stop
	@$(DOCKER_COMPOSE) up -d

## logs/proxy: view logs of the proxy application
.PHONY: logs/proxy
logs/proxy:
	@$(DOCKER_COMPOSE) logs --tail=100 -f

## ps/proxy: view processes of the proxy application
.PHONY: ps/proxy
ps/proxy:
	@$(DOCKER_COMPOSE) ps

# ==================================================================================== #
# PRODUCTION
# ==================================================================================== #

production_host_ip = "your.ip.address"
production_host_username = "root"
production_kamailio_version = "56"

## production/connect: connect to the production server
.PHONY: production/connect
production/connect:
	ssh ${production_host_username}@${production_host_ip}


## production/install/dependencies: install the proxy dependencies to production
.PHONY: production/install/dependencies
production/install/dependencies:
	ssh -t ${production_host_username}@${production_host_ip} '\
		rm -rf /var/lib/apt/lists/* \
		&& apt-get update \
		&& apt-get install --assume-yes gnupg wget \
		&& echo "deb http://deb.kamailio.org/kamailio${production_kamailio_version} bullseye main" > /etc/apt/sources.list.d/kamailio.list \
		&& wget -O- http://deb.kamailio.org/kamailiodebkey.gpg | apt-key add -
		&& apt-get update && apt-get install --assume-yes \
	          kamailio \
	          kamailio-extra-modules \
	          kamailio-json-modules \
	          kamailio-systemd-modules \
	          kamailio-utils-modules \
	          kamailio-xml-modules \
		&& sudo systemctl enable kamailio \
	'


## production/deploy/proxy: deploy the proxy to production
.PHONY: production/deploy/proxy
production/deploy/proxy:
	rsync -P ./src/kamailio.cfg ${production_host_username}@${production_host_ip}:~
	ssh -t ${production_host_username}@${production_host_ip} '\
		sudo mv ~/kamailio.cfg /etc/kamailio/ \
        	&& sudo  mv ~/db /db \
		&& sudo systemctl restart kamailio \
	'

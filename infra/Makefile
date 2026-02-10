# Copyright: (c) 2007-2024 (see the AUTHORS file)
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
# SPDX-License-Identifier: AGPL-3.0-or-later

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

DOCKER_COMPOSE := docker compose -f docker-compose.yml --env-file /srv/pks/.env

## check/proxy: check the kamailio file
.PHONY: check/proxy
check/proxy:
	docker build -f Dockerfile.test -t pks-proxy-test .
	docker run --name pks-proxy-test pks-proxy-test
	docker rm pks-proxy-test

## build/proxy-mysql: build the MySQL kamailio image
.PHONY: build/proxy-mysql
build/proxy-mysql:
	docker build -f Dockerfile.mysql -t pks-proxy-mysql .
	docker run --name pks-proxy-mysql pks-proxy-mysql
	docker rm pks-proxy-mysql

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

## run/sipproxy: run the sip proxy
.PHONY: run/sipproxy
run/sipproxy:
	@$(DOCKER_COMPOSE) up -d pks-sip

## stop/sipproxy: stop the sip proxy
.PHONY: stop/sipproxy
stop/sipproxy:
	@$(DOCKER_COMPOSE) stop pks-sip

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

# ==================================================================================== #
# HELPERS
# ==================================================================================== #

## help: print this help message
.PHONY: help
help:
	@echo 'Usage:'
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'


# ==================================================================================== #
# DOCKER FOR DEV
# ==================================================================================== #
DB_DSN = postgres://postgres:password@pks-postgres/pks-DB?sslmode=disable

## docker/start/postgres: start the postgres container
.PHONY: docker/start/postgres
docker/start/postgres:
	docker run --rm -d \
		--name pks-postgres \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=pks-DB \
		-v ${HOME}/dev-postgres/data/:/var/lib/postgresql/data \
		-p 5432:5432 \
		postgres

## docker/bash/postgres: connect to the postgres container - use psql -h localhost -U postgres
.PHONY: docker/bash/postgres
docker/bash/postgres:
	docker exec -it pks-postgres bash

## docker/stop/postgres: stop the postgres container
.PHONY: docker/stop/postgres
docker/stop/postgres:
	docker stop pks-postgres

## docker/build/admin : build the pks-admin image
.PHONY: docker/build/admin
docker/build/admin:
	docker build -t pks-admin .

## docker/stop/admin : stop the pks-admin container
.PHONY: docker/stop/admin
docker/stop/admin:
	docker stop pks-admin

## docker/stop/all : stop all pks containers
.PHONY: docker/stop/all
docker/stop/all:
	docker/stop/admin \
	docker/stop/postgres

# ==================================================================================== #
# QUALITY CONTROL
# ==================================================================================== #

## tidy: format code and tidy modfile
.PHONY: tidy
tidy:
	go fmt ./...
	go mod tidy -v

## audit: run quality control checks
.PHONY: audit
audit:
	go vet ./...
	go run honnef.co/go/tools/cmd/staticcheck@latest -checks=all,-ST1000,-U1000 ./...
	go test -race -vet=off ./...
	go mod verify


# ==================================================================================== #
# BUILD
# ==================================================================================== #

## build: build the cmd/web application
.PHONY: build
build:
	go mod verify
	go build -ldflags='-s' -o=./bin/pks-admin ./main.go
	GOOS=linux GOARCH=amd64 go build -ldflags='-s' -o=./bin/linux_amd64/pks-admin ./main.go

## run: run the main.py application
.PHONY: run
run:
	go run github.com/cosmtrek/air@v1.40.4 --c="./air.toml"

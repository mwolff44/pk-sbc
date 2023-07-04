# Quick start

## First steps

    1. Check prerequisites.
    2. Download the PKS CLI and launch it.
    3. Try PKS.

## Prerequisites

Use the following steps to install P-KISS-SBC : 

1. Install docker and docker-compose
2. create 2 folders in /srv redis and db
3. download the ...

## Requirements

P-KISS-SBC uses Docker containers to run and supports all infrastructures that support containers.
Automated deployment uses docker compose, but kubernetes will be supported in the near future.
To deploy P-KISS-SBC, docker and docker compose must be installed.

!!! Tip "HowTo install ?"

    To install docker and docker compose on debian, follow this guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

## Step 1

2 folders must be created to host the P-KISS-SBC data: 

```
mkdir /src/redis /srv/db
```

## Step 2

Download the PKS script and run it

## Optional step

The *local* logging driver is recommended as it performs log-rotation by default, and uses a more efficient file format.
To configure the Docker daemon to default to a specific logging driver, set the value of log-driver to the name of the logging driver in the daemon.json /etc/docker/daemon.json

```
{
“log-driver”: “local”
}
```

Restart Docker for the changes to take effect

```
sudo systemctl restart docker.service
```

And to check

```
docker info --format '{{.LoggingDriver}}'
```

## Next steps
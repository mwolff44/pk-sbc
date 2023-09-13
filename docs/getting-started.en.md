# Quick start

## First steps

    1. Check prerequisites.
    2. Download the PKS CLI and launch it.
    3. Try PKS.

## Prerequisites

Use the following steps to install P-KISS-SBC :

1. Install docker, docker-compose and git
2. create folders in /srv for P-KISS-SBC datas
3. download the PKS code

## Requirements

P-KISS-SBC uses Docker containers to run and supports all infrastructures that support containers.
Automated deployment uses docker compose, but kubernetes will be supported in the near future.
To deploy P-KISS-SBC, docker and docker compose must be installed.

!!! Tip "HowTo install ?"

    To install docker and docker compose on debian, follow this guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

To download the PKS code, you need to have installed git and make commands. On debian/ubuntu :

```bash
apt install git make
```

## Installation

2 folders must be created to host the P-KISS-SBC data: 

```bash
mkdir /src/pks/redis /srv/pks/db
```

and download the PKS script and run it :

```bash
cd /usr/src
git clone https://gitlab.com/mwolff44/pyfreebilling
ln -s /usr/src/pyfreebilling/src/pks /usr/local/bin/pks
```

## Optional step

The *local* logging driver is recommended as it performs log-rotation by default, and uses a more efficient file format.
To configure the Docker daemon to default to a specific logging driver, set the value of log-driver to the name of the logging driver in the daemon.json /etc/docker/daemon.json

```bash
{
“log-driver”: “local”
}
```

Restart Docker for the changes to take effect

```bash
sudo systemctl restart docker.service
```

And to check

```bash
docker info --format '{{.LoggingDriver}}'
```

## Setup

### Initial configuration

create file in directory /srv/pks

```bash
touch .env
```

And add values corresponding to your installation. This is an example : 

```text
# Public IP of my VM
PUBLIC_IP=1.1.1.1
LISTEN_ADVERTISE=1.1.1.1:5060

# Private IP of my VM
LOCAL_IP=192.168.0.1

# RTP ports range
PORT_MIN=16000
PORT_MAX=18000

ENVIRONMENT=prod
RTPENGINE_URL=127.0.0.1
BIND_HTTP_IP=127.0.0.1
REDIS_URL=127.0.0.1

# Disable gateway probing
NOT_PROBING=true
```

### Quick configuration

#### Add a SIP Provider

To add a SIP Provider, use the commandline PKS to declare the IP/PORT of the provider gateway and add a default route to route all calls coming from IPBX to this SIP Provider.

```bash
pks admin add provider
```

#### Add an IPBX

To add an IPBX, use the commandline PKS to declare the IP/PORT of the IPBX and add DIDs to route incoming calls to thid IPBX.

```bash
pks admin add ipbx

pks admin add did
```

## Manage P-KISS-SBC

To lauch P-KISS-SBC and manage it, you will use the simple but effective commandline PKS.

```bash
# To start
pks start

# To stop
pks stop

# To reload the configuration
pks reload

# To see containers status
pks status

# To see the logs
pks debug
```

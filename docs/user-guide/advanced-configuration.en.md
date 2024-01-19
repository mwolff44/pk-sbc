# Advanced Configuration

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

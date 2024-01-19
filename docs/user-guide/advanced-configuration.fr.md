# Configuration Avancée

## Prérequis

Suivez les étapes suivantes pour installer P-KISS-SBC : 

1. Installer docker, docker-compose et git
2. créer les dossiers dans /srv pour les données de P-KISS-SBC
3. télécharger le code PKS

Pour télécharger le code PKS, vous devez avoir installé les commandes git et make. Sur debian/ubuntu : 

```bash
apt install git make
```

## Installation

2 dossiers doivent être créés pour héberger les données P-KISS-SBC : 

```bash
mkdir /src/pks/redis /srv/pks/db
```

et télécharger le script PKS et l'exécuter :

```bash
cd /usr/src
git clone https://gitlab.com/mwolff44/pyfreebilling
ln -s /usr/src/pyfreebilling/src/pks /usr/local/bin/pks
```

## Setup

### Configuration initiale

créer un fichier dans le répertoire /srv/pks

```bash
touch .env
```

Et ajoutez les valeurs correspondant à votre installation. Voici un exemple : 

```bash
# IP publique de ma VM
PUBLIC_IP=1.1.1.1
LISTEN_ADVERTISE=1.1.1.1:5060

# IP privée de ma VM
LOCAL_IP=192.168.0.1

# Gamme de ports RTP
PORT_MIN=16000
PORT_MAX=18000

ENVIRONMENT=prod
RTPENGINE_URL=127.0.0.1
BIND_HTTP_IP=127.0.0.1
REDIS_URL=127.0.0.1

# Désactiver le sondage de la passerelle
NOT_PROBING=true
```

### Configuration rapide

#### Ajouter un fournisseur SIP

Pour ajouter un fournisseur SIP, utilisez la ligne de commande PKS pour déclarer l'IP/PORT de la passerelle du fournisseur et ajoutez une route par défaut pour acheminer tous les appels provenant de l'IPBX vers ce fournisseur SIP.

```bash
pks admin add provider
```

#### Ajouter un IPBX

Pour ajouter un IPBX, utilisez la ligne de commande PKS pour déclarer l'IP/PORT de l'IPBX et ajouter des SDAs pour router les appels entrants vers cet IPBX.

```bash
pks admin add ipbx

pks admin add did
```

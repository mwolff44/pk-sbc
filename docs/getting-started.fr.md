# Démarrage rapide

## Premiers pas

    1. Vérifier les prérequis.
    2. Téléchargez la CLI PKS et lancez-la.
    3. Essayez PKS.

## Prérequis

Suivez les étapes suivantes pour installer P-KISS-SBC : 

1. Installer docker, docker-compose et git
2. créer 2 dossiers dans /srv redis et db
3. télécharger le code PKS

## Exigences

P-KISS-SBC utilise des conteneurs Docker pour fonctionner et prend en charge toutes les infrastructures qui prennent en charge les conteneurs.
Le déploiement automatisé utilise docker compose, mais kubernetes sera pris en charge dans un avenir proche.
Pour déployer P-KISS-SBC, docker et docker compose doivent être installés.

!!! Tip "Comment installer ?"

    Pour installer docker et docker compose sur debian, suivez ce guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

Pour télécharger le code PKS, vous devez avoir installé les commandes git et make. Sur debian/ubuntu : 

```
apt install git make
```

## Installation

2 dossiers doivent être créés pour héberger les données P-KISS-SBC : 

```
mkdir /src/redis /srv/db
```

et télécharger le script PKS et l'exécuter :

```
cd /usr/src
git clone https://gitlab.com/mwolff44/pyfreebilling
ln -s /usr/src/pyfreebilling/src/pks /usr/local/bin/pks
```

## Étape optionnelle

Le pilote de journalisation *local* est recommandé car il effectue la rotation des journaux par défaut et utilise un format de fichier plus efficace.
Pour configurer le daemon Docker pour qu'il utilise par défaut un pilote de journalisation spécifique, définissez la valeur de log-driver avec le nom du pilote de journalisation dans le fichier daemon.json /etc/docker/daemon.json

```
{
"log-driver" : "local"
}
```

Redémarrez Docker pour que les changements soient pris en compte

```
sudo systemctl restart docker.service
```

Et pour vérifier

```
docker info --format '{{.LoggingDriver}}'
```

## Setup

### Configuration initiale

créer un fichier dans le répertoire /srv

```
touch .env
```

Et ajoutez les valeurs correspondant à votre installation. Voici un exemple : 

```
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

```
pks admin add provider
```

#### Ajouter un IPBX

Pour ajouter un IPBX, utilisez la ligne de commande PKS pour déclarer l'IP/PORT de l'IPBX et ajouter des SDAs pour router les appels entrants vers cet IPBX.

```
pks admin add ipbx

pks admin add did
```

## Gérer P-KISS-SBC

Pour lancer P-KISS-SBC et le gérer, vous utiliserez la ligne de commande simple mais efficace PKS.

```
# Pour démarrer
pks start

# Pour arrêter
pks stop

# Pour recharger la configuration
pks reload

# Pour voir l'état des conteneurs
pks status

# Pour voir les logs
pks debug
```

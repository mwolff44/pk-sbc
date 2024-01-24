# Prérequis

P-KISS-SBC utilise des __conteneurs Docker__ pour fonctionner et prend en charge toutes les infrastructures qui prennent en charge les conteneurs.

Le déploiement automatisé utilise docker compose, mais kubernetes sera pris en charge dans un avenir proche.

Ainsi, la seule chose dont vous avez besoin pour installer P-KISS-SBC est un serveur avec Docker et docker compose installés.

!!! Tip "Comment installer Docker ?"

    Pour installer docker et docker compose sur debian, suivez ce guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

## Systèmes d'exploitation supportés

Le script d'installation automatique en une étape peut être utilisé avec un nombre limité de systèmes d'exploitation.

Les systèmes d'exploitation suivants sont __officiellement__ pris en charge :

| Distribution | Release          | Architecture        |
| ------------ | ---------------- | ------------------- |
| DietPi   | v8.xx | x86_64 |
| Ubuntu | 22.04 | x86_64 |
| Debian | 12 | x86_64 |

!!! Note "Déployer sur un autre OS"
    Il est tout à fait possible de déployer PKS sur un autre OS. Les pré-requis devront-être installés manuellement !

## Dimensionnement VM

Le serveur doit être équipé de __processeur x86_64__ et prendre en charge SSE 4.2 ou des instructions NEON équivalentes.

Nous recommandons d'utiliser un __minimum de 2 vcpu et 2GB de RAM__, mais les exigences dépendront de votre trafic VoIP en termes d'appels simultanés et de nouveaux appels par seconde.

!!! warning "Ressources dédiées"
    Il est important de ne pas pas oublier que PKS va traiter des flux pseudo __temps réel__ (VoIP). Il est donc essentiel de __dédier__ les __ressources matériels__ (CPU et RAM) à PKS. Il faut éviter les sur-allocations qui auront pour conséquences une qualité audio dégradée.
    Même si les écritures ne sont pas critiques, PKS n'utilisant pas de base de données, il faut s'assurer que les accès disque soient assez rapide.

## Réseau

### Qualité

La VoIP nécessite un __réseau__ bien dimensionné et de __bonne qualité__. Les __flux média__ doivent-être __priorisé__ (par défaut le `TOS 184` est défini).

!!! tip ""
    La __réservation de bande passante__ est aussi intéressante à mettre en oeuvre au sein de vos équipements réseaux.

### Adressage IP

PKS se déploie sur une VM avec __une seule adresse IP privée__. Une __adresse IP publique__ avec les ports renvoyés sur cette VM est __nécessaire__ (voir la liste ci-dessous).

!!! tip "2 adresses IP publiques"
    Il est possible de disposer d'une addresse IP pour la signalisation différente de l'addresse IP publique du média.

### Ports réseaux

PKS utilise __2 ports réseau différents__ pour la __signalisation__ (UDP 5060 et UDP 5070) et une __plage de ports__ prédéfinis pour le __média__ (UDP 16000 à 18000).

Ces __paramètres__ peuvent-être __modifiés__ pour correspondre à vos besoins, notamment la plage de ports RTP afin de pouvoir gérer plus d'appels concurrents.

!!! note "Administration web"
    De plus, si vous utilisez PKS-Admin, l'interface Web d'administration, le port TCP 443 devra être ouvert.

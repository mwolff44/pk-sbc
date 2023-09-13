# Cas d'utilisation

## Sécurisation d'un système de téléphonie

Ce premier cas d'usage est le plus simple : utiliser P-KISS-SBC entre le monde extérieur et l'IPBX afin de protéger celui-ci. Le schéma sera le suivant :

SIP Provider ==== P-KISS-SBC ===== IPBX

Un SBC embarque des fonctionnalités de sécurité plus évoluées et performantes qu'un IPBX qui doit-être considéré comme un serveur d'application. Un IPBX expose un grand nombre de services ce qui rend sa surface d'attaque importante. IL est aussi peu robuste aux attaques de type déni de services. P-KISS-SBC de part sa conception offre une surface d'attaque très faible, détecte et bloques les tentatives d'attaques avant qu'elles arrivent à l'IPBX et est très résilient par sa capacité à supporter un grand nombre de requêtes.

TODO : détailler les fonctionnalités de sécurité ainsi que la mise en oeuvre

## Fail over d'un IPBX principal à un secondaire

Une autre cas d'usage simple à mettre en oeuvre avec P-KISS-SBC est la haute disponibilité d'IPBX. 2 scénarios sont alors possibles. Tout d'abord le failover permettant d'envoyer les requêtes lors de la parter de l'IPBX principal à l'IPBX secondaire sans aucune action manuelle. Le ou les opérateurs télécoms ne voient aucun changement et n'ont aucune connaissance de l'infrastructure téléphonique interne.

Fonctionnement nominal :

SIP PROVIDER ==== P-KISS-SBC ==== IPBX principal
                             ---- IPBX secondaire

En cas de perte de l'IPBX prinvciapl, les flux sont redirrigés vers l'IPBX secondaire

SIP PROVIDER ==== P-KISS-SBC ---- IPBX principal
                             ==== IPBX secondaire

Le retour au fonctionnement nominal est automatique dès que P-KISS-SBC détecte le retour en bon état de fonctionnement de l'IPBX principal.

## Haute disponibilité d'un IPBX avec 2 ou plus instances

En plus du fail over, P-KISS-SBC supporte aussi la haute disponibilité ou l'IPBX fonctionne avec 2 ou plus instances actives simultannément. Dans ce cas, P-KISS-SBC route les requêtes équitablement entre les instances :

SIP PROVIDER ==== P-KISS-SBC ==50%== IPBX instance 1
                             ==50%== IPBX instance 2

## Répartition géographique d'IPBX avec connexion opérateur télécom centralisé

POur des raisons d'optimisation de flux, de disponibilité ou de répartition de charge, les instances de IPBX peuvent-être déployées sur des sites différents. P-KISS-SBC permet une connexion unique à un opérateur et de router silmplement les appels à l'instance souhaitée :

Appel à destination du site 1 :

SIP PROVIDER ==== P-KISS-SBC ==== IPBX 1
                             ---- IPBX 2

Appel à destination du site 2 :

SIP PROVIDER ==== P-KISS-SBC ---- IPBX 1
                             ==== IPBX 2

## Connexion d'un IPBX mutli-entités avec un opérateur télécom

Dans le cadre d'administrations ou de sites hébergeant plusieurs entreprises, il est courant d'utiliser un IPBX multi-tenant, c'est à dire hébergeant des entités séparées et hermétiques les unes vis à vis des autres. EN dehors d'une bidouille, il est impossible de connecter cet IPBX multi-tenant avec un opérateur télécom via un trunk unique. P-KISS-SBC perment de réaliser cela :

SIP PROVIDER ==== P-KISS-SBC ==tenant 1== IPBX tenant 1
                             ==tenant 2== IPBX tenant 2

## Raccordement d'un IPBX à plus d'un opérateur

Afin d'écononomiser sur les abonnements et communications téléphoniques, il peut-être souhaitable d'utiliser des opérateurs différents selon les destinations ou les numéros souhaités notamment dans le cadre international. P-KISS-SBC permet de connecter plusieurs opérateurs à un IPBX et de router les appels entrants à celui-ci quelque soit l'opérateur d'origine et de router les appels sortants sur l'iopérateur souhaité. Même s'il est possible de connecter plusieurs opérateurs directements sur un IPBX, il est par contre complexe de router les appels sur l'opérateur souhaité tout en intégrant une fonctionnalité de failover. P-KISS-SBC intègre une fonctionnalité permettant de tenter de router l'appel vers un opérateur de préférence et en cas d'échec de tenter d'aboutir l'appel sur un deuxième opérateur.

SIP PROVIDER 1
              ===== P-KISS-SBC ==== IPBX
SIP PROVIDER 2

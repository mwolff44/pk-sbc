# Prérequis

P-KISS-SBC utilise des __conteneurs Docker__ pour fonctionner et prend en charge toutes les infrastructures qui prennent en charge les conteneurs.

Le déploiement automatisé utilise docker compose, mais kubernetes sera pris en charge dans un avenir proche.

Ainsi, la seule chose dont vous avez besoin pour installer P-KISS-SBC est un serveur avec Docker et docker compose installés.

!!! Tip "Comment installer Docker ?"

    Pour installer docker et docker compose sur debian, suivez ce guide : [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)

Le serveur doit être équipé de __processeur x86_64__ et prendre en charge SSE 4.2 ou des instructions NEON équivalentes.

Nous recommandons d'utiliser un minimum de 2 vcpu et 2GB de RAM, mais les exigences dépendront de votre trafic VoIP en termes d'appels simultanés et de nouveaux appels par seconde.

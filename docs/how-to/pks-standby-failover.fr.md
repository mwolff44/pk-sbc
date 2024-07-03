<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# PKS Standby failover architecture

PKS peut-être déployé en mode actif passif, afin de permettre une reprise en cas d'incident majeur.
Dans cette configuration, les données seront synchronisées du serveur primaire vers le serveur secondaire. A noter que dans la configuration présentée dans cette page, la base secondaire n'est pas accessible en écriture.

## Pré-requis

Vous devez déployer 2 instances complètes de PKS en suivant le process standard.

## Mise en oeuvre

Les ports IP prévus pour la base de données primaire-secondaire sont, par exemple, les suivants :

* Primary DB: 10.0.3.10:5432
* Secondary DB: 10.0.3.11:5432

## Préparation du server primaire

!!! Warning

    La DB doit-être redémarrée !

Créer un compte spécial pour les flux de réplication primary-secondary :

    # 1. Entrer dans le container
    docker exec -it pks-db bash

    # 2. Se connecter à PostgreSQL
    psql -U postgres

    # 3. Créer le rôle utilisateur
    CREATE ROLE repuser WITH LOGIN REPLICATION CONNECTION LIMIT 5 PASSWORD '123456';
    # Username repuser; Maximum number of links: 5; Password: 123456

    # 4. Voir les rôles
    \du

                                       List of roles
     Role name |                         Attributes                         | Member of
    -----------+------------------------------------------------------------+-----------
     postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
     repuser   | Replication                                               +| {}
               | 5 connections                                              |

    # 5. Quitter
    \q
    exit

Modifier le fichier de configuration du primaire :

    # 1. Entrer dans le dossier du serveur primaire 
    cd /srv/pks/db

    # 2. Et ajouter la règle à la fin
    echo "host replication repuser 10.0.3.11/24 md5" >> pg_hba.conf

Modifier le fichier postgresql.conf , en trouvant les lignes suivantes, en décommentant et en modifiant ainsi:

    archive_mode = on				# Enable Archive Mode
    archive_command = '/bin/date'	# Set archiving behavior
    # The sum of the number of concurrent connections from the slave to the host
    max_wal_senders = 10			
    # Specifies that if the backup server needs to obtain log segment files for stream replication, pg_ The minimum size of past log file segments that can be retained in the wal directory	
    wal_keep_size = 16		
    # Specify a list of backup servers that support synchronous replication
    synchronous_standby_names = '*'

Pour plus de détails sur les paramètres, veuillez vous référer à : https://www.postgresql.org/docs/

Redémarrer le container primaire :

    #Using pg_ctl stop stops the database safely
    docker exec -it -u postgres pks-db pg_ctl stop
    docker start pks-db

## Configuration du serveur secondaire

Editer la configuration de docker compose :

    # Créer le dossier repl 
    mkdir /srv/pks/repl
    chmod 777 /srv/pks/repl

    # Stop pks
    pks stop

    # line 92 add :
    - pks-db-repl:/var/lib/postgresql/repl

    # line 180 add :
    pks-db-repl:
        driver: local
        driver_opts:
        type: 'none'
        o: 'bind'
        device: '/srv/pks/repl'

    # Et démarrer pks
    pks start

Synchronizer les donner

    # 1. Entrer dans le container
    docker exec -it -u postgres pks-db bash

    # 2. Sauvegardez les données de l'hôte dans le dossier repl. Saisissez ici le mot de passe défini ci-dessus : 123456
    pg_basebackup -R -D /var/lib/postgresql/repl -Fp -Xs -v -P -h 10.0.3.11 -p 5432 -U repuser

    pg_basebackup: initiating base backup, waiting for checkpoint to complete
    pg_basebackup: checkpoint completed
    pg_basebackup: write-ahead log start point: 0/2000028 on timeline 1
    pg_basebackup: starting background WAL receiver
    pg_basebackup: created temporary replication slot "pg_basebackup_154"
    24264/24264 kB (100%), 1/1 tablespace
    pg_basebackup: write-ahead log end point: 0/2000138
    pg_basebackup: waiting for background process to finish streaming ...
    pg_basebackup: syncing data to disk ...
    pg_basebackup: renaming backup_manifest.tmp to backup_manifest
    pg_basebackup: base backup completed

    # 3. Sortir du container après que la sauvegarde soit terminée
    exit

Reconstruire le container secondaire

Grâce à la sauvegarde initiale de l'étape précédente, vous pouvez maintenant reconstruire le conteneur secondaire en utilisant les données contenues dans /srv/pks/repl. Supprimez d'abord le répertoire db, puis remplacez le répertoire repl par db, qui est le répertoire de données de la base de données secondaire :

    # 1. Supprimer le container
    docker rm -f pks-db

    # 2. Supprimer le dossier de base et renommer repl en db
    cd /srv/pks/
    rm -rf db
    mv repl db
    cd /srv/pks/db

    # 3. Voir les informations de configuration
    # postgresql.auto.conf contiendra les informations nécessaires à la réplication
    cat postgresql.auto.conf

    primary_conninfo = 'user=repuser password=123456 channel_binding=prefer host=10.0.3.11 port=5432 sslmode=prefer sslcompression=0 ssl_min_protocol_version=TLSv1.2 gssencmode=prefer krbsrvname=postgres target_session_attrs=any'

Reconstruire le container secondaire:

    # Supprimer les paramètres ajouté plus haut dans le fichier du docker compose

    # Redémarrer le container DB
    pks start

## Visualiser les informations de réplication primaire-secondaire

    ps -aux | grep postgres

    Main library process:
    postgres: walsender repuser 172.18.0.1(52678) streaming 0/3000148
     Process from library:
    postgres: walreceiver streaming 0/3000148

Visualiser les informations de réplication

    # Entrer dans le container primaire et basculer en utilisateur postgres
    docker exec -it pks-db bash
    psql -U postgres

    -- Query replication information
    select * from pg_stat_replication;

    pid | usesysid | usename | application_name | client_addr | client_hostname...
    170	16384	repuser	walreceiver	172.18.0.1		52678	2021-09-29 05:57:30.471391+00...

## Gestion

Vous pouvez forcer les requêtes SIP sur l'un des 2 serveurs.

La base de données du serveur secondaire est uniquement en lecture seule, permettant un fonctionnement du SBC mais ne permettant pas d'effectuer de modification.

Si vous voulez forcer le trafic SIP sur un serveur, il suffit d'éteindre le container du proxy SIP : `docker start pks-sip`
<!---
# P-KISS-SBC documentation © 2007-2024 by Mathias WOLFF 
# is licensed under Attribution-NonCommercial-ShareAlike 4.0 International (see https://creativecommons.org/licenses/by-nc-sa/4.0/)
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
--->

# PKS Standby failover setup

PKS can be deployed in passive active mode, to enable recovery in the event of a major incident.
In this configuration, data will be synchronized from the primary server to the secondary server. Note that in the configuration presented on this page, the secondary database is not writable.

## Prerequisites

You need to deploy 2 complete instances of PKS following the standard process.

## Implementation

The planned IP ports of the primary-secondary DB are as follows as an example :

* Primary DB: 10.0.3.10:5432
* Secondary DB: 10.0.3.11:5432

## Primary server preparation

!!! Warning

    The DB must be started !

Create a special account for primary-secondary stream replication :

    # 1. Enter the container
    docker exec -it pks-db bash

    # 2. Connect to PostgreSQL
    psql -U postgres

    # 3. Create user rules
    CREATE ROLE repuser WITH LOGIN REPLICATION CONNECTION LIMIT 5 PASSWORD '123456';
    # Username repuser; Maximum number of links: 5; Password: 123456

    # 4. View rules
    \du

                                       List of roles
     Role name |                         Attributes                         | Member of
    -----------+------------------------------------------------------------+-----------
     postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
     repuser   | Replication                                               +| {}
               | 5 connections                                              |

    # 5. Exit
    \q
    exit

Modify the primary configuration file

    # 1. Enter the folder of the primary server
    cd /srv/pks/db

    # 2. Add rules at the end
    echo "host replication repuser 10.0.3.11/24 md5" >> pg_hba.conf

Modify the postgresql.conf configuration file, find the following lines, uncomment and modify the configuration:

    archive_mode = on				# Enable Archive Mode
    archive_command = '/bin/date'	# Set archiving behavior
    # The sum of the number of concurrent connections from the slave to the host
    max_wal_senders = 10			
    # Specifies that if the backup server needs to obtain log segment files for stream replication, pg_ The minimum size of past log file segments that can be retained in the wal directory	
    wal_keep_size = 16		
    # Specify a list of backup servers that support synchronous replication
    synchronous_standby_names = '*'

For more details of parameters, please refer to: https://www.postgresql.org/docs/

Restart the primary container

    #Using pg_ctl stop stops the database safely
    docker exec -it -u postgres pks-db pg_ctl stop
    docker start pks-db

## Secondary server configuration

Edit the docker compose configuration :

    # Create repl directory
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

    # And start pks
    pks start

Synchronize data

    # 1. Enter the container
    docker exec -it -u postgres pks-db bash

    # 2. Back up the host data to the repl folder. Here, enter the password set above: 123456
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

    # 3. Exit the container after the backup is completed
    exit

Rebuild the secondary container

Through the initial backup in the previous step, you can now rebuild the secondary container using the data in /srv/pks/repl. First delete the db directory, and then change the repl directory to db, which is the data directory of the secondary DB:

    # 1. Delete container
    docker rm -f pks-db

    # 2. Delete the original folder and rename repl to db
    cd /srv/pks/
    rm -rf db
    mv repl db
    cd /srv/pks/db

    # 3. View configuration information
    # postgresql.auto.conf will contain the information required for replication
    cat postgresql.auto.conf

    primary_conninfo = 'user=repuser password=123456 channel_binding=prefer host=10.0.3.11 port=5432 sslmode=prefer sslcompression=0 ssl_min_protocol_version=TLSv1.2 gssencmode=prefer krbsrvname=postgres target_session_attrs=any'

Rebuild the secondary container:

    # Remove the settings in docker compose file

    # Restart the DB container
    pks start

## View primary-secondary replication information

    ps -aux | grep postgres

    Main library process:
    postgres: walsender repuser 172.18.0.1(52678) streaming 0/3000148
     Process from library:
    postgres: walreceiver streaming 0/3000148

Verify primary-secondary configuration

    # Enter the primary container and switch to the postgres user
    docker exec -it pks-db bash
    psql -U postgres

    -- Query replication information
    select * from pg_stat_replication;

    pid | usesysid | usename | application_name | client_addr | client_hostname...
    170	16384	repuser	walreceiver	172.18.0.1		52678	2021-09-29 05:57:30.471391+00...

## How to manage

You can force SIP requests to one of the 2 servers.

The secondary server's database is read-only, allowing SBC operation but not modification.

If you want to force SIP traffic on one server, simply switch off the SIP proxy container: `docker start pks-sip`
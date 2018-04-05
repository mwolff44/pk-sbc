Installation
************

Table of contents
=================

* Introduction
* Prerequisites
* Sip server installation
* SBC installation
* Postgresql configuration
* Web server install
* PyFreeBilling installation
* Next step

Introduction
============

This howto is written for Debian 8 server.
You need 2 interfaces with 2 ip public addresses, one for customers side and the other one for provider side.

Prerequisites
=============

First, you need to install these packages

::

    apt-get install git-core build-essential autoconf automake libtool libtool-bin libncurses5 libncurses5-dev gawk libjpeg-dev zlib1g-dev pkg-config libssl-dev libpq-dev unixodbc-dev odbc-postgresql postgresql postgresql-client libpq-dev libxml2-dev libxslt-dev ntp ntpdate libapache2-mod-wsgi apache2 gcc python-setuptools python-pip libdbd-pg-perl libtext-csv-perl sqlite3 libsqlite3-dev libcurl4-openssl-dev libpcre3-dev libspeex-dev libspeexdsp-dev libldns-dev libedit-dev libmemcached-dev python-psycopg2 python-dev libgeoip-dev libffi-dev
    
Postgresql configuration
========================

* create user and database :

::

    su postgres

::

    createuser -P pyfreebilling --interactive
        Enter password for new role:
        Enter it again:
        Shall the new role be a superuser? (y/n) n
        Shall the new role be allowed to create databases? (y/n) y
        Shall the new role be allowed to create more new roles? (y/n) y

::

    createdb -O pyfreebilling -E UTF8 pyfreebilling
    exit


Sip server installation
=======================

* First, install dependencies, edit sources.list :

::

    nano /etc/apt/sources.list

* Add this lines at the end of the files :

::

    # Kamailio 4.4 Release
    deb http://deb.kamailio.org/kamailio44 jessie main
    deb-src http://deb.kamailio.org/kamailio44 jessie main

* Add the repo GPG key, update the packages list, and install packages :

::

    wget -O- http://deb.kamailio.org/kamailiodebkey.gpg | sudo apt-key add -
    apt-get update
    apt-get install libpq5 libpq-dev
    apt-get install kamailio kamailio-tls-modules kamailio-postgres-modules kamailio-outbound-modules kamailio-extra-modules kamailio-xml-modules


* After finishing the installation, you have to edit  /etc/default/kamailio file:

::

    #
        # Kamailio startup options
        #

        # Set to yes to enable kamailio, once configured properly.
        RUN_KAMAILIO=yes

        # User to run as
        USER=kamailio

        # Group to run as
        GROUP=kamailio

        # Amount of shared and private memory to allocate
        # for the running Kamailio server (in Mb)
        #SHM_MEMORY=64
        #PKG_MEMORY=8

        # Config file
        CFGFILE=/etc/kamailio/kamailio.cfg

        # Enable the server to leave a core file when it crashes.
        # Set this to 'yes' to enable Kamailio to leave a core file when it crashes
        # or 'no' to disable this feature. This option is case sensitive and only
        # accepts 'yes' and 'no' and only in lowercase letters.
        # On some systems it is necessary to specify a directory for the core files
        # to get a dump. Look into the kamailio init file for an example configuration.
        DUMP_CORE=yes

* Configration files are located in /etc/kamailio/ folder.

The /etc/kamailio/kamctlrc is the configuration file for kamctl and kamdbctl tools. You need to edit it and set the SIP_DOMAIN to your SIP service domain (or IP address if you don't have a DNS hostname associated with your SIP service).

Set also the DBENGINE to be PGSQL and adjust other setting as you want. Very important are the passwords to connect to PostgreSSQL server, respectively DBRWPW and DBROPW. By default, their values are kamailiorw and kamailioro. You should change them before executing kamdbctl create (step detailed the section Create Database).

::

    sed "/^[# ]*SIP_DOMAIN/cSIP_DOMAIN=sip.<DOMAIN>.net" -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBENGINE/cDBENGINE=PGSQL' -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBHOST/cDBHOST=localhost' -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBNAME/cDBNAME=kamailiopyfb' -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBRWUSER/cDBRWUSER=kamailio' -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBRWPW/cDBRWPW="kamailio"' -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBROUSER/cDBROUSER=kamailioro' -i /etc/kamailio/kamctlrc
    sed '/^[#]*DBROPW/cDBROPW=kamailioro' -i /etc/kamailio/kamctlrc
    sed '/^[# ]*DBROOTUSER/cDBROOTUSER="pyfreebilling" ' -i /etc/kamailio/kamctlrc


* Create DB :
  Install Kamailio DB with db name kamailiopyfb (do not install extra tables) and drop these tables : usr_preferences, subscriber, address, dbaliases and dialplan.

To create the database structure needed by Kamailio, run:

::

    echo *:*:*:pyfreebilling:mypasswd > /root/.pgpass
    # Change **mypasswd** by  kamailiorw db password
    chmod 600 /root/.pgpass
    kamdbctl create

The database name created in PostgreSQL is kamailio. Two access users to PostgreSQL server were created:

* kamailio - (with password set by DBRWPW in kamctlrc) - user which has full access rights to kamailio database
* kamailioro - (with password set by DBROPW in kamctlrc) - user which has read-only access rights to kamailio database


* Start / stop kamailio :

If the default startup system is systemd, then kamailio can be managed via systemctl:

::

    systemctl start kamailio
    systemctl stop kamailio

First you may also need to edit /etc/default/kamailio and adjust the setting for kamailio startup script, in particular the one that enables kamailio to start.


* Check if it is ok :

::

    lsof -i :5060

* Add crontab :

::

    */10 * * * * /usr/sbin/kamcmd dialplan.reload>> /var/log/cron.log 2>&1
    */10 * * * * /usr/sbin/kamcmd dispatcher.reload>> /var/log/cron.log 2>&1
    */10 * * * * /usr/sbin/kamcmd permissions.addressReload>> /var/log/cron.log 2>&1




SBC installation
=======================

* AUTOMATIC INSTALL (from package) :

::

    wget -O - https://files.freeswitch.org/repo/deb/debian/freeswitch_archive_g0.pub | apt-key add -

        echo "deb http://files.freeswitch.org/repo/deb/freeswitch-1.6/ jessie main" > /etc/apt/sources.list.d/freeswitch.list

        # you may want to populate /etc/freeswitch at this point.
        # if /etc/freeswitch does not exist, the standard vanilla configuration is deployed
        apt-get update && apt-get install -y freeswitch-meta-bare freeswitch-mod-commands freeswitch-meta-codecs freeswitch-mod-console freeswitch-mod-logfile freeswitch-conf-vanilla freeswitch-mod-lua freeswitch-mod-cdr-csv freeswitch-mod-event-socket freeswitch-mod-sofia freeswitch-mod-sofia-dbg freeswitch-mod-loopback freeswitch-mod-db freeswitch-mod-dptools freeswitch-mod-hash freeswitch-mod-esl freeswitch-mod-dialplan-xml freeswitch-dbg freeswitch-mod-directory freeswitch-mod-nibblebill
        apt-get install -f odbc-postgresql unixodbc-bin unixodbc-dev libdbd-pg-perl libtext-csv-perl

* If you do not want to use snmp, comment the corresponding line in modules.conf.xml.


ODBC configuration
========================


* set odbc parameters; you need to create and edit /etc/odbc.ini file. Do not forget to specify your postgres password !

::

    [freeswitch]
    Driver = PostgreSQL
    Description = Connection to POSTGRESQL
    Servername = 127.0.0.1
    Port = 5432
    Protocol = 6.4
    FetchBufferSize = 99
    Username = pyfreebilling
    Password =
    Database = pyfreebilling
    ReadOnly = no
    Debug = 0
    CommLog = 0

* edit /etc/odbcinst.ini (delete all entries and add these ones)

::

    [PostgreSQL]
    Description     = PostgreSQL ODBC driver (Unicode version)
    Driver          = /usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so
    Setup           = /usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
    Debug           = 0
    CommLog         = 0
    UsageCount      = 0
    Threading       = 0
    MaxLongVarcharSize = 65536

Web server install
==================


* securing apache

::

    sudo a2enmod ssl
    sudo make-ssl-cert /usr/share/ssl-cert/ssleay.cnf /etc/ssl/private/localhost.pem (or use others methods or certificats)

* install python virtualenv

::

        pip install virtualenv
        cd /usr/local
        virtualenv venv --no-site-packages
        chown -R myuser:mysuser venv (replace myuser by your current user, perhaps root - better other one)

* activate it :

::

        source venv/bin/activate
        cd venv

* install CPAN :

   * install all dependent packages for CPAN

   ::

                apt-get install build-essential

   * invoke the cpan command as a normal user :

   ::

      $cpan
      But once you hit on enter for “cpan” to execute, you be asked of
      some few questions. To make it simple for yourself, answer “no”
      for the first question so that the latter ones will be done for
      you automatically.

      -> ANSWER YES


   * Once the above is done, you will be present with the cpan prompt.
      now enter the commands below

   ::

      cpan prompt> make install
      cpan prompt> install Bundle::CPAN


   * Now all is set and you can install any perl module you want.
      examples of what installed below

   ::

      cpan prompt>  install Carp
      cpan prompt>  install Filter::Simple
      cpan prompt>  install Config::Vars
      cpan prompt>  exit


Pyfreebilling installation
==========================

* download pyfreebilling sources :

::

        cd /usr/local/venv
        git clone https://github.com/mwolff44/pyfreebilling.git -b v2.0
        chown -R www-data:www-data pyfreebilling
        cd pyfreebilling

* create a new file in pyfreebilling directory called local.py (**delete the existing one**)

::

    nano /usr/local/venv/pyfreebilling/config/settings/local.py

* edit this new file, and put yours specific values

::

        # -*- coding: utf-8 -*-
        from .base import *

        #  ######### DEBUG CONFIGURATION
        DEBUG = False
        #  ######### END DEBUG CONFIGURATION

        #  ######### MANAGER CONFIGURATION
        ADMINS = (
            # ('Your Name', 'your_email@example.com'),
        )

        MANAGERS = ADMINS
        #  ######### END MANAGER CONFIGURATION

        #  ######### DATABASE CONFIGURATION
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'pyfreebilling',
                'USER': 'pyfreebilling',
                'PASSWORD': 'password',
                'HOST': '127.0.0.1',
                'PORT': '',                      # Set to empty string for default.
            }
        }
        #  ######### END DATABASE CONFIGURATION

        #  ######### HOST CONFIGURATION
        #  Add your IP and domain
        ALLOWED_HOSTS = ['*']
        #  ######### END HOST CONFIGURATION

        #  ######### SECRET CONFIGURATION
        # Note: very important - put your key for security - any string
        SECRET_KEY = 'securitykeymustbechanged'
        #  ######### END SECRET CONFIGURATION

        #  ######### COUNTRY SPECIFIC
        TIME_ZONE = 'Europe/Paris'
        # LANGUAGE_CODE = 'it' # uncomment do change webinterface language
        #  ######### END COUNTRY SPECIFIC

        #  ######### SPECIFIC SETTINGS

        OPENEXCHANGERATES_APP_ID = "Your API Key"

        #-- Nb days of CDR to show
        PFB_NB_ADMIN_CDR = 30
        PFB_NB_CUST_CDR = 30

        #  ######### END SPECIFIC SETTINGS

        #  ######### EMAIL CONFIGURATION
        # EMAIL SETUP
        TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
        TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
        TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = ''
        EMAIL_PORT = 587
        EMAIL_HOST_USER = ''
        EMAIL_HOST_PASSWORD = ''
        #EMAIL_USE_TLS = True
        EMAIL_USE_SSL = True
        EMAIL_SIGNATURE = ''
        #  ######### END EMAIL CONFIGURATION

* and now, enter the following commands without sudo (IMPORTANT). At the step "syncdb", you will fave a prompt asking you to enter a username and a password. They are very important, as thez are the admin one !

::

        pip install -r requirements/prod.txt
        python manage.py migrate
        python manage.py createsuperuser
        - (IMPORTANT : enter your username and password) --

        python manage.py loaddata 0001_initial_SipProfile.json
        python manage.py loaddata 0001_initial_ReccurentTasks.json
        python manage.py collectstatic (answer 'yes')


* copy some config files :

::

        mkdir /usr/share/freeswitch/scripts
        cd /usr/local/venv/pyfreebilling/install/resources/fs/config
        cp -av conf/autoload_configs/* /etc/freeswitch/autoload_configs/
        cp -av conf/dialplan/* /etc/freeswitch/dialplan/
        cp -av scripts/* /usr/share/freeswitch/scripts/




* configure Freeswitch :

::

        rm -f /etc/freeswitch/directory/default/*
        chown freeswitch:www-data -R /etc/freeswitch/
        mkdir /tmp/cdr-csv/
        chmod 777 -R /tmp/cdr-csv
        touch /tmp/cdr-csv/Master.csv
        chmod 600 /tmp/cdr-csv/Master.csv
        chown freeswitch:freeswitch /tmp/cdr-csv/Master.csv
        chown -R freeswitch:daemon /tmp/cdr-csv/

You need to adapt acl_conf.xml to accept sip requests from kamailio.

* configure Kamailio :

::

        cp /usr/local/venv/pyfreebilling/install/resources/kam/config/* /etc/kamailio/

Adapt the data in kamctlrc and kamailio-local.cfg (do not touch kamailio.cfg)


* set apache config :

::

        cp /usr/local/venv/pyfreebilling/setup/apache/001-pyfreebilling /etc/apache2/sites-enabled/000-default.conf
        a2ensite 000-default
        /etc/init.d/apache2 restart


* set crontab :

::

    */1 * * * * perl /usr/share/freeswitch/scripts/import-csv.pl>> /var/log/cron.log 2>&1
    * * * * * /usr/local/venv/bin/chroniker -e /usr/local/venv/bin/activate_this.py -p /usr/local/venv/pyfreebilling -s config.settings.local


* modify db password and somme settings in :

::

        /usr/local/venv/pyfreebilling/config/settings/local.py
        /usr/share/freeswitch/scripts/import-csv.pl


* restart FreeSwitch :

::

    systemctl restart freeswitch



Pyfreebilling login
==========================

 Got to the url https://my-ip/extranet and enter your username and password.

 The customer portal url is : https://my-ip

 I recommend to setup a firewall restrincting access to web pages and your voip ports !

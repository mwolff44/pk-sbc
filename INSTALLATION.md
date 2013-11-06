********************************************************************************
                             Table of content
********************************************************************************

- Introduction
- Prerequisites
- Freeswitch installation
- Postgresql configuration
- Web server install
- PyFreeBilling installation
- Next step

********************************************************************************
                             Introduction
********************************************************************************

This howto is written for ubuntu 12.04 LTS server. You can use the same commands for debian based servers, but depending on version, some commands may differ. 

********************************************************************************
                             Prerequisites
********************************************************************************

First, you need to install these packages :

`apt-get install git-core build-essential autoconf automake libtool libncurses5 libncurses5-dev gawk libjpeg-dev zlib1g-dev pkg-config libssl-dev libpq-dev unixodbc-dev odbc-postgresql postgresql postgresql-client libpq-dev libxml2-dev libxslt-dev ntp ntpdate`

********************************************************************************
                             Freeswitch installation
********************************************************************************

*go to the source directory :
`cd /usr/src`

*and download the last stable freeswitch version :
`git clone -b v1.2.stable git://git.freeswitch.org/freeswitch.git`

*after, boostrap, configure, make and install freeswitch :
`cd freeswitch
./bootstrap.sh -j
./configure`

*edit modules.conf suiting your needs. You will find below the minimum modules to install :

`applications/mod_commands
applications/mod_db
applications/mod_dptools
applications/mod_esf
applications/mod_esl
applications/mod_expr
applications/mod_fifo
applications/mod_fsv
applications/mod_hash
applications/mod_memcache
applications/mod_nibblebill
codecs/mod_amr
codecs/mod_g723_1
codecs/mod_g729
dialplans/mod_dialplan_xml
endpoints/mod_loopback
endpoints/mod_sofia
event_handlers/mod_cdr_csv
event_handlers/mod_event_socket
formats/mod_local_stream
formats/mod_native_file
formats/mod_sndfile
formats/mod_tone_stream
languages/mod_lua
languages/mod_spidermonkey
loggers/mod_console
loggers/mod_logfile
loggers/mod_syslog
say/mod_say_en`

* after do :
`make
make install`

* create a freeswitch user and group as follow :
`groupadd freeswitch
adduser --disabled-password  --quiet --system --home /usr/local/freeswitch --gecos "FreeSWITCH Voice Platform" --ingroup daemon freeswitch`

* and to apply the rule to freeswitch user :
	
`chown -R freeswitch:daemon /usr/local/freeswitch/
chmod -R o-rwx /usr/local/freeswitch/`

* and now, we need to create the init script to start and stop freeswitch :
	
`nano /etc/init.d/freeswitch`

* Add your init code

* make this script executable :
	
`chmod +x /etc/init.d/freeswitch
update-rc.d freeswitch defaults`

*add the cli link :
`ln -s /usr/local/freeswitch/bin/fs_cli /bin/fs_cli`

********************************************************************************
                             Postgresql configuration
********************************************************************************

* create user and database :
`sudo -i -u postgres
createuser -P pyfreebilling
	Enter password for new role: 
	Enter it again: 
	Shall the new role be a superuser? (y/n) n
	Shall the new role be allowed to create databases? (y/n) y
	Shall the new role be allowed to create more new roles? (y/n) y
	
createdb -O pyfreebilling -E UTF8 pyfreebilling`

* set odbc parameters
** edit /etc/odbc.ini

`
[freeswitch]
; WARNING: The old psql odbc driver psqlodbc.so is now renamed psqlodbcw.so
; in version 08.x. Note that the library can also be installed under an other
; path than /usr/local/lib/ following your installation.
;Driver         = /usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so
Driver = PostgreSQL
Description = Connection to LDAP/POSTGRESQL
Servername = 127.0.0.1
Port = 5432
Protocol = 6.4
FetchBufferSize = 99
Username = pyfreebilling
Password = 
Database = pyfreebilling
ReadOnly = no
Debug = 0
CommLog = 0`

** edit /etc/odbcinst.ini
`
[PostgreSQL]
Description             = PostgreSQL ODBC driver (Unicode version)
Driver          = /usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so
Setup           = /usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
Debug           = 0
CommLog         = 0
UsageCount              = 0
Threading = 0
MaxLongVarcharSize = 65536`

********************************************************************************
                             Web server install
********************************************************************************

* install some packages :
`apt-get install libapache2-mod-wsgi apache2 gcc python-setuptools python-pip libjpeg62 libjpeg62-dev libdbd-pg-perl libtext-csv-perl
apt-get install python-psycopg2 
apt-get install python-dev`

* install python virtualenv
`pip install virtualenv
cd /usr/local
virtualenv venv --no-site-packages (IMPORTANT : no sudo !!!)`

* activate it :
`source venv/bin/activate
cd venv`

* install CPAN : 
1. Install all dependent packages for CPAN
`apt-get install build-essential`

2. invoke the cpan command as a normal user
$cpan
But once you hit on enter for “cpan” to execute, you
be asked of some few questions. To make it simple for
yourself, answer “no” for the first question so that
the latter ones will be done for you automatically.
3. Once the above is done, you will be present with the cpan
prompt. now enter the commands below
`make install
install Bundle::CPAN`

4. Now all is set and you can install any perl module you want. examples of what installed below
`cpan prompt>  install Carp
cpan prompt>  install Filter::Simple
install Config::Vars`

********************************************************************************
                             Pyfreebilling installation
********************************************************************************

* download pyfreebilling sources :
`git clone git@bitbucket.org:mwolff/pyfreebilling.git
chown -R www-data:www-data pyfreebilling
cd pyfreebilling
pip install -r requirements.txt
python manage.py syncdb
python manage.py migrate
python manage.py loaddata country_dialcode.json`

* copy some config files
`cp -av /usr/local/venv/pyfreebilling/freeswitch/conf/autoload_configs/acl.conf.xml /usr/local/freeswitch/conf/autoload_configs/acl.conf.xml 

cp -av /usr/local/venv/pyfreebilling/freeswitch/conf/autoload_configs/cdr_csv.conf.xml /usr/local/freeswitch/conf/autoload_configs/cdr_csv.conf.xml

cp -av /usr/local/venv/pyfreebilling/freeswitch/conf/autoload_configs/modules.conf.xml /usr/local/freeswitch/conf/autoload_configs/modules.conf.xml

cp -av /usr/local/venv/pyfreebilling/freeswitch/conf/autoload_configs/nibblebill.conf.xml /usr/local/freeswitch/conf/autoload_configs/nibblebill.conf.xml

cp -av /usr/local/venv/pyfreebilling/freeswitch/dialplan/pyfreebill.xml /usr/local/freeswitch/conf/dialplan/pyfreebill.xml

cp -av /usr/local/venv/pyfreebilling/freeswitch/conf/freeswitch.xml /usr/local/freeswitch/conf/freeswitch.xml`

* set good rights :
`rm -f /usr/local/freeswitch/conf/directory/default/*
chown -R freeswitch:freeswitch freeswitch/scripts/
chown freeswitch:www-data -R /usr/local/freeswitch/
chmod 2750 /usr/local/freeswitch
chmod 2750 /usr/local/freeswitch/conf/
chmod 2750 /usr/local/freeswitch/conf/autoload_configs/
chmod 2750 /usr/local/freeswitch/conf/directory/
chmod 770 /usr/local/freeswitch/conf/directory/default.xml
chmod 770 /usr/local/freeswitch/conf/autoload_configs/sofia.conf.xml
create mkdir /tmp/cdr-csv/
chmod 777 -R /tmp/cdr-csv
touch /tmp/cdr-csv/Master.csv
chmod 600 /tmp/cdr-csv/Master.csv
chown freeswitch:freeswitch /tmp/cdr-csv/Master.csv
chown -R freeswitch:daemon /tmp/cdr-csv/`

* set apache config
`cp apache/001-pyfreebilling /etc/apache2/sites-enabled/000-default
a2ensite 000-default
/etc/init.d/apache2 restart`

* set crontab
`*/5 * * * * perl /usr/local/venv/pyfreebilling/freeswitch/scripts/import-csv.pl>> /var/log/cron.log 2>&1
* * * * * /usr/local/venv/pyfreebilling/chroniker -e /usr/local/venv/bin/activate_this.py -p /usr/local/venv/pyfreebilling`

* modify db password and somme settings in :
** `/usr/local/venv/pyfreebilling/pyfreebilling/local_settings.py`
** `/usr/local/venv/pyfreebilling/freeswitch/scripts/import-csv.pl`

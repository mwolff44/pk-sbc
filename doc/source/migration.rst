Migration
*********

Table of contents
=================

* Introduction
* Prerequisites
* From 1.4.5 to 1.4.6

Introduction
============

You will find migration guide from stable version to another one. Please follow carefully each step.

Prerequisites
=============

Before following the migration guide, you must be located in :

::

cd /usr/local/venv/pyfreebilling directory.

Also, you virtual venv must be activated : 

::

source /usr/local/venv/bin/activate


From 1.4.6 to 1.5.0
===================

* Prerequisites

You must use FreeSwitch 1.4 (not use 1.2 and not 1.5 as it is not yet for production) and PostgresSQL ( min 9.1)

* Update PyFreeBilling code :

Go to the working directory (/usr/local/venv/pyfreebilling) and activate the virtal environment.
And after, enter these commands :

::

git pull
pip install -U -r requirements/requirements.txt
python manage.py syncdb
python manage.py migrate
python manage.py loaddata 0001_initial_PyfbSettings.json
python manage.py collectstatic

And restart FreeSwitch and apache !

* create un new file in /usr/local/venv/pyfreebilling/ directory called MyConfig.pm

::

    touch pyfreebilling/MyConfig.pm


* edit this new file, and put yours specific values (change the default password)

::

# ==== CONFIG FILE MyConfig.pm ====
use strict;
package MyConfig;
use Config::Vars;

var $dsn = "DBI:Pg:dbname=pyfreebilling;host=localhost;port=5432";
var $pg_user = "pyfreebilling";
var $pg_pwd = "password";
#var $dbh;
# ==== END CONFIG FILE ====


From 1.4.5 to 1.4.6
===================

Go to the working directory (/usr/local/venv/pyfreebilling) and activate the virtal environment.
And after, just enter these commands :

::

git pull


And restart FreeSwitch.
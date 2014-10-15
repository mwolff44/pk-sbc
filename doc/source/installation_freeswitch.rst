Installation
************

Table of contents
=================

* Introduction
* Prerequisites
* Freeswitch installation
* Postgresql configuration
* Web server install
* PyFreeBilling installation
* Next step

Introduction
============

This howto is written for ubuntu 12.04 LTS server. You can use the same
commands for debian based servers, but depending on version, some
commands may differ.

Prerequisites
=============

First, you need to install these packages (Debian)

::

    apt-get install autoconf automake devscripts gawk g++ git-core libjpeg-dev libncurses5-dev libtool make python-dev gawk pkg-config libtiff5-dev libperl-dev libgdbm-dev libdb-dev gettext libssl-dev libcurl4-openssl-dev libpcre3-dev libspeex-dev libspeexdsp-dev libsqlite3-dev libedit-dev libldns-dev libpq-dev

Freeswitch installation
=======================

* go to the source directory

::

    cd /usr/src

* and download the last stable freeswitch version

::

    git clone -b v1.4 https://stash.freeswitch.org/scm/fs/freeswitch.git

* after, boostrap, configure, make and install freeswitch

::

    cd freeswitch
    ./bootstrap.sh -j
    

* edit modules.conf suiting your needs. You will find below the minimum
   modules to install :

::

   applications/mod_commands
   applications/mod_db
   applications/mod_dptools
   pplications/mod_esf
   applications/mod_esl
   applications/mod_expr
   applications/mod_fifo
   applications/mod_fsv
   applications/mod_hash
   applications/mod_nibblebill
   codecs/mod_amr
   codecs/mod_g723_1
   codecs/mod_spandsp
   codecs/mod_siren
   codecs/mod_amrwb
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
   say/mod_say_en

* after, do :

::

    ./configure
    make
    make install

* you need to compile esl for python

::

    cd libs/esl
    make pymod
    make pymod-install

* create a freeswitch user and group as follow :

::

    adduser --disabled-password  --quiet --system --home /usr/local/freeswitch --gecos "FreeSWITCH Voice Platform" --ingroup daemon freeswitch

* and to apply the rule to freeswitch user :

::

    chown -R freeswitch:daemon /usr/local/freeswitch/
    chmod -R ug=rwX,o= /usr/local/freeswitch/
    chmod -R u=rwx,g=rx /usr/local/freeswitch/bin/

* and now, we need to create the init script to start and stop
   freeswitch :

::

    nano /etc/init.d/freeswitch

* Add your init code

::

	#!/bin/bash
	### BEGIN INIT INFO
	# Provides:          freeswitch
	# Required-Start:    $local_fs $remote_fs
	# Required-Stop:     $local_fs $remote_fs
	# Default-Start:     2 3 4 5
	# Default-Stop:      0 1 6
	# Description:       Freeswitch debian init script.
	# Author:            Matthew Williams
	#
	### END INIT INFO
	# Do NOT "set -e"
	 
	# PATH should only include /usr/* if it runs after the mountnfs.sh script
	PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin
	DESC="Freeswitch"
	NAME=freeswitch
	DAEMON=/usr/local/freeswitch/bin/$NAME
	DAEMON_ARGS="-nc -nonat"
	PIDFILE=/usr/local/freeswitch/run/$NAME.pid
	SCRIPTNAME=/etc/init.d/$NAME
	 
	FS_USER=freeswitch
	FS_GROUP=daemon
	 
	# Exit if the package is not installed
	[ -x "$DAEMON" ] || exit 0
	 
	# Read configuration variable file if it is present
	[ -r /etc/default/$NAME ] && . /etc/default/$NAME
	 
	# Load the VERBOSE setting and other rcS variables
	. /lib/init/vars.sh
	 
	# Define LSB log_* functions.
	# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
	. /lib/lsb/init-functions
	 
	#
	# Function that sets ulimit values for the daemon
	#
	do_setlimits() {
	        ulimit -c unlimited
	        ulimit -d unlimited
	        ulimit -f unlimited
	        ulimit -i unlimited
	        ulimit -n 999999
	        ulimit -q unlimited
	        ulimit -u unlimited
	        ulimit -v unlimited
	        ulimit -x unlimited
	        ulimit -s 240
	        ulimit -l unlimited
	        ulimit -a
	        return 0
	}
	 
	#
	# Function that starts the daemon/service
	#
	do_start()
	{
	    # Set user to run as
	        if [ $FS_USER ] ; then
	      DAEMON_ARGS="`echo $DAEMON_ARGS` -u $FS_USER"
	        fi
	    # Set group to run as
	        if [ $FS_GROUP ] ; then
	          DAEMON_ARGS="`echo $DAEMON_ARGS` -g $FS_GROUP"
	        fi
	 
	        # Return
	        #   0 if daemon has been started
	        #   1 if daemon was already running
	        #   2 if daemon could not be started
	        start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON --test > /dev/null -- \
	                || return 1
	        do_setlimits
	        start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON --background -- \
	                $DAEMON_ARGS \
	                || return 2
	        # Add code here, if necessary, that waits for the process to be ready
	        # to handle requests from services started subsequently which depend
	        # on this one.  As a last resort, sleep for some time.
	}
	 
	#
	# Function that stops the daemon/service
	#
	do_stop()
	{
	        # Return
	        #   0 if daemon has been stopped
	        #   1 if daemon was already stopped
	        #   2 if daemon could not be stopped
	        #   other if a failure occurred
	        start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE --name $NAME
	        RETVAL="$?"
	        [ "$RETVAL" = 2 ] && return 2
	        # Wait for children to finish too if this is a daemon that forks
	        # and if the daemon is only ever run from this initscript.
	        # If the above conditions are not satisfied then add some other code
	        # that waits for the process to drop all resources that could be
	        # needed by services started subsequently.  A last resort is to
	        # sleep for some time.
	        start-stop-daemon --stop --quiet --oknodo --retry=0/30/KILL/5 --exec $DAEMON
	        [ "$?" = 2 ] && return 2
	        # Many daemons don't delete their pidfiles when they exit.
	        rm -f $PIDFILE
	        return "$RETVAL"
	}
	 
	#
	# Function that sends a SIGHUP to the daemon/service
	#
	do_reload() {
	        #
	        # If the daemon can reload its configuration without
	        # restarting (for example, when it is sent a SIGHUP),
	        # then implement that here.
	        #
	        start-stop-daemon --stop --signal 1 --quiet --pidfile $PIDFILE --name $NAME
	        return 0
	}
	 
	case "$1" in
	  start)
	        [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
	        do_start
	        case "$?" in
	                0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
	                2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
	        esac
	        ;;
	  stop)
	        [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
	        do_stop
	        case "$?" in
	                0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
	                2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
	        esac
	        ;;
	  status)
	       status_of_proc -p $PIDFILE $DAEMON $NAME && exit 0 || exit $?
	       ;;
	  #reload|force-reload)
	        #
	        # If do_reload() is not implemented then leave this commented out
	        # and leave 'force-reload' as an alias for 'restart'.
	        #
	        #log_daemon_msg "Reloading $DESC" "$NAME"
	        #do_reload
	        #log_end_msg $?
	        #;;
	  restart|force-reload)
	        #
	        # If the "reload" option is implemented then remove the
	        # 'force-reload' alias
	        #
	        log_daemon_msg "Restarting $DESC" "$NAME"
	        do_stop
	        case "$?" in
	          0|1)
	                do_start
	                case "$?" in
	                        0) log_end_msg 0 ;;
	                        1) log_end_msg 1 ;; # Old process is still running
	                        *) log_end_msg 1 ;; # Failed to start
	                esac
	                ;;
	          *)
	                # Failed to stop
	                log_end_msg 1
	                ;;
	        esac
	        ;;
	  *)
	        #echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
	        echo "Usage: $SCRIPTNAME {start|stop|restart|force-reload}" >&2
	        exit 3
	        ;;
	esac
	 
	exit 0

* Or modify this file /usr/src/freeswitch/debian/freeswitch-sysvinit.freeswitch.init and change

::

    # Near line 20, edit these lines to look like this:
    DAEMON=/usr/local/freeswitch/bin/freeswitch
    CONFDIR=/usr/local/freeswitch/conf
    GROUP=daemon

    # Save the file and copy the init script :
    cp /usr/src/freeswitch/debian/freeswitch-sysvinit.freeswitch.default /etc/default/freeswitch
    cp /usr/src/freeswitch/debian/freeswitch-sysvinit.freeswitch.init  /etc/init.d/freeswitch


* make this script executable :

::

    mkdir /var/lib/freeswitch
    chown freeswitch:daemon /var/lib/freeswitch
    chmod -R ug=rwX,o= /var/lib/freeswitch
    chmod ug=rwX,o= /etc/init.d/freeswitch
    chown freeswitch:daemon /etc/init.d/freeswitch
    chmod +x /etc/init.d/freeswitch
    update-rc.d freeswitch defaults

* add the cli link :

::

	ln -s /usr/local/freeswitch/bin/fs_cli /bin/fs_cli
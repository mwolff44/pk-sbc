#!/bin/sh

#move to script directory so all relative paths work
cd "$(dirname "$0")"

. ../colors.sh
. ../arguments.sh

apt-get update && apt-get install -y --force-yes curl memcached haveged
arch=$(uname -m)
if [ $arch = 'armv7l' ] && [ $USE_SWITCH_PACKAGE_UNOFFICIAL_ARM = true ]; then
        echo "deb http://repo.sip247.com/debian/freeswitch-stable-armhf/ jessie main" > /etc/apt/sources.list.d/freeswitch.list
        curl http://repo.sip247.com/debian/sip247.com.gpg.key | apt-key add -
else
        echo "deb http://files.freeswitch.org/repo/deb/freeswitch-1.6/ jessie main" > /etc/apt/sources.list.d/freeswitch.list
        curl http://files.freeswitch.org/repo/deb/freeswitch-1.6/key.gpg | apt-key add -
fi
apt-get update
apt-get install -y --force-yes gdb ntp
apt-get install -y --force-yes freeswitch-meta-bare freeswitch-conf-vanilla freeswitch-mod-commands freeswitch-meta-codecs freeswitch-mod-console freeswitch-mod-logfile
apt-get install -y --force-yes freeswitch-mod-cdr-csv freeswitch-mod-event-socket freeswitch-mod-sofia freeswitch-mod-sofia-dbg freeswitch-mod-loopback
apt-get install -y --force-yes freeswitch-mod-db freeswitch-mod-dptools freeswitch-mod-expr
apt-get install -y --force-yes freeswitch-mod-hash freeswitch-mod-esl freeswitch-mod-dialplan-xml freeswitch-dbg
apt-get install -y --force-yes freeswitch-mod-sndfile freeswitch-mod-native-file freeswitch-mod-lua freeswitch-mod-directory

#make sure that postgresql is started before starting freeswitch
sed -i /lib/systemd/system/freeswitch.service -e s:'local-fs.target:local-fs.target postgresql.service:'
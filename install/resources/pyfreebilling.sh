#!/bin/sh

#move to script directory so all relative paths work
cd "$(dirname "$0")"

. ./colors.sh
. ./arguments.sh

#send a message
verbose "Installing pyfreebilling"

#install dependencies
apt-get install -y --force-yes git dbus haveged ssl-cert
apt-get install -y --force-yes ghostscript libtiff5-dev libtiff-tools

if [ $USE_SYSTEM_MASTER = false ]; then
	PYFB_MAJOR=$(git ls-remote --heads https://github.com/mathias44w/pyfreebilling.git | cut -d/ -f 3 | grep -P '^\d+\.\d+' | sort | tail -n 1 | cut -d. -f1)
	PYFB_MINOR=$(git ls-remote --tags https://github.com/mathias44w/pyfreebilling.git $PYFB_MAJOR.* | cut -d/ -f3 |  grep -P '^\d+\.\d+' | sort | tail -n 1 | cut -d. -f2)
	PYFB_VERSION=$PYFB_MAJOR.$PYFB_MINOR
	verbose "Using version $PYFB_VERSION"
	BRANCH="-b $PYFB_VERSION"
else
	verbose "Using master"
	BRANCH=""
fi

#get the source code
git clone $BRANCH https://github.com/mathias44w/pyfreebilling.git /var/www/pyfreebilling
chown -R www-data:www-data /var/www/pyfreebilling
chmod -R 755 /var/www/pyfreebilling/
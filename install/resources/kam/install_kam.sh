curl http://deb.kamailio.org/kamailiodebkey.gpg | apt-key add -
echo "deb http://deb.kamailio.org/kamailio44 jessie main" > /etc/apt/sources.list.d/kamailio.list
echo "deb-src http://deb.kamailio.org/kamailio44 jessie main" >> /etc/apt/sources.list.d/kamailio.list
apt-get update
apt-get -y install kamailio kamailio-extra-modules kamailio-postgres-modules kamailio-tls-modules

sed "/^[# ]*SIP_DOMAIN/cSIP_DOMAIN=sip.<DOMAIN>.net" -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBENGINE/cDBENGINE=PGSQL' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBHOST/cDBHOST=localhost' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBNAME/cDBNAME=openser' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBRWUSER/cDBRWUSER=openser' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBRWPW/cDBRWPW="openser"' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBROUSER/cDBROUSER=openserro' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBROPW/cDBROPW=openserro' -i /etc/kamailio/kamctlrc
sed '/^[# ]*DBROOTUSER/cDBROOTUSER="postgres" ' -i /etc/kamailio/kamctlrc


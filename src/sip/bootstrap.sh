#!/bin/bash
set -e

PATH=/usr/local/bin:$PATH

SHM_MEM=512
PKG_MEM=64
FILE=/bootstrap.sh

if test -f "$FILE"; then
    echo "Link already present"
else
    ln -s /etc/kamailio/bootstrap.sh /bootstrap.sh
fi

case $CLOUD in 
  gcp)
    LOCAL_IP=$(curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/ip)
    PUBLIC_IP=$(curl -s -H "Metadata-Flavor: Google" http://metadata/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
    ;;
  aws)
    LOCAL_IP=$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
    ;;
  digitalocean)
    LOCAL_IP=$(curl -s http://169.254.169.254/metadata/v1/interfaces/private/0/ipv4/address)
    PUBLIC_IP=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
    ;;
  scaleway)
    LOCAL_IP=$(curl -s --local-port 1-1024 http://169.254.42.42/conf | grep PRIVATE_IP | cut -d = -f 2)
    PUBLIC_IP=$(curl -s --local-port 1-1024 http://169.254.42.42/conf | grep PUBLIC_IP_ADDRESS | cut -d = -f 2)
    ;;
  azure)
    LOCAL_IP=$(curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/privateIpAddress?api-version=2017-08-01&format=text")
    PUBLIC_IP=$(curl -H Metadata:true "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-08-01&format=text")
    ;;
  *)
    LOCAL_IP=`ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'`
    ;;
esac

# run kamailio
export PATH_KAMAILIO_CFG=/etc/kamailio/kamailio.cfg
kamailio=$(which kamailio)

# Add my IP
if [ -n "$LISTEN_PRIVATE" ]; then
  echo -n 'LISTEN_PRIVATE is: '; echo "$LISTEN_PRIVATE"
  echo "#!define LISTEN_PRIVATE $LISTEN_PRIVATE" >> /etc/kamailio/kamailio-local.cfg
else
  echo -n 'LISTEN_PRIVATE is: '; echo "$LOCAL_IP:5061"
  echo "#!define LISTEN_PRIVATE $LOCAL_IP:5061" >> /etc/kamailio/kamailio-local.cfg
fi

if [ -n "$LISTEN_PUBLIC" ]; then
  echo -n 'LISTEN_PUBLIC is: '; echo "$LISTEN_PUBLIC"
  echo "#!define LISTEN_PUBLIC $LISTEN_PUBLIC" >> /etc/kamailio/kamailio-local.cfg
else
  echo -n 'LISTEN_PUBLIC is: '; echo "$LOCAL_IP:5060"
  echo "#!define LISTEN_PUBLIC $LOCAL_IP:5060" >> /etc/kamailio/kamailio-local.cfg
fi

if [ -n "$LISTEN_ADVERTISE" ]; then
    echo -n 'PUBLIC_IP is: '; echo "$LISTEN_ADVERTISE"
    echo "#!define LISTEN_ADVERTISE $LISTEN_ADVERTISE" >> /etc/kamailio/kamailio-local.cfg
else
  if [ -n "$PUBLIC_IP" ]; then
    echo -n 'PUBLIC_IP is: '; echo "$PUBLIC_IP"
    echo "#!define LISTEN_ADVERTISE $PUBLIC_IP:5060" >> /etc/kamailio/kamailio-local.cfg
  else
    echo ' No public IP available !'
  fi
fi

if [ -n "$RTPENGINE_URL" ]; then
  echo -n 'RTPENGINE_URL is: '; echo "$RTPENGINE_URL"
  rtpengine=$(echo '#!define RTPENGINE_LIST "udp:RTPENGINE_URL:22222=1"' | sed "s/RTPENGINE_URL/$RTPENGINE_URL/")
  echo "$rtpengine" >> /etc/kamailio/kamailio-local.cfg
fi

if [ -n "$REDIS_URL" ]; then
  echo -n 'REDIS_URL is: '; echo "$REDIS_URL"
  redis=$(echo '#!define REDIS "name=srv8;addr=REDIS_URL;port=6379;db=8"' | sed "s/REDIS_URL/$REDIS_URL/")
  echo "$redis" >> /etc/kamailio/kamailio-local.cfg
fi

# Test the syntax.
echo 'kamailio-local.cfg : '
cat /etc/kamailio/kamailio-local.cfg
$kamailio -f $PATH_KAMAILIO_CFG -c
echo 'Kamailio will be called using the following environment variables:'
echo -n '$DUMP_CORE is: ' ; echo "${DUMP_CORE}"
echo -n '$SHM_MEM is: ' ; echo "${SHM_MEM}"
echo -n '$PKG_MEM is: ' ; echo "${PKG_MEM}"
echo -n '$ENVIRONMENT is: ' ; echo "${ENVIRONMENT}"

# Run kamailio
if [ "$1" = 'kamailio' ]; then
  shift
  exec $kamailio -f $PATH_KAMAILIO_CFG -m "${SHM_MEM}" -M "${PKG_MEM}" -DD -E -e
fi

exec $@
#!/bin/bash
echo $0 starting
# to start it with settings environment values on the fly :
# VOIP_DOMAIN=dev-voip.com FROM_CALLER=+33613000014 /scripts/full_test.sh

MSISDN_FROM=${FROM_CALLER}
VOIP_DOMAIN=${VOIP_DOMAIN}

VOIP_PATROL_DIR=.
VOIP_PATROL_XML_DIR=scripts/xml/
VOIP_PATROL_BINARY=$(which voip_patrol)
VOIP_PATROL_BINARY=./voip_patrol
VOIP_PATROL_RESULTS_DIR=/
VOIP_PATROL_RESULTS_FILENAME=results.json

SIP_RESPONSE_LIST="403,404,408,486,487,503,200"
IFS=,
for SIP_RESPONSE_CODE in $SIP_RESPONSE_LIST;
do
  echo ============== SIP_RESPONSE_CODE = $SIP_RESPONSE_CODE==========================
  MSISDN_TO=+33100000$SIP_RESPONSE_CODE

  echo "makecall from $MSISDN_FROM to $MSISDN_TO expecting SIP reesponse code $SIP_RESPONSE_CODE..."
  VOIP_PATROL_XML_FILE=makecall_$SIP_RESPONSE_CODE.xml


  XMLFILE=$VOIP_PATROL_XML_DIR/$VOIP_PATROL_XML_FILE

  sed -i -r "s/registrar=.*/registrar=\"${VOIP_DOMAIN}\"/" $XMLFILE
  sed -i -r "s/callee=.*/callee=\"${MSISDN_TO}@${VOIP_DOMAIN}\"/" $XMLFILE
  sed -i -r "s/caller=.*/caller=\"${CALLER}@${VOIP_DOMAIN}\"/" $XMLFILE
  sed -i -r "s/account=.*/account=\"${USER_ID_TEST}\"/" $XMLFILE
  sed -i -r "s/username=.*/username=\"${MSISDN_FROM}\"/" $XMLFILE
  sed -i -r "s/\"Bearer .*\"/\"Bearer ${TOKEN_TEST}\"/" $XMLFILE
  sed -i -r "s/label=.*/label=\"${VOIP_PATROL_XML_FILE}\"/" $XMLFILE

  # execute in /scripts/ to use default /tls/* certifcates
  cd $VOIP_PATROL_DIR
  $VOIP_PATROL_BINARY -c  $XMLFILE -o $VOIP_PATROL_RESULTS_DIR/$VOIP_PATROL_RESULTS_FILENAME --gracefull-shutdown --log-level-file 0 --log-level-console 3

done
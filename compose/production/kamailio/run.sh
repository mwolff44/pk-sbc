#!/usr/bin/dumb-init /bin/bash

. /env.sh

for var in ${!DEFAULT_KAM*}; do
  t=${var/DEFAULT_/}
  if [ -z ${!t} ]; then
    echo "Using default for ${t}:${!var}"
    eval ${t}=${!var}
    export "${t}"
  else
    echo "Using override value for ${t}"
  fi
done

for var in ${!KAM_*}; do
  if [[ $var == KAM_*  && "${var}" != "KAM_DISPATCHER_ROUTES" ]]; then
    if [[ $var == KAM_DEFINE_* && ${!var} != "false" ]]; then
      echo "#!define ${var/KAM_DEFINE_/} \"${!var}\"" >> "/etc/kamailio/kamailio-local.cfg"
    fi
  fi
done

exec "${@}"

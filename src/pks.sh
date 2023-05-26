#!/usr/bin/env bash

# PKS P-KISS-SBC
# (c) 2022 Mathias WOLFF
#
# This file is copyright under the latest version of the EUPL.
# Please see LICENSE file for your rights under this license.

VERSION="1.0.0"
APP_NAME="PKS"
SCRIPT_NAME=$(basename "$0")
ENV_FILE="/srv/.env"
DC_FILE="/usr/src/pyfreebilling/src/sip/docker-compose.yml"
DOCKER_COMPOSE=(docker compose -f ${DC_FILE} --env-file ${ENV_FILE})

#----------------------------------------------------
# wait for a yes or no answer
#----------------------------------------------------
confirmFunc(){
  echo -e "Are you sure? \c"
  while true
  do
    read x
    case "$x" in
      y | yes | Y | Yes | YES )
        return 0;;
      n | no  | N | No  | NO )
        echo
        echo "Cancelled"
        exit 1;;
      *) echo "Please enter yes or no" ;;
    esac
  done
}

test_prerequesites(){
  echo "test if prerequesites are respected"
}

install_prerequesites(){
  echo "Install prerequesites"
}

Select_db(){
    echo "Before installation, where do you want to store data ?"
    PS3="Select your DB choice please: "

    select db in Default DBtext MySQL PostgreSQL SQLite Quit
    do
        case $db in
            "Default")
                echo "$db database selected - we will use DBText";;
            "MySQL")
                echo "$db database selected";;
            "PostgreSQL")
                echo "$db database selected";;
            "SQLite")
                echo "$db database selected";;
            "Quit")
                echo "Install process aborted"
                break;;
            *)
                echo "Ooops - unknown choice";;
        esac
    done
}

startFunc(){
  echo -e "Start PKS ..."
  "${DOCKER_COMPOSE[@]}" up -d
  exit 1
}

stopFunc(){
  echo -e "Stop PKS ..."
  "${DOCKER_COMPOSE[@]}" down
  exit 1
}

restartFunc(){
    echo -e "Stop PKS ..."
  "${DOCKER_COMPOSE[@]}" down
  sleep 1
  echo -e "Start PKS ..."
  "${DOCKER_COMPOSE[@]}" up -d
  exit 1
}

reloadFunc(){
  echo "PKS will reload data from database"
  echo " ... reload address table ..."
  docker exec -it pks-sip kamcmd permissions.addressDump
  sleep 1
  echo " ... reload dialplan table ..."
  docker exec -it pks-sip kamcmd dialplan.reload
  sleep 1
  echo " ... reload tenant table ..."
  docker exec -it pks-sip kamcmd htable.reload tenantmap
  sleep 1
  echo " ... reload dispatcher table ..."
  docker exec -it pks-sip kamcmd dispatcher.reload
  echo "PKS has been refreshed with latest data"
}

debugFunc(){
  "${DOCKER_COMPOSE[@]}" logs --tail=100 -f
  exit 1
}

statusFunc(){
  "${DOCKER_COMPOSE[@]}" ps
  exit 1
}

helpFunc(){
  echo "Usage: pks [options]
  Example: 'pks -r -h'
  Add '-h' after specific commands for more information on usage

  Admin Options:
    start              start PKS
    stop               stop PKS
    restart            restart PKS
    -r, reload         reload PKS

  Debugging Options:
    -d, debug          View the live output of the PKS log
    -s, status         status ok PKS containers

  Options:
    -h, --help, help   Show this help dialog  
    -v, version        Show installed version
    uninstall          Uninstall PKS from your system
    update             Update PKS

  install              Install PKS
  ";

  exit 0
}

versionFunc(){
  echo -e "PKS version ${VERSION}"
  exit 0
}

uninstallFunc(){
  echo "Not available, sorry"
  exit 0
}

updateFunc(){
  echo "PKS will be updated. PKS will be retarded, are you sure ?"
  confirmFunc
  echo "Starting update ..."
  "${DOCKER_COMPOSE[@]}" build
  echo "Update successfully done."
  restartFunc
  exit 0
}

installFunc(){
  echo "Not available, sorry"
  exit 0
}

###### MAIN #####

if [[ $# = 0 ]]; then
  helpFunc
fi

case "${1}" in
  "start"                       ) startFunc "$@";;
  "stop"                        ) stopFunc "$@";;
  "restart"                     ) restartFunc "$@";;
  "-r" | "reload"               ) reloadFunc "$@";;
  "-d" | "debug"                ) debugFunc "$@";;
  "-s" | "status"               ) statusFunc "$@";;
  "-h" | "help" | "--help"      ) helpFunc;;
  "-v" | "version"              ) versionFunc "$@";;
  "uninstall"                   ) uninstallFunc "$@";;
  "update"                      ) updateFunc "$@";;
  "install"                     ) installFunc "$@";;
  *                             ) helpFunc;;
esac

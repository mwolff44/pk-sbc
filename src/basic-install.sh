#!/usr/bin/env bash

# PKS P-KISS-SBC
#
# Copyright: (c) 2007-2024 Mathias WOLFF (mathias@celea.org)
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)
# SPDX-License-Identifier: AGPL-3.0-or-later

# Append common folders to the PATH to ensure that all basic commands are available.
export PATH+=':/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

# Variables
readonly PKS_GIT_URL="https://raw.githubusercontent.com/mwolff44/pyfreebilling"
readonly PKS_INSTALL_DIR="/srv/pks/scripts"
readonly PKS_BIN_DIR="/usr/local/bin"
readonly VERSION="v4.1.2"

# Install the PKS script from repository
installScript() {
    local str="Installing scripts from PKS sources"
    printf "  %b %s..." "${INFO}" "${str}"

    # DEPENDENCIES
    apt install -y curl

    install -d ${PKS_INSTALL_DIR}
    curl -fsSL -o ${PKS_INSTALL_DIR}/pks "$PKS_GIT_URL/$VERSION/src/pks"
    chmod +x ${PKS_INSTALL_DIR}/pks
    ln -sf ${PKS_INSTALL_DIR}/pks ${PKS_BIN_DIR}/pks
}

# Launch the PKS script
launchScript() {
    local str="Launching PKS script"
    printf "  %b %s..." "${INFO}" "${str}"
    pks install
}

###### MAIN #####


read -p "Do you want to execute the script ? [y/N]" -n 1 -r </dev/tty
echo

if [[ $REPLY =~ ^[Nn]$ ]]
then
  exit
fi


installScript
launchScript

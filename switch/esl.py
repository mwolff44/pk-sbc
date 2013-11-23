# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling. If not, see <http://www.gnu.org/licenses/>

from ESL import *
from switch import logger
from switch.models import *

def get_fs_connections():
    """
    Get all available ESL connections.
    """
    logger.info("get_fs_connections()")
    voipswitchs = VoipSwitch.objects.all()
    if voipswitchs:
        logger.info("%s voipswitch's config" % len(voipswitchs))
    else:
        logger.error("No voip switch config found! Unable to connect to freeswitch.")
        
    for vs in voipswitchs:
        logger.info("creating ESL connection : %s / %s / %s" % (str(vs.esl_listen_ip), vs.esl_listen_port, vs.esl_password))
        yield ESLconnection("%s" % vs.esl_listen_ip, "%s" % vs.esl_listen_port, "%s" % str(vs.esl_password))

    logger.info("get_fs_connections() done")

def fs_cmd(command):
    """
    Operations via ESL.
    """
    logger.info("fs_cmd: " + command)

    for connection in get_fs_connections():
    	logger.info("connection : %s" % connection)
        if not connection.connected():
            raise IOError("No connection to FreeSWITCH")
        try:
            connection.sendRecv(command.encode('utf-8'))
        except Exception, e:
            logger.info("fs_cmd error: " + str(e))
            raise
        logger.info("fs_cmd done")
        return
    raise ValueError("No EventSocket configured in FreeSwitch. "
        "Cannot connect to FreeSWITCH over event socket")

        
def getReloadACL():
    """Reload ACL"""
    fs_cmd("bgapi reloadacl")

    
def getReloadGateway(profile_name):
    """Reload sofia's gateway"""
    fs_cmd("bgapi sofia profile " + profile_name + " rescan reloadxml")
    
    
def getRestartSofia(profile_name):
    """Restart sofia profile"""
    fs_cmd("bgapi sofia profile " + profile_name + " restart")



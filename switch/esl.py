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
# Source code from PyMunin
# Modified by Mathias WOLFF

import re
import ESL 

# Default
defaultESLport = 8021
defaultESLsecret = 'ClueCon'
conn_timeout = 5


class FSinfo:
    """Class that establishes connection to FreeSWITCH ESL Interface
    to retrieve statistics on operation.

    """

    def __init__(self, host='127.0.0.1', port=defaultESLport, secret="ClueCon", 
                 autoInit=True):
        """Initialize connection to FreeSWITCH ESL Interface.
        
        @param host:     FreeSWITCH Host
        @param port:     FreeSWITCH ESL Port
        @param secret: FreeSWITCH ESL Secret
        @param autoInit: If True connect to FreeSWITCH ESL Interface on 
                         instantiation.

        """
        # Set Connection Parameters
        self._eslconn = None
        self._eslhost = host or '127.0.0.1'
        self._eslport = int(port or defaultESLport)
        self._eslpass = secret or defaultESLsecret
        
        ESL.eslSetLogLevel(0)
        if autoInit:
            self._connect()

    def __del__(self):
        """Cleanup."""
        if self._eslconn is not None:
            del self._eslconn

    def _connect(self):
        """Connect to FreeSWITCH ESL Interface."""
        try:
            self._eslconn = ESL.ESLconnection(self._eslhost, 
                                              str(self._eslport), 
                                              self._eslpass)
        except:
            pass
        if not self._eslconn.connected():
            raise Exception(
                "Connection to FreeSWITCH ESL Interface on host %s and port %d failed."
                % (self._eslhost, self._eslport)
                )
    
    def _execCmd(self, cmd, args):
        """Execute command and return result body as list of lines.
        
            @param cmd:  Command string.
            @param args: Command arguments string. 
            @return:     Result dictionary.
            
        """
        command = cmd + " " + args
        print command
        print command.encode('utf-8')
        output = self._eslconn.sendRecv(command.encode('utf-8'))
        body = output.getBody()
        if body:
            return body.splitlines()
        return None
    
    def _execShowCmd(self, showcmd):
        """Execute 'show' command and return result dictionary.
        
            @param cmd: Command string.
            @return: Result dictionary.
            
        """
        result = None
        lines = self._execCmd("show", showcmd)
        if lines and len(lines) >= 2 and lines[0] != '' and lines[0][0] != '-':
            result = {}
            result['keys'] = lines[0].split(',')
            items = []
            for line in lines[1:]:
                if line == '':
                    break
                items.append(line.split(','))
            result['items'] = items
        return result
    
    def _execShowCountCmd(self, showcmd):
        """Execute 'show' command and return result dictionary.
        
            @param cmd: Command string.
            @return: Result dictionary.
            
        """
        result = None
        lines = self._execCmd("api show", showcmd + " count")
        for line in lines:
            mobj = re.match('\s*(\d+)\s+total', line)
            if mobj:
                return int(mobj.group(1))
        return result

    def getChannelCount(self):
        """Get number of active channels from FreeSWITCH.
        
        @return: Integer or None.
        
        """
        return self._execShowCountCmd("channels")
        
    def getReloadGateway(self):
        """Reload sofia's gateway"""
        result = None
        return self._execCmd("bgapi", "reload mod_sofia")

        
fs = FSinfo(host='127.0.0.1', port=defaultESLport, secret="ClueCon")
print fs.getChannelCount()
print fs.getReloadGateway()
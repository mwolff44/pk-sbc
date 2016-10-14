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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

# The Initial Developer of the Original Code is
# Traun Leyden <tleyden@branchcut.com>
# Portions created by the Initial Developer are Copyright (C)
# the Initial Developer. All Rights Reserved.
# 
# Contributor(s): Riccardo Magliocchetti

import logging
import traceback

"""
Log levels:

    CRITICAL
    ERROR
    WARNING
    INFO
    DEBUG
"""

logobj = logging.getLogger('wikipbx')
logobj.setLevel(logging.DEBUG)
#logobj.setLevel(logging.INFO)

handler = logging.StreamHandler()
logobj.addHandler(handler)

def info(*messages):
    logobj.info(*messages)

def debug(*messages):
    logobj.debug(*messages)

def error(*messages):
    logobj.error(*messages)
    tb = traceback.format_exc()
    logobj.error(tb)

def warn(*messages):
    logobj.warning(*messages)

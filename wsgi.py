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

import django.core.handlers.wsgi

import os
import sys
import site

DIRS = ['/usr/local/venv/lib/python2.7/site-packages']

for directory in DIRS:
    site.addsitedir(directory)

sys.path.insert(0, directory)

root = os.path.join(os.path.dirname(__file__))

# sys.path.append('/usr/local/venv/pyfreebilling')

sys.path.insert(0, root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyfreebilling.settings'

application = django.core.handlers.wsgi.WSGIHandler()

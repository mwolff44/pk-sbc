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

from django.core.exceptions import ValidationError

from netaddr import IPNetwork, AddrFormatError

import re


def validate_cidr(value):
    if value:
        try:
            cidr_val = IPNetwork(value)
            m = re.search('/32$', value)
            if m:
                return IPNetwork(cidr_val)
            elif len(cidr_val) == 1:
                return str(cidr_val) + str('/32')
            else:
                return IPNetwork(cidr_val)
        except (AddrFormatError, TypeError), e:
            raise ValidationError(str(e))

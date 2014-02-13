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


def validate_cidr(value):
    if value:
        try:
            cidr_val = IPNetwork(value)
            return IPNetwork(cidr_val)
        except (AddrFormatError, TypeError), e:
            raise ValidationError(str(e))

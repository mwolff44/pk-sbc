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
# Initial code from parseltone -- parseltone.org
# Modify by Mathias WOLFF

import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_integer, validate_ipv4_address
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


def validate_freeswitch_variable(value):
    m = re.compile('^\$\$\{\w+\}$').search(value.strip())
    if not m or not m.group():
        raise ValidationError(_(u'Invalid FreeSWITCH variable.'))

def validate_freeswitch_integer(value):
    try:
        validate_integer(value)
    except ValidationError, e:
        try:
            validate_freeswitch_variable(smart_unicode(value))
        except ValidationError:
            raise ValidationError(_(u'Enter an integer or a '
                'FreeSWITCH variable.'))

def validate_freeswitch_ipaddress(value):
    try:
        validate_ipv4_address(value)
    except ValidationError, e:
        try:
            validate_freeswitch_variable(value)
        except ValidationError:
            raise ValidationError(_(u'Enter a valid IPv4 address, '
                'or a FreeSWITCH variable.'))
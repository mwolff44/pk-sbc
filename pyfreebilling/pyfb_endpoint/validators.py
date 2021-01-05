from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

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
        except AddrFormatError as e:
            raise ValidationError(str(e))

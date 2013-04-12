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

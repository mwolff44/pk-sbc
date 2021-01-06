# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from netaddr import IPNetwork
import re
import random
import string

from model_utils.models import TimeStampedModel
from model_utils import Choices

from partial_index import PartialIndex

from pyfb_company.models import Customer, Provider

from pyfb_normalization.models import NormalizationGrp

from pyfb_kamailio.models import Domain, UacReg

from .validators import validate_cidr


def random_string():
    # Alphanumeric + special characters
    chars = string.ascii_letters + string.digits + string.punctuation

    pwdSize = 25

    return str(''.join((random.choice(chars)) for _ in range(pwdSize)))


class Codec(TimeStampedModel):

    # Fields
    name = models.CharField(_(u"name"), max_length=100, unique=True)
    number = models.PositiveIntegerField(_(u"payload number"), unique=True, help_text=_(u"payload types (PT) for audio encodings"))
    ptime = models.PositiveIntegerField(_(u"ptime"))
    stereo = models.BooleanField(_(u"is stereo ?"), default=False)
    rfc_name = models.CharField(_(u"rfc name"), max_length=30, unique=True, help_text=_(u"format is important !."))
    description = models.TextField(_(u"description"), blank=True, max_length=100)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-endpoint:pyfb_endpoint_codec_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-endpoint:pyfb_endpoint_codec_update', args=(self.pk,))


class CustomerEndpoint(TimeStampedModel):
    """ Customer Endpoint Model """

    # Choices
    SIP_TRANSPORT_CHOICES = Choices(
        'udp',
        'tcp',
        'tls'
    )
    RTP_TRANSPORT_CHOICES = Choices(
        'RTP/AVP',
    )
    TOS_RTP_CHOICES = Choices(
        # reference : https://en.wikipedia.org/wiki/Type_of_service
        (0, '0 - CS0 - 0 Best effort'),
        (160, '160 - CS5 - 5 Critical'),
        (184, '184 - EF - 5 Critical'),
    )

    # Fields
    name = models.CharField(_(u"username"), max_length=50, unique=True, help_text=_(u"Ex.: customer SIP username, etc..."))
    enabled = models.BooleanField(_(u"enabled / disabled"), default=True)
    registration = models.BooleanField(_(u"registration"), default=True, help_text=_(u"Is registration needed for calling ? True, the phone needs to register with correct username/password. If false, you must specify a CIDR in SIP IP CIDR !"))
    password = models.CharField(_(u"password"), max_length=64, blank=True, default=random_string, help_text=_(u"It's recommended to use strong passwords for the endpoint."))
    ha1 = models.CharField(_(u"ha1"), max_length=128, blank=True, default=random_string, help_text=_(u"It's recommended to use strong passwords for the endpoint. md5(username:realm:password)"))
    ha1b = models.CharField(_(u"ha1b"), max_length=128, blank=True, default=random_string, help_text=_(u"It's recommended to use strong passwords for the endpoint. md5(username@domain:realm:password)"))
    rtp_ip = models.CharField(_(u"RTP IP CIDR"), max_length=100, default="auto", help_text=_(u"Internal IP address/mask to bindto for RTP. Format : CIDR Ex. 192.168.1.0/32"))
    sip_ip = models.CharField(_(u"SIP IP CIDR"), max_length=100, null=True, blank=True, validators=[validate_cidr], help_text=_(u"Internal IP address/mask to bind to for SIP. Format : CIDR. Ex. 192.168.1.0/32"))
    sip_port = models.PositiveIntegerField(_(u"SIP port"), default=5060)
    sip_transport = models.CharField(_(u"SIP transport protocol"), max_length=15, default="udp", choices=SIP_TRANSPORT_CHOICES, help_text=_(u"Which transport protocol to use for SIP messages"))
    rtp_transport = models.CharField(_(u"RTP transport protocol"), max_length=15, default="RTP/AVP", choices=RTP_TRANSPORT_CHOICES, help_text=_(u"Which transport protocol to use for RTP packets"))
    rtp_tos = models.PositiveIntegerField(_(u"TOS value for RTP streams"), default=184, choices=TOS_RTP_CHOICES, help_text=_(u"Which TOS value to use for RTP packets"))
    max_calls = models.PositiveIntegerField(_(u'max calls'), default=1, help_text=_(u"max simultaneous calls allowed for this customer account."))
    calls_per_second = models.PositiveIntegerField(_(u'max calls per second'), default=10, help_text=_(u"maximum calls per second allowed for this customer endpoint."))
    outbound_caller_id_name = models.CharField(_(u"callerID name"), max_length=50, blank=True, help_text=_(u"Caller ID name sent to provider on outbound calls."))
    outbound_caller_id_number = models.CharField(_(u"callerID num"), max_length=80, blank=True, help_text=_(u"Caller ID number sent to provider on outbound calls."))
    force_caller_id = models.BooleanField(_(u"force callerID"), default=False)
    masq_caller_id = models.BooleanField(_(u"masq callerID"), default=False)
    pai = models.BooleanField(_(u"caller ID in PAI field"), default=False, help_text=_(u"put callerid in SIP P-Asserted-Id field if enabled"))
    pid = models.BooleanField(_(u"caller ID in PID field"), default=False, help_text=_(u"put callerid in SIP PID field if enabled"))
    ppi = models.BooleanField(_(u"caller ID in PPD field"), default=False, help_text=_(u"put callerid in SIP P-Preferred-Id field if enabled"))
    urgency_number = models.BooleanField(_(u"allow urgency numbers"), default=True, help_text=_(u"You have also to allow global routing option and define an urgency ratecard"))
    insee_code = models.CharField(_(u'special code for routing urgency numbers'), null=True, blank=True, max_length=10, help_text=_(u"Postal code, INSEE code ... for routing urgency number to the right urgency call center."))
    fake_ring = models.BooleanField(_(u"fake ring"), default=False, help_text=_(u"Fake ring : Enabled / Disabled - Send a fake ring to the caller."))
    cli_debug = models.BooleanField(_(u"CLI debug"), default=False, help_text=_(u"CLI debug : Enabled / Disabled - Permit to see all debug messages on cli."))
    transcoding_allowed = models.BooleanField(_(u'allow transcoding calls'), default=False, help_text=_(u"If enabled, calls could be transcoded. be careful, as it is an expensive cpu task."))
    recording_allowed = models.BooleanField(_(u'allow recording calls'), default=False, help_text=_(u"If enabled, calls could be recorded. be careful on available space."))
    recording_always = models.BooleanField(_(u'record all calls'), default=False, help_text=_(u"If enabled, all calls will be recorded. be careful on available space."))
    recording_limit = models.PositiveIntegerField(_(u'recording space storage'), default=30, help_text=_(u"how many Mo will be available for recording storage."))
    recording_retention = models.PositiveIntegerField(_(u'retention days for recording'), default=30, help_text=_(u"how many days a recording will be available. After, it will be deleted by automatic job"))
    description = models.TextField(_(u'description'), blank=True)

    # Relationship Fields
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE, related_name="customers", verbose_name=_(u"customer")
    )
    callerid_norm = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='calleridnormrules_c', null=True, blank=True, verbose_name=_(u"CallerID normalization rules for outbound call")
    )
    callee_norm = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='caleenormrules_c', null=True, blank=True, verbose_name=_(u"Destination number normalization rules for outbound call")
    )
    callerid_norm_in = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='calleridnormrulesin_c', null=True, blank=True, verbose_name=_(u"CallerID normalization rules for inbound call")
    )
    callee_norm_in = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='caleenormrulesin_c', null=True, blank=True, verbose_name=_(u"Destination number normalization rules for inbound call")
    )
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE, related_name='domain_edp', verbose_name=_(u"SIP Domain")
    )
    codec_list = models.ManyToManyField(
        Codec, blank=True,
        related_name="codecs_c",
        help_text=_(u"if NULL, all available codecs are allowed")
    )


    class Meta:
        db_table = 'pyfb_endpoint_customer'
        ordering = ('customer', 'name')
        verbose_name = _(u'customer endpoint')
        verbose_name_plural = _(u'customer endpoints')
        indexes = [
            PartialIndex(fields=['name', 'callerid_norm'], unique=True, where_postgresql='enabled = True'),
            PartialIndex(fields=['name', 'callee_norm'], unique=True, where_postgresql='enabled = True'),
            PartialIndex(fields=['name', 'callerid_norm_in'], unique=True, where_postgresql='enabled = True'),
            PartialIndex(fields=['name', 'callee_norm_in'], unique=True, where_postgresql='enabled = True'),
        ]

    def __str__(self):
        return "%s (%s:%s)" % (self.name, self.sip_ip, self.sip_port)

    def get_absolute_url(self):
        return reverse('pyfb-endpoint:pyfb_endpoint_customerendpoint_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('pyfb-endpoint:pyfb_endpoint_customerendpoint_update', args=(self.pk,))

    def clean(self):
        if (self.registration and
                (self.password is None or self.password == '')):
            raise ValidationError(_(u"""You have to specify a password if you
                                  want to allow registration"""))
        if (self.registration is False and
                (self.sip_ip is None or self.sip_ip == '')):
            raise ValidationError(_(u"""You must specify a SIP IP CIDR if you do
                                  not want to use registration"""))
        if self.registration and self.password:
            # in future use https://github.com/dstufft/django-passwords ?
            MIN_LENGTH = 8
            if len(self.password) < MIN_LENGTH:
                raise ValidationError(_(u"""The password must be at least %d
                                      characters long.""") % MIN_LENGTH)
            first_isalpha = self.password[0].isalpha()
            if all(c.isalpha() == first_isalpha for c in self.password):
                raise ValidationError(_(u"""The new password must contain
                                            at least one letter and at least
                                            one digit"""))
        if self.sip_ip:
            m = re.search('/32$', self.sip_ip)
            if m:
                pass
            elif len(IPNetwork(self.sip_ip)) == 1:
                self.sip_ip = str(self.sip_ip) + str('/32')
                # add name check no space ...


class ProviderEndpoint(TimeStampedModel):

    # Choices
    SIP_TRANSPORT_CHOICES = Choices(
        'udp',
        'tcp',
        'tls'
    )
    RTP_TRANSPORT_CHOICES = Choices(
        'RTP/AVP',
    )
    TOS_RTP_CHOICES = Choices(
        # reference : https://en.wikipedia.org/wiki/Type_of_service
        (0, '0 - CS0 - 0 Best effort'),
        (160, '160 - CS5 - 5 Critical'),
        (184, '184 - EF - 5 Critical'),
    )

    # Fields
    name = models.CharField(_(u"name"), max_length=64, unique=True)
    enabled = models.BooleanField(_(u"enabled / disabled"), default=True)
    register = models.BooleanField(_(u"register"), default=False)
    username = models.CharField(_(u"username"), blank=True, default='', max_length=35)
    password = models.CharField(_(u"password"), blank=True, default='', max_length=64)
    realm = models.CharField(_(u"realm"), max_length=64, blank=True, default="", help_text=_(u"Authentication realm. Same as gateway name, if blank."))
    from_domain = models.CharField(_(u"from domain"), max_length=50, blank=True, default="", help_text=_(u"Domain to use in from field. Same as realm if blank."))
    expire_seconds = models.PositiveIntegerField(_(u"expire seconds"), default=3600, null=True)
    retry_seconds = models.PositiveIntegerField(_(u"retry seconds"), default=30, null=True, help_text=_(u"How many seconds before a retry when a failure or timeout occurs"))
    max_calls = models.PositiveIntegerField(_(u'max calls'), default=30, help_text=_(u"max simultaneous calls allowed for this customer account."))
    calls_per_second = models.PositiveIntegerField(_(u'max calls per second'), default=10, help_text=_(u"maximum calls per second allowed for this gateway."))
    sip_proxy = models.CharField(_(u"proxy"), max_length=128, default="", help_text=_(u"IP if register is False."))
    sip_transport = models.CharField(_(u"SIP transport protocol"), max_length=15, default="udp", choices=SIP_TRANSPORT_CHOICES, help_text=_(u"Which transport to use for SIP messages"))
    sip_port = models.PositiveIntegerField(_(u"SIP port"), default="5060", help_text=_(u"Gateway SIP port - Default 5060 -."))
    rtp_transport = models.CharField(_(u"RTP transport protocol"), max_length=15, default="RTP/AVP", choices=RTP_TRANSPORT_CHOICES, help_text=_(u"Which transport protocol to use for RTP packets"))
    rtp_tos = models.PositiveIntegerField(_(u"TOS value for RTP streams"), default=184, choices=TOS_RTP_CHOICES, help_text=_(u"Which TOS value to use for RTP packets"))
    prefix = models.CharField(_(u'prefix'), blank=True, default='', max_length=15)
    suffix = models.CharField(_(u'suffix'), blank=True, default='', max_length=15)
    caller_id_in_from = models.BooleanField(_(u"caller ID in From field"), default=True, help_text=_(u"Use the callerid of an inbound call in the from field on outbound calls via this gateway."))
    add_plus_in_caller = models.BooleanField(_(u"add + in caller ID"), default=False, help_text=_(u"Add a + in front of the callerid number for outbound calls via this gateway."))
    pid = models.BooleanField(_(u"caller ID in PID field"), default=False, help_text=_(u"put callerid in SIP PID field if enabled"))
    pai = models.BooleanField(_(u"caller ID in PAI field"), default=False, help_text=_(u"put callerid in SIP P-Asserted-Id field if enabled"))
    ppi = models.BooleanField(_(u"caller ID in PPD field"), default=False, help_text=_(u"put callerid in SIP P-Preferred-Id field if enabled"))

    # Relationship Fields
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE, related_name="providers_p", verbose_name=_(u"Provider")
    )
    callerid_norm = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='calleridnormrules_p', null=True, blank=True, verbose_name=_(u"CallerID normalization rules for outbound call")
    )
    callee_norm = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='caleenormrules_p', null=True, blank=True, verbose_name=_(u"Destination number normalization rules for outbound call")
    )
    callerid_norm_in = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='calleridnormrulesin_p', null=True, blank=True, verbose_name=_(u"CallerID normalization rules for inbound call")
    )
    callee_norm_in = models.ForeignKey(
        NormalizationGrp,
        on_delete=models.CASCADE, related_name='caleenormrulesin_p', null=True, blank=True, verbose_name=_(u"Destination number normalization rules for inbound call")
    )
    codec_list = models.ManyToManyField(
        Codec, blank=True,
        related_name="codecs_p",
        help_text=_(u"if NULL, all available codecs are allowed")
    )
    uacreg = models.OneToOneField(
        UacReg,
        related_name="uac_reg",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_(u"Must be set if registration is needed")
    )

    class Meta:
        db_table = 'pyfb_endpoint_provider'
        ordering = ('provider', 'name')
        verbose_name = _(u'provider endpoint')
        verbose_name_plural = _(u'provider endpoints')
        indexes = [
            PartialIndex(fields=['name', 'callerid_norm'], unique=True, where_postgresql='enabled = True'),
            PartialIndex(fields=['name', 'callee_norm'], unique=True, where_postgresql='enabled = True'),
            PartialIndex(fields=['name', 'callerid_norm_in'], unique=True, where_postgresql='enabled = True'),
            PartialIndex(fields=['name', 'callee_norm_in'], unique=True, where_postgresql='enabled = True'),
        ]

    def __str__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('pyfb-endpoint:pyfb_endpoint_providerendpoint_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('pyfb-endpoint:pyfb_endpoint_providerendpoint_update', args=(self.pk,))

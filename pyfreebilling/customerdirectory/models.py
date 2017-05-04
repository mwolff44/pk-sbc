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
from django.db import models
from django.utils.translation import ugettext_lazy as _

from netaddr import IPNetwork
import re

from pyfreebilling.pyfreebill.models import Company
from pyfreebilling.pyfreebill.validators import validate_cidr

from pyfreebilling.normalizationrule.models import NormalizationGroup

from pyfreebilling.switch.models import Domain


class Subscriber(models.Model):
    """ Subscriber table for Kam """
    id = models.AutoField(auto_created=True, primary_key=True)
    username = models.CharField(max_length=64)
    # domain = models.CharField(max_length=64, blank=True)
    password = models.CharField(max_length=25, blank=True)
    # email_address = models.CharField(max_length=64, blank=True)
    # ha1 = models.CharField(max_length=64, blank=True)
    # ha1b = models.CharField(max_length=64, blank=True)
    #rpid = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "subscriber"
        app_label = "customerdirectory"
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        pass

# CREATE OR REPLACE VIEW subscriber AS
#     SELECT row_number() OVER () AS id,
#         c.name AS username,
##         c.domain,
#         c.password,
##         md5(username:realm:password) AS ha1,
##         md5(username@domain:realm:password) AS ha1b
#     FROM customer_directory c WHERE c.enabled=True and c.registration=True


class CustomerDirectory(models.Model):
    """ Customer Directory Model """
    company = models.ForeignKey(Company,
                                verbose_name=_(u"company"))
    registration = models.BooleanField(_(u"Registration"),
                                       default=False,
                                       help_text=_(u"""Is registration needed
                                       for calling ? True, the phone needs to
                                       register with correct username/password.
                                       If false, you must specify a CIDR in SIP
                                       IP CIDR !"""))
    password = models.CharField(_(u"password"),
                                max_length=100,
                                blank=True,
                                help_text=_(u"""It's recommended to use strong
                                passwords for the endpoint."""))
    description = models.TextField(_(u'description'),
                                   blank=True)
    name = models.CharField(_(u"SIP username"),
                            max_length=50,
                            unique=True,
                            help_text=_(u"Ex.: customer SIP username, etc..."))
    domain = models.ForeignKey(
        Domain,
        verbose_name=_(u"SIP domain"),
        help_text=_(u"""A sip account must belong to a domain.
            This domain must be used in SIP message"""))
    rtp_ip = models.CharField(_(u"RTP IP CIDR"),
                              max_length=100,
                              default="auto",
                              help_text=_(u"""Internal IP address/mask to bind
                              to for RTP. Format : CIDR Ex. 192.168.1.0/32"""))
    sip_ip = models.CharField(_(u"SIP IP CIDR"),
                              max_length=100,
                              null=True,
                              blank=True,
                              validators=[validate_cidr],
                              help_text=_(u"""Internal IP address/mask to bind
                              to for SIP. Format : CIDR. Ex. 192.168.1.0/32
                              """))
    sip_port = models.PositiveIntegerField(_(u"SIP port"),
                                           default=5060)
    max_calls = models.PositiveIntegerField(_(u'max calls'),
                                            default=1,
                                            help_text=_(u"""max simultaneous
                                            calls allowed for this customer
                                            account."""))
    calls_per_second = models.PositiveIntegerField(_(u'max calls per second'),
                                                   default=10,
                                                   help_text=_(u"""maximum
                                                   calls per second allowed for
                                                   this customer account."""))
    log_auth_failures = models.BooleanField(_(u"log auth failures"),
                                            default=False,
                                            help_text=_(u"""It true, the server
                                            will log authentication failures.
                                            Required for Fail2ban."""))
    MULTIPLE_CODECS_CHOICES = (
        ("PCMA,PCMU,G729", _(u"PCMA,PCMU,G729")),
        ("PCMU,PCMA,G729", _(u"PCMU,PCMA,G729")),
        ("G729,PCMA,PCMU", _(u"G729,PCMA,PCMU")),
        ("G729,PCMU,PCMA", _(u"G729,PCMU,PCMA")),
        ("PCMA,G729", _(u"PCMA,G729")),
        ("PCMU,G729", _(u"PCMU,G729")),
        ("G729,PCMA", _(u"G729,PCMA")),
        ("G729,PCMU", _(u"G729,PCMU")),
        ("PCMA,PCMU", _(u"PCMA,PCMU")),
        ("PCMU,PCMA", _(u"PCMU,PCMA")),
        ("G722,PCMA,PCMU", _(u"G722,PCMA,PCMU")),
        ("G722,PCMU,PCMA", _(u"G722,PCMU,PCMA")),
        ("G722", _(u"G722")),
        ("G729", _(u"G729")),
        ("PCMU", _(u"PCMU")),
        ("PCMA", _(u"PCMA")),
        ("ALL", _(u"ALL")),
    )
    codecs = models.CharField(_(u"Codecs"),
                              max_length=100,
                              default="ALL",
                              choices=MULTIPLE_CODECS_CHOICES,
                              help_text=_(u"""Codecs allowed - beware about
                              order, 1st has high priority """))
    MULTIPLE_REG_CHOICES = (
        ("call-id", _(u"Call-id")),
        ("contact", _(u"Contact")),
        ("false", _(u"False")),
        ("true", _(u"True")))
    multiple_registrations = models.CharField(_(u"multiple registrations"),
                                              max_length=100,
                                              default="false",
                                              choices=MULTIPLE_REG_CHOICES,
                                              help_text=_(u"""Used to allow to
                                              call one extension and ring
                                              several phones."""))
    outbound_caller_id_name = models.CharField(_(u"CallerID name"),
                                               max_length=50,
                                               blank=True,
                                               help_text=_(u"""Caller ID name
                                               sent to provider on outbound
                                               calls."""))
    outbound_caller_id_number = models.CharField(_(u"""CallerID
                                                   num"""),
                                                 max_length=80,
                                                 blank=True,
                                                 help_text=_(u"""Caller ID
                                                 number sent to provider on
                                                 outbound calls."""))
    callerid_norm = models.ForeignKey(
        NormalizationGroup,
        related_name='calleridnormrules',
        null=True,
        blank=True,
        verbose_name=_(u"CallerID normalization rules for outbound call"))
    callee_norm = models.ForeignKey(
        NormalizationGroup,
        related_name='caleenormrules',
        null=True,
        blank=True,
        verbose_name=_(u"Destination number normalization rules for outbound call"))
    callerid_norm_in = models.ForeignKey(
        NormalizationGroup,
        related_name='calleridnormrulesin',
        null=True,
        blank=True,
        verbose_name=_(u"CallerID normalization rules for inbound call"))
    callee_norm_in = models.ForeignKey(
        NormalizationGroup,
        related_name='caleenormrulesin',
        null=True,
        blank=True,
        verbose_name=_(u"Destination number normalization rules for inbound call"))
    force_caller_id = models.BooleanField(
        _(u"Force callerID"),
        default=False)
    masq_caller_id = models.BooleanField(
        _(u"Masq callerID"),
        default=False)
    urgency_numbr = models.BooleanField(
        _(u"Allow urgency numbers"),
        default=True,
        help_text=_(u"""You have also to allow global routing option
          and define an urgency ratecard"""))
    insee_code = models.PositiveIntegerField(
        _(u'Special code for routing urgency numbers'),
        null=True,
        blank=True,
        help_text=_(u"""Postal code, INSEE code ... for routing
          urgency number to the right urgency call center."""))
    IEM_CHOICES = (
        ("false", _(u"false")),
        ("true", _(u"true")),
        ("ring_ready", _(u"ring_ready")))
    ignore_early_media = models.CharField(_(u"Ignore early media"),
                                          max_length=20,
                                          default="false",
                                          choices=IEM_CHOICES,
                                          help_text=_(u"""Controls if the call
                                                      returns on early media
                                                      or not. Default is false.
                                                      Setting the value to
                                                      "ring_ready" will work
                                                      the same as
                                                      ignore_early_media=true
                                                      but also send a SIP 180
                                                      to the inbound leg when
                                                      the first SIP 183 is
                                                      caught.
                                                      """))
    enabled = models.BooleanField(_(u"Enabled / Disabled"),
                                  default=True)
    fake_ring = models.BooleanField(_(u"Fake ring"),
                                    default=False,
                                    help_text=_(u"""Fake ring : Enabled /
                                    Disabled - Send a fake ring to the
                                    caller."""))
    cli_debug = models.BooleanField(_(u"CLI debug"),
                                    default=False,
                                    help_text=_(u"""CLI debug : Enabled /
                                    Disabled - Permit to see all debug
                                    messages on cli."""))
    vmd = models.BooleanField(_(u"Voicemail detection : Enabled / Disabled"),
                              default=False,
                              help_text=_(u"""Be carefull with this option, as
                              it takes a lot of ressources !."""))
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'customer_directory'
        app_label = 'customerdirectory'
        ordering = ('company', 'name')
        verbose_name = _(u'Customer sip account')
        verbose_name_plural = _(u'Customer sip accounts')

    def __unicode__(self):
        return "%s (%s:%s)" % (self.name, self.sip_ip, self.sip_port)

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

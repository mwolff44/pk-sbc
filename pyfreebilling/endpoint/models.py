# Copyright 2018 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.core.urlresolvers import reverse
from django.db import models as models
from django.db.models import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django_extensions.db import fields as extension_fields
from django_extensions.db.fields import AutoSlugField


class UacReg(models.Model):

    # Fields
    l_uuid = models.CharField(max_length=64, default="", db_index=True, help_text=_(u"Local unique id used to build and match contact addresses."))
    l_username = models.CharField(max_length=64, default="", help_text=_(u"Local username"))
    l_domain = models.CharField(max_length=64, default="", help_text=_(u"Local domain"))
    r_username = models.CharField(max_length=64, default="", help_text=_(u"Remote username"))
    r_domain = models.CharField(max_length=64, default="", help_text=_(u"Remote domain"))
    realm = models.CharField(max_length=64, default="", help_text=_(u"realm"))
    auth_username = models.CharField(max_length=64, default="", help_text=_(u"Auth username"))
    auth_password = models.CharField(max_length=64, default="", help_text=_(u"Auth password"))
    auth_ha1 = models.CharField(max_length=128, default="", help_text=_(u"Hashed (HA1) auth password"))
    auth_proxy = models.CharField(max_length=128, default="", help_text=_(u"Outbound proxy SIP address"))
    expires = models.IntegerField(default=0, help_text=_(u"Expiration time in seconds, 0 means disabled"))
    flags = models.IntegerField(default=0, help_text=_(u"Flags to control the behaviour"))
    reg_delay = models.IntegerField(default=0, help_text=_(u"initial registration delay"))


    class Meta:
        db_table = 'uacreg'
        app_label = 'endpoint'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('endpoint_uacreg_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('endpoint_uacreg_update', args=(self.pk,))


class Trusted(models.Model):

    # Choices
    PROTO_CHOICES = (
        ('any', 'any'),
        ('udp', 'udp'),
        ('tcp', 'tcp'),
        ('tls', 'tls'),
        ('sctp', 'sctp'),
    )

    # Fields
    src_ip = models.CharField(max_length=50, db_index=True, default="", help_text=_(u"Source address is equal to source address of request"))
    proto = models.CharField(max_length=4, choices=PROTO_CHOICES, default="any", help_text=_(u"Transport protocol is either any or equal to transport protocol of request"))
    from_pattern = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Regular expression matches From URI of request."))
    ruri_pattern = models.CharField(max_length=64, null=True, blank=True, help_text=_(u"Regular expression matches Request URI of request."))
    tag = models.CharField(max_length=64, default="", help_text=_(u"Tag"))
    priority = models.IntegerField(default=0, help_text=_(u"Priority of rule"))


    class Meta:
        db_table = 'trusted'
        app_label = 'endpoint'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('endpoint_trusted_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('endpoint_trusted_update', args=(self.pk,))

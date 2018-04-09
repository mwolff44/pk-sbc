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

class Version(models.Model):

    # Fields
    table_name = CharField(max_length=32, unique=True)
    table_version = IntegerField(default=0)


    class Meta:
        db_table = 'version'
        app_label = 'kamailio'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_version_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_version_update', args=(self.pk,))


class Location(models.Model):

    # Fields
    ruid = CharField(max_length=64, default='', unique=True, help_text=_(u"Record internal unique id"))
    username = CharField(max_length=64, default='', help_text=_(u"Username / phone number"))
    domain = CharField(max_length=64, null=True, blank=True, help_text=_(u"Doamin name"))
    contact = CharField(max_length=512, default='', help_text=_(u"Contact header field value provides a URI whoses meaning depends on the type of request or response it is in."))
    received = CharField(max_length=128, null=True, blank=True, help_text=_(u"Received IP:PORT in the format SIP:IP:PORT"))
    path = CharField(max_length=512, null=True, blank=True, help_text=_(u"Path Header(s) per RFC 3327"))
    expires = DateTimeField(default='2030-05-28 21:32:15', db_index=True, help_text=_(u"Date and time when this entry expires."))
    q = DecimalField(max_digits=10, decimal_places=2, default=1.0, help_text=_(u"Value used for preferential routing."))
    callid = CharField(max_length=255, default='Default-Call-ID', help_text=_(u"	 Call-ID header field uniquely identifies a particular invitation or all registrations of a particular client."))
    cseq = IntegerField(default=1, help_text=_(u"CSeq header field contains a single decimal sequence number and the request method."))
    last_modified = DateTimeField(default='2000-01-01 00:00:01', help_text=_(u"Date and time when this entry was last modified"))
    flags = IntegerField(default=0, help_text=_(u"Internal flags"))
    cflags = IntegerField(default=0, help_text=_(u"Branch and contact flags"))
    user_agent = CharField(max_length=255, default='', help_text=_(u"User-Agent header field contains information about the UAC originating the request."))
    socket = CharField(max_length=64, null=True, blank=True, help_text=_(u"Socket used to connect to Kamailio. For example: UDP:IP:PORT"))
    methods = IntegerField(null=True, blank=True, help_text=_(u"Flags that indicate the SIP Methods this contact will accept."))
    instance = CharField(max_length=255, null=True, blank=True, help_text=_(u"The value of SIP instance parameter for GRUU."))
    reg_id = IntegerField(default=0, help_text=_(u"The value of reg-id contact parameter"))
    server_id = IntegerField(default=0, help_text=_(u"The value of server_id from configuration file"))
    connection_id = IntegerField(default=0, help_text=_(u"The value of connection id for location record"))
    keepalive = IntegerField(default=0, help_text=_(u"The value to control sending keep alive requests"))
    partition = IntegerField(default=0, help_text=_(u"The value to of the partition for keep alive requests"))


    class Meta:
        db_table = 'location'
        app_label = 'kamailio'
        ordering = ('-pk',)
        verbose_name = _(u"user location")
        indexes = [
            models.Index(fields=['username', 'domain', 'contact']),
            models.Index(fields=['server_id', 'connection_id']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_location_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_location_update', args=(self.pk,))


class LocationAttrs(models.Model):

    # Fields
    ruid = CharField(max_length=64, default='', help_text=_(u"Record internal unique id"))
    username = CharField(max_length=64, default='', help_text=_(u"Username / phone number"))
    domain = CharField(max_length=64, null=True, blank=True, help_text=_(u"Domain name"))
    aname = CharField(max_length=64, default='', help_text=_(u"Attribute name"))
    atype = IntegerField(default=0, help_text=_(u"Attribute type"))
    avalue = CharField(max_length=255, default='', help_text=_(u"Attribute value"))
    last_modified = DateTimeField(default='2000-01-01 00:00:01', db_index=True, help_text=_(u"Date and time when this entry was last modified"))


    class Meta:
        db_table = 'location_attrs'
        app_label = 'kamailio'
        ordering = ('-pk',)
        indexes = [
            models.Index(fields=['username', 'domain', 'ruid']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_locationattrs_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_locationattrs_update', args=(self.pk,))


class UserBlackList(models.Model):
    # Choices
    WHITELIST_CHOICES = (
        ('0', 'blacklist'),
        ('1', 'whitelist'),
    )
    # Fields
    username = CharField(max_length=64, default='', help_text=_(u"The user that is used for the blacklist lookup"))
    domain = CharField(max_length=64, default='', help_text=_(u"The domain that is used for the blacklist lookup"))
    prefix = CharField(max_length=64, default='', help_text=_(u"The prefix that is matched for the blacklist"))
    whitelist = CharField(
        max_length=1,
        choices=WHITELIST_CHOICES,
        default='0',
        help_text=_(u"Specify if this a blacklist (0) or a whitelist (1) entry")
    )


    class Meta:
        db_table = 'userblacklist'
        app_label = 'kamailio'
        ordering = ('-pk',)
        indexes = [
            models.Index(fields=['username', 'domain', 'prefix']),
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_userblacklist_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_userblacklist_update', args=(self.pk,))


class GlobalBlackList(models.Model):
    # Choices
    WHITELIST_CHOICES = (
        ('0', 'blacklist'),
        ('1', 'whitelist'),
    )
    # Fields
    prefix = CharField(max_length=64, default='', db_index=True, help_text=_(u"The prefix that is matched for the blacklist"))
    whitelist = CharField(
        max_length=1,
        choices=WHITELIST_CHOICES,
        default='0',
        help_text=_(u"Specify if this a blacklist (0) or a whitelist (1) entry")
    )
    description = TextField(max_length=255, default='', help_text=_(u"A comment for the entry"))


    class Meta:
        db_table = 'globalblacklist'
        app_label = 'kamailio'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_globalblacklist_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_globalblacklist_update', args=(self.pk,))


class SpeedDial(models.Model):

    # Fields
    username = CharField(max_length=64, default='', help_text=_(u"Username / phone number"))
    domain = CharField(max_length=64, default='', help_text=_(u"Domain name"))
    sd_username = CharField(max_length=64, default='', help_text=_(u"Speed dial username"))
    sd_domain = CharField(max_length=64, default='', help_text=_(u"Speed dial domain"))
    new_uri = CharField(max_length=128, default='', help_text=_(u"New URI"))
    fname = CharField(max_length=64, default='', help_text=_(u"First name"))
    lname = CharField(max_length=64, default='', help_text=_(u"Last name"))
    description = CharField(max_length=64, default='', help_text=_(u"Description"))


    class Meta:
        db_table = 'speed_dial'
        app_label = 'kamailio'
        ordering = ('-pk',)
        unique_together = [
            ["username", "domain", "sd_domain", "sd_username"],
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_speeddial_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_speeddial_update', args=(self.pk,))


class PipeLimit(models.Model):
    # choices
    ALGO_CHOICES = (
        ('NOP', 'NOP'),
        ('RED', 'RED'),
        ('TAILDROP', 'TAILDROP'),
        ('FEEDBACK', 'FEEDBACK'),
        ('NETWORK', 'NETWORK'),
    )
    # Fields
    pipeid = CharField(max_length=64, default='', help_text=_(u"Unique ID for pipe"))
    algorithm = CharField(
        max_length=32,
        choices=ALGO_CHOICES,
        default='TAILDROP',
        help_text=_(u"Algorithm to be used for pipe limits. See the readme of the module for description of available options: NOP, RED, TAILDROP, FEEDBACK, NETWORK"))
    plimit = IntegerField(default=0, help_text=_(u"Pipe limit (hits per second)"))


    class Meta:
        db_table = 'pl_pipes'
        app_label = 'kamailio'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_pipelimit_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_pipelimit_update', args=(self.pk,))


class Mtree(models.Model):

    # Fields
    tprefix = CharField(max_length=32, default='', unique=True, help_text=_(u"Key to be used to index the values in the tree, usually a DID or prefix"))
    tvalue = CharField(max_length=128, default='', help_text=_(u"The value of the key"))


    class Meta:
        db_table = 'mtree'
        app_label = 'kamailio'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_mtree_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_mtree_update', args=(self.pk,))


class Mtrees(models.Model):

    # Fields
    tname = CharField(max_length=128, default='', help_text=_(u"Name of shared memory tree"))
    tprefix = CharField(max_length=32, default='', help_text=_(u"Key to be used to index the values in the tree, usually a DID or prefix"))
    tvalue = CharField(max_length=128, default='', help_text=_(u"The value of the key"))


    class Meta:
        db_table = 'mtrees'
        app_label = 'kamailio'
        ordering = ('-pk',)
        unique_together = [
            ["tname", "tprefix", "tvalue"],
        ]

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_mtrees_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_mtrees_update', args=(self.pk,))


class Htable(models.Model):

    # Fields
    key_name = CharField(max_length=64, default='', help_text=_(u"Name of the hash key"))
    key_type = IntegerField(default=0, help_text=_(u"Type of the key"))
    value_type = IntegerField(default=0, help_text=_(u"Type of the value"))
    key_value = CharField(max_length=128, default='', help_text=_(u"The value of the key"))
    expires = IntegerField(default=0, help_text=_(u"The epoch at which the key expires"))


    class Meta:
        db_table = 'htable'
        app_label = 'kamailio'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('kamailio_htable_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('kamailio_htable_update', args=(self.pk,))

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


class Acc(models.Model):

    # Fields
    method = CharField(max_length=16, default='', help_text=_(u"A method is the primary function that a request is meant to invoke on a server."))
    from_tag = CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    to_tag = CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    callid = CharField(max_length=255, default='', db_index=True, help_text=_(u"Call-ID header field uniquely identifies a particular invitation or all registrations of a particular client."))
    sip_code = CharField(max_length=3, default='', help_text=_(u"SIP reply code."))
    sip_reason = CharField(max_length=128, default='', help_text=_(u"SIP reply reason"))
    time = DateTimeField(help_text=_(u"Date and time when this record was written."))
    time_attr = models.IntegerField(help_text=_(u"Unix timestamp"))
    time_exten = models.IntegerField(help_text=_(u"extended value related to the time of event"))


    class Meta:
        db_table = 'acc'
        app_label = 'accounting'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('accounting_acc_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('accounting_acc_update', args=(self.pk,))


class AccCdr(models.Model):

    # Fields
    start_time = DateTimeField(default='2000-01-01 00:00:00', db_index=True, help_text=_(u"Start date and time"))
    end_time = DateTimeField(default='2000-01-01 00:00:00', help_text=_(u"End date and time"))
    duration = DecimalField(max_digits=10, decimal_places=3, default=0, help_text=_(u"Duration"))


    class Meta:
        db_table = 'acc_cdrs'
        app_label = 'accounting'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('accounting_acccdr_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('accounting_acccdr_update', args=(self.pk,))


class MissedCall(models.Model):

    # Fields
    method = CharField(max_length=16, default='', help_text=_(u"A method is the primary function that a request is meant to invoke on a server."))
    from_tag = CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    to_tag = CharField(max_length=64, default='', help_text=_(u"The tag parameter serves as a general mechanism to identify a dialog, which is the combination of the Call-ID along with two tags, one from participant in the dialog."))
    callid = CharField(max_length=255, default='', db_index=True, help_text=_(u"Call-ID header field uniquely identifies a particular invitation or all registrations of a particular client."))
    sip_code = CharField(max_length=3, default='', help_text=_(u"SIP reply code."))
    sip_reason = CharField(max_length=128, default='', help_text=_(u"SIP reply reason"))
    time = DateTimeField(help_text=_(u"Date and time when this record was written."))


    class Meta:
        db_table = 'missed_calls'
        app_label = 'accounting'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def get_absolute_url(self):
        return reverse('accounting_missedcall_detail', args=(self.pk,))


    def get_update_url(self):
        return reverse('accounting_missedcall_update', args=(self.pk,))

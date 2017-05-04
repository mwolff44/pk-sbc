# -*- coding: utf-8 -*-
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

from django.db import models
from django.utils.translation import ugettext_lazy as _

# VOIP SWITCH


class Domain(models.Model):
    """
    Domain management
    """

    domain = models.CharField(
        _(u"Domain"),
        max_length=64,
        help_text=_(u"SIP domain"))
    did = models.CharField(
        _(u"Domain identifier"),
        max_length=64,
        help_text=_(u"Unique identifier for the domain."))
    FLAG_LIST = (
        (0, _(u'Default')),
        (1, _(u'Disabled')),
        (2, _(u'Canonical')),
        (3, _(u'Allowed_to')),
        (4, _(u'Allowed_From')),
        (5, _(u'For_serweb')),
        (6, _(u'Pending')),
        (7, _(u'Deleted')),
        (8, _(u'Caller_deleted')),
        (9, _(u'Calle_deleted')),
    )
    flags = models.IntegerField(
        _(u"flags"),
        default="0",
        choices=FLAG_LIST,
        help_text=_(u"Kamailio flags."))
    date_added = models.DateTimeField(
        _(u'date added'),
        auto_now_add=True)
    date_modified = models.DateTimeField(
        _(u'date modified'),
        auto_now=True)

    class Meta:
        db_table = 'uid_domain'
        app_label = 'switch'
        ordering = ('domain', )
        verbose_name = _(u'SIP domain')
        verbose_name_plural = _(u'SIP domains')

    def __unicode__(self):
        return u"%s" % (self.domain)

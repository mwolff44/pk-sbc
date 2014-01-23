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
from django.core import urlresolvers


class ContractDid(models.Model):
    """
    link between did and customer
    TODO :
     - tarif plan
     - destination (inlines, as we need many level for failover purpose)
    """
    did = models.ForeignKey('did.Did', unique=True)
    customer = models.ForeignKey('pyfreebill.Company',
                                 verbose_name=_(u"company"),
                                 limit_choices_to={'customer_enabled': True})
    max_channels = models.PositiveIntegerField(_(u'max calls'),
                                               default=1,
                                               help_text=_(u"""maximum
                    simultaneous calls allowed for this did."""))
    description = models.TextField(_(u'description'),
                                   blank=True)
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'did_contract'
        app_label = 'did'
        ordering = ('did', )
        verbose_name = _(u'DID contract')
        verbose_name_plural = _(u'DID contracts')

    def __unicode__(self):
        return u"%s (:%s)" % (self.did, self.customer)

    def get_admin_url(self):
        return urlresolvers.reverse("admin:%s_%s_change" %
            (self._meta.app_label, self._meta.module_name), args=(self.id,))

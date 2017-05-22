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

#from pyfreebilling.pyfreebill.models import Ratecard, Providertariff


class Did(models.Model):
    """
    DID model
    """
    number = models.CharField(_(u'DID number'),
                              max_length=30,
                              db_index=True,
                              unique=True)
    provider = models.ForeignKey(
        'pyfreebill.Company',
        on_delete=models.CASCADE,
        related_name='didprovider',
        verbose_name=_(u"Provider"),
        limit_choices_to={'supplier_enabled': True})
    prov_ratecard = models.ForeignKey(
        'pyfreebill.Providertariff',
        on_delete=models.CASCADE,
        verbose_name=_(u"provider rate plan"),
        null=True,
        blank=True,
        limit_choices_to={'enabled': True})
    prov_max_channels = models.PositiveIntegerField(
        _(u'provider channels'),
        default=0,
        help_text=_(u"""maximum simultaneous calls allowed
            for this did. 0 means no limit"""))
    customer = models.ForeignKey(
        'pyfreebill.Company',
        on_delete=models.SET_NULL,
        related_name='didcustomer',
        verbose_name=_(u"Customer"),
        null=True,
        blank=True,
        limit_choices_to={'customer_enabled': True})
    cust_ratecard = models.ForeignKey(
        'pyfreebill.ratecard',
        on_delete=models.SET_NULL,
        verbose_name=_(u"Customer rate plan"),
        null=True,
        blank=True,
        limit_choices_to={'enabled': True, 'rctype': 'DIDIN'})
    cust_max_channels = models.PositiveIntegerField(
        _(u'customer channels'),
        default=0,
        null=True,
        blank=True,
        help_text=_(u"""maximum simultaneous calls allowed
            for this did. 0 means no limit"""))
    insee_code = models.CharField(
        _(u'Special code for routing urgency numbers'),
        null=True,
        blank=True,
        max_length=10,
        help_text=_(u"""Postal code, INSEE code ... for routing
          urgency number to the right urgency call center."""))
    description = models.TextField(_(u'description'),
                                   blank=True)
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'did'
        app_label = 'did'
        ordering = ('number', )
        verbose_name = _(u'DID')
        verbose_name_plural = _(u'DIDs')

    def __unicode__(self):
        return u"%s (:%s)" % (self.number, self.provider)

# Create your tests here.
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


class ProviderRatesDid(models.Model):
    """ Provider Rates Model for Did"""
    name = models.CharField(_(u'name'), max_length=128)
    rate = models.DecimalField(_(u'Rate'),
                               max_digits=11,
                               decimal_places=5)
    block_min_duration = models.IntegerField(_(u'block min duration'),
                                             default=1)
    interval_duration = models.IntegerField(_(u'Interval duration'),
                                            default=1)
    provider = models.ForeignKey(
        'pyfreebill.Company',
        on_delete=models.CASCADE,
        verbose_name=_(u"provider"),
        limit_choices_to={'supplier_enabled': True})
    enabled = models.BooleanField(_(u"Enabled / Disabled"),
                                  default=True)
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'provider_rates_did'
        app_label = 'did'
        ordering = ('provider', 'name')
        unique_together = ("name", "provider")
        verbose_name = _(u'DID provider rate')
        verbose_name_plural = _(u'DID provider rates')

    def __unicode__(self):
        return u"n: %s -r: %s : %s/%s - " % (self.name,
                                             self.rate,
                                             self.block_min_duration,
                                             self.interval_duration)


class CustomerRatesDid(models.Model):
    """ Customer Rates Model for Did"""
    name = models.CharField(_(u'name'), max_length=128)
    rate = models.DecimalField(_(u'Rate'),
                               max_digits=11,
                               decimal_places=5)
    block_min_duration = models.IntegerField(_(u'block min duration'),
                                             default=1)
    interval_duration = models.IntegerField(_(u'Interval duration'),
                                            default=1)
    enabled = models.BooleanField(_(u"Enabled / Disabled"),
                                  default=True)
    date_added = models.DateTimeField(_(u'date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'customer_rates_did'
        app_label = 'did'
        ordering = ('name',)
        verbose_name = _(u'DID customer rate')
        verbose_name_plural = _(u'DID customer rates')

    def __unicode__(self):
        return u"%s -r: %s : %s/%s" % (self.name,
                                       self.rate,
                                       self.block_min_duration,
                                       self.interval_duration)

# Copyright 2017 Mathias WOLFF
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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from pyfreebilling.customerdirectory.models import CustomerDirectory
from pyfreebilling.pyfreebill.models import Company


class Fraud(models.Model):
    """Fraud model."""
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        limit_choices_to={'customer_enabled': True},
        blank=True,
        null=True)
    customerdirectory = models.OneToOneField(
        CustomerDirectory,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    # Fraud based on amount
    amount_fraud = models.BooleanField(
        _(u"Activate amount fraud system"),
        default=False,
        help_text=_(u"If checked, this account will be protected by threshold fraud system by checking daily consumption."))
    amount_limit_alert = models.DecimalField(
        _(u'Amount - alert'),
        max_digits=12,
        decimal_places=4,
        default=0,
        help_text=_(u"Daily consumption allowed before alerting."))
    amount_block_alert = models.DecimalField(
        _(u'Amount - block'),
        max_digits=12,
        decimal_places=4,
        default=0,
        help_text=_(u"Daily consumption allowed before blocking."))
    high_amount_alert_sent = models.BooleanField(
        _(u"Fraud alert ON (based on daily consumption)"),
        default=False)
    # Fraud based on minutes
    minutes_fraud = models.BooleanField(
        _(u"Activate minutes fraud system"),
        default=False,
        help_text=_(u"If checked, this account will be protected by threshold fraud system by checking daily minutes consumption."))
    minutes_limit_alert = models.IntegerField(
        _(u'Nb minutes - alert'),
        default=0,
        help_text=_(u"Daily minutes consumption allowed before alerting."))
    minutes_block_alert = models.IntegerField(
        _(u'Nb minutes - Block'),
        default=0,
        help_text=_(u"Daily minutes consumption allowed before blocking."))
    high_minutes_alert_sent = models.BooleanField(
        _(u"Fraud alert ON (based on daily minutes consumption)"),
        default=False)
    # General settings
    account_blocked_alert_sent = models.BooleanField(
        _(u"Account blocked - Fraud alert ON"),
        default=False)
    date_added = models.DateTimeField(_('date added'),
                                      auto_now_add=True)
    date_modified = models.DateTimeField(_(u'date modified'),
                                         auto_now=True)

    class Meta:
        db_table = 'fraud_alert'
        app_label = 'antifraud'
        verbose_name = _(u'antifraud')
        verbose_name_plural = _(u'antifraud')

    def __unicode__(self):
        return self.id

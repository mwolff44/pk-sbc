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

from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _

import decimal
import math
import qsstats

from pyfreebilling.pyfreebill.models import Company, SofiaGateway, RateCard, LCRGroup

from pyfreebilling.customerdirectory.models import CustomerDirectory


class CDR(models.Model):
    """ CDR Model    """
    customer = models.ForeignKey(
        Company,
        verbose_name=_(u"customer"),
        null=True,
        related_name="customer_related")
    customer_ip = models.CharField(
        _(u"customer IP address"),
        max_length=100,
        null=True,
        help_text=_(u"Customer IP address."))
    uuid = models.CharField(
        _(u"UUID"),
        max_length=100,
        null=True)
    bleg_uuid = models.CharField(
        _(u"b leg UUID"),
        null=True,
        default="",
        max_length=100)
    kam_uuid = models.CharField(
        _(u"SIP Server unique call-ID"),
        max_length=100,
        null=True)
    caller_id_number = models.CharField(
        _(u"caller ID num"),
        max_length=100,
        null=True)
    destination_number = models.CharField(
        _(u"Dest. number"),
        max_length=100,
        null=True)
    chan_name = models.CharField(
        _(u"channel name"),
        max_length=100,
        null=True)
    start_stamp = models.DateTimeField(
        _(u"start time"),
        null=True,
        db_index=True)
    answered_stamp = models.DateTimeField(
        _(u"answered time"),
        null=True)
    end_stamp = models.DateTimeField(
        _(u"hangup time"),
        null=True)
    duration = models.IntegerField(
        _(u"global duration"),
        null=True)
    effectiv_duration = models.IntegerField(
        _(u"total duration"),
        null=True,
        help_text=_(
            u"Global call duration since call has been received by the switch in ms."))
    effective_duration = models.IntegerField(
        _(u"effective duration"),
        null=True,
        help_text=_(u"real call duration in s."))
    billsec = models.IntegerField(
        _(u"billed duration"),
        null=True,
        help_text=_(u"billed call duration in s."))
    read_codec = models.CharField(
        _(u"read codec"),
        max_length=20,
        null=True)
    write_codec = models.CharField(
        _(u"write codec"),
        max_length=20,
        null=True)
    hangup_cause = models.CharField(
        _(u"hangup cause"),
        max_length=50,
        null=True,
        db_index=True)
    hangup_cause_q850 = models.IntegerField(
        _(u"q.850"),
        null=True)
    gateway = models.ForeignKey(
        SofiaGateway,
        verbose_name=_(u"gateway"),
        null=True)
    cost_rate = models.DecimalField(
        _(u'buy rate'),
        max_digits=11,
        decimal_places=5,
        default="0",
        null=True)
    total_sell = models.DecimalField(
        _(u'total sell'),
        max_digits=11,
        decimal_places=5,
        default="0",
        null=True)
    total_cost = models.DecimalField(
        _(u'total cost'),
        max_digits=11,
        decimal_places=5,
        default="0",
        null=True)
    prefix = models.CharField(
        _(u'Prefix'),
        max_length=30,
        null=True)
    country = models.CharField(
        _(u'Country'),
        max_length=100,
        null=True)
    rate = models.DecimalField(
        _(u'sell rate'),
        max_digits=11,
        decimal_places=5,
        null=True)
    init_block = models.DecimalField(
        _(u'Connection fee'),
        max_digits=11,
        decimal_places=5,
        null=True)
    block_min_duration = models.IntegerField(
        _(u'increment'),
        null=True)
    lcr_carrier_id = models.ForeignKey(
        Company,
        verbose_name=_(u"provider"),
        null=True,
        related_name="carrier_related")
    ratecard_id = models.ForeignKey(
        RateCard,
        null=True,
        verbose_name=_(u"ratecard"))
    lcr_group_id = models.ForeignKey(
        LCRGroup,
        null=True,
        verbose_name=_(u"lcr group"))
    sip_charge_info = models.CharField(
        _(u'charge info'),
        null=True,
        max_length=100,
        help_text=_(u"Contents of the P-Charge-Info header for billing purpose."))
    sip_user_agent = models.CharField(
        _(u'sip user agent'),
        null=True,
        max_length=100)
    sip_rtp_rxstat = models.CharField(
        _(u'sip rtp rx stat'),
        null=True,
        max_length=30)
    sip_rtp_txstat = models.CharField(
        _(u'sip rtp tx stat'),
        null=True,
        max_length=30)
    switchname = models.CharField(
        _(u"Media server name"),
        null=True,
        default="",
        max_length=100)
    sipserver_name = models.CharField(
        _(u"FSIP server name"),
        null=True,
        default="",
        max_length=100)
    switch_ipv4 = models.CharField(
        _(u"switch ipv4"),
        null=True,
        default="",
        max_length=100)
    hangup_disposition = models.CharField(
        _(u"hangup disposition"),
        null=True,
        default="",
        max_length=100,
        help_text=_(
            u"""Interpretation of these values differs on incoming and
            outgoing calls since FreeSWITCH is at different ends of the
            session.

            <b>Incoming :</b>
            send_bye    FS sent BYE to the caller (we hung up)
            recv_bye    FS received BYE from the caller (they hung up)
            send_refuse FS rejected the call (e.g. 4xx or 5xx)
            send_cancel n/a

            <b>Outgoing :</b>
            send_bye    FS sent BYE to the endpoint (we hung up)
            recv_bye    FS received BYE from the endpoint (they hung up)
            send_refuse Endpoint rejected the call (e.g. 4xx or 5xx)
            send_cancel FS aborted the call (we sent CANCEL)"""))
    sip_hangup_cause = models.CharField(
        _(u"SIP hangup cause"),
        null=True,
        default="",
        max_length=100)
    sell_destination = models.CharField(
        _(u'sell destination'),
        blank=True,
        default='',
        null=True,
        max_length=128,
        db_index=True)
    cost_destination = models.CharField(
        _(u'cost destination'),
        blank=True,
        default='',
        null=True,
        max_length=128,
        db_index=True)
    insee_code = models.CharField(
        _(u'Special code for routing urgency numbers'),
        null=True,
        blank=True,
        max_length=10,
        help_text=_(u"""Postal code, INSEE code ... for routing
          urgency number to the right urgency call center."""))
    customerdirectory_id = models.CharField(
        max_length=50,
        null=True,
        verbose_name=_(u"sip account"))
    rctype = models.CharField(
        _(u"Type of call"),
        max_length=10,
        null=True,
        blank=True,
        help_text=_(u"""Type of calls."""))

    class Meta:
        db_table = 'cdr'
        app_label = 'cdr'
        ordering = ('start_stamp', 'customer')
        indexes = [
            models.Index(fields=['customerdirectory_id']),
        ]
        verbose_name = _(u"CDR")
        verbose_name_plural = _(u"CDRs")

    def __unicode__(self):
        if self.start_stamp:
            return unicode(self.start_stamp)
        else:
            return self.custom_alias_name

    def hangup_cause_colored(self):
        if self.billsec == 0:
            color = "red"
        else:
            color = "green"
        return " <span style=color:%s>%s</span>" % (color, self.hangup_cause)
    hangup_cause_colored.allow_tags = True

    @property
    def daily_total_answered_calls(self):
        return qsstats.QuerySetStats(
            self.objects.all()
                .exclude(effective_duration="0")
                .filter(hangup_cause="NORMAL_CLEARING"),
            'start_stamp',
            aggregate=Count('id')
        ).this_day()

    @property
    def daily_total_calls(self):
        return qsstats.QuerySetStats(
            self.objects.all(),
            'start_stamp',
            aggregate=Count('id')
        ).this_day()

    @property
    def daily_total_effective_duration_calls(self):
        return qsstats.QuerySetStats(
            self.objects.all()
                .exclude(effective_duration="0")
                .filter(hangup_cause="NORMAL_CLEARING"),
            'start_stamp',
            aggregate=Sum('effective_duration')
        ).this_day()

    @property
    def daily_total_sell_calls(self):
        return qsstats.QuerySetStats(
            self.objects.all()
                .exclude(effective_duration="0")
                .filter(hangup_cause="NORMAL_CLEARING"),
            'start_stamp',
            aggregate=Sum('total_sell')
        ).this_day()

    @property
    def daily_total_cost_calls(self):
        return qsstats.QuerySetStats(
            self.objects.all()
                .exclude(effective_duration="0")
                .filter(hangup_cause="NORMAL_CLEARING"),
            'start_stamp',
            aggregate=Sum('total_cost')
        ).this_day()

    def _get_min_effective_duration(self):
        if self.effective_duration:
            min = int(self.effective_duration / 60)
            sec = int(self.effective_duration % 60)
        else:
            min = 0
            sec = 0

        return "%02d:%02d" % (min, sec)
    min_effective_duration = property(_get_min_effective_duration)

    def _get_total_sell(self):
        if self.rate and self.rate != 0:
            totalsell = decimal.Decimal(self.billsec) * decimal.Decimal(self.rate) / 60
        else:
            totalsell = 0.000000
        if self.init_block:
            totalsell = decimal.Decimal(totalsell) + decimal.Decimal(self.init_block)
        return round(totalsell, 6)
    total_sell_py = property(_get_total_sell)

    def _get_total_cost(self):
        if self.cost_rate:
            totalcost = decimal.Decimal(self.effective_duration) * decimal.Decimal(self.cost_rate) / 60
        else:
            totalcost = 0.000000
        return round(totalcost, 6)
    total_cost_py = property(_get_total_cost)

    def _get_effective_duration(self):
        if self.effectiv_duration:
            effdur = math.ceil(self.effectiv_duration / 1000.0)
        else:
            effdur = 0
        return int(effdur)
    effective_duration_py = property(_get_effective_duration)

    def _get_billsec(self):
        if self.block_min_duration and self.effective_duration:
            if self.effective_duration < self.block_min_duration:
                billsec = self.block_min_duration
            else:
                billsec = math.ceil(self.effective_duration / self.block_min_duration) * self.block_min_duration
        else:
            billsec = self.effective_duration
        return int(billsec)
    billsec_py = property(_get_billsec)

    def success_cdr(self):
        return self.CDR.objects.exclude(effective_duration="0")

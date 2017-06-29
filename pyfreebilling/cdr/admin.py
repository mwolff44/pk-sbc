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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.db.models import Sum, Avg
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from datetime import date
import datetime
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from pyfreebilling.pyfreebill.models import Person

from .models import CDR
from .resources import CDRResourceExtra


DEFAULT_FORMATS = (base_formats.CSV, )


class TotalAveragesChangeList(ChangeList):

    def __init__(self, *args):
        super(TotalAveragesChangeList, self).__init__(*args)

    def get_min_duration(self, sec_duration):
        if sec_duration:
            min = int(sec_duration / 60)
            sec = int(sec_duration % 60)
        else:
            min = 0
            sec = 0
        return "%02d:%02d" % (min, sec)

    def get_results(self, request):
        super(TotalAveragesChangeList, self).get_results(request)
        self.total_sell_total = 0
        self.total_cost_total = 0
        try:
            q = self.result_list.aggregate(
                total_sell_sum=Sum('total_sell'),
                total_cost_sum=Sum('total_cost'),
                effective_duration_sum=Sum('effective_duration'),
                effective_duration_avg=Avg('effective_duration')
            )
        except:
            self.total_effective_duration = 0
            self.total_cost_total = 0
            self.total_sell_total = 0
            self.avg_effective_duration = 0
            self.margin = 0
            return
        self.total_effective_duration = q['effective_duration_sum']
        self.total_cost_total = q['total_cost_sum']
        self.total_sell_total = q['total_sell_sum']
        self.avg_effective_duration = q['effective_duration_avg']
        try:
            self.margin = self.total_sell_total - self.total_cost_total
        except:
            self.margin = 0
        self.min_avg_effective_duration = self.get_min_duration(q['effective_duration_avg'])
        self.min_total_effective_duration = self.get_min_duration(q['effective_duration_sum'])


class CDRAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ['^prefix',
                     '^destination_number',
                     '^customer__name',
                     '^cost_destination',
                     '^sell_destination']
    list_filter = ('start_stamp',)
#    date_hierarchy = 'start_stamp'
    change_list_template = 'admin/cdr/change_list.html'
    resource_class = CDRResourceExtra
    fieldsets = (
        (_(u'General'), {
            'fields': ('customer', 'customerdirectory_id',
                       'start_stamp',
                       'destination_number',
                       ('min_effective_duration', 'billsec'),
                       ('sell_destination', 'cost_destination'),
                       'switchname')
        }),
        (_(u'Advanced date / duration infos'), {
            'fields': (('answered_stamp',
                        'end_stamp',
                        'duration',
                        'effectiv_duration'))
        }),
        (_(u'Financial infos'), {
            'fields': (('total_cost', 'cost_rate'),
                       ('total_sell', 'rate'),
                       ('init_block', 'block_min_duration'))
        }),
        (_(u'LCR infos'), {
            'fields': ('prefix',
                       ('ratecard_id', 'lcr_group_id'),
                       ('lcr_carrier_id', 'gateway'))
        }),
        (_(u'Call detailed infos'), {
            'fields': ('caller_id_number',
                       ('hangup_cause',
                        'hangup_cause_q850',
                        'hangup_disposition',
                        'sip_hangup_cause'),
                       ('read_codec', 'write_codec'),
                       'sip_user_agent',
                       'customer_ip',
                       ('uuid', 'bleg_uuid', 'chan_name', 'country'))
        }),
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        if request.user.is_superuser:
            return
        else:
            return

    def get_changelist(self, request, **kwargs):
        return TotalAveragesChangeList

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display_links = ['start_stamp', ]
            return super(CDRAdmin, self).changelist_view(request,
                                                         extra_context=None)
        else:
            self.list_display_links = ['None', ]
            return super(CDRAdmin, self).changelist_view(request,
                                                         extra_context=None)

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ['-start_stamp', ]
        else:
            return ['-start_stamp', ]

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['start_stamp',
                    'customer',
                    'sell_destination',
                    'destination_number',
                    'min_effective_duration',
                    'hangup_cause_colored',
                    'lcr_carrier_id',
                    'cost_rate',
                    'rate',
                    'prefix',
                    'ratecard_id',
                    'switchname']
        else:
            return ['start_stamp',
                    'customer',
                    'customer_ip',
                    'sell_destination',
                    'destination_number',
                    'min_effective_duration',
                    'hangup_cause',
                    'rate',
                    'total_sell']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['start_stamp',
                    'customer',
                    'lcr_carrier_id',
                    'ratecard_id',
                    'rctype',
                    'switchname']
        else:
            return ['start_stamp', 'sell_destination']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['customer_ip',
                    'customer',
                    'customerdirectory_id',
                    'caller_id_number',
                    'destination_number',
                    'start_stamp',
                    'answered_stamp',
                    'end_stamp',
                    'duration',
                    'min_effective_duration',
                    'billsec',
                    'hangup_cause',
                    'hangup_cause_q850',
                    'gateway',
                    'lcr_carrier_id',
                    'prefix',
                    'country',
                    'cost_rate',
                    'total_cost',
                    'total_sell',
                    'rate',
                    'init_block',
                    'block_min_duration',
                    'ratecard_id',
                    'lcr_group_id',
                    'uuid',
                    'bleg_uuid',
                    'chan_name',
                    'read_codec',
                    'write_codec',
                    'sip_user_agent',
                    'hangup_disposition',
                    'effectiv_duration',
                    'sip_hangup_cause',
                    'sell_destination',
                    'cost_destination',
                    'switchname',
                    'sipserver_name']
        else:
            return ['start_stamp',
                    'customer',
                    'customer_ip',
                    'sell_destination',
                    'destination_number',
                    'min_effective_duration',
                    'hangup_cause',
                    'rate',
                    'total_sell']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['effectiv_duration',
                        'effective_duration',
                        'sip_rtp_rxstat',
                        'sip_rtp_txstat',
                        'switch_ipv4']
        if not request.user.is_superuser:
            self.exclude.append('cost_rate')
            self.exclude.append('total_cost')
            self.exclude.append('gateway')
            self.exclude.append('switchname')
            self.exclude.append('lcr_carrier_id')
            self.exclude.append('lcr_group_id')
            self.exclude.append('cost_destination')
        return super(CDRAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        today_c = date.today() - datetime.timedelta(days=settings.PFB_NB_CUST_CDR)
        today_a = date.today() - datetime.timedelta(days=settings.PFB_NB_ADMIN_CDR)
        user = getattr(request, 'user', None)
        qs = super(CDRAdmin, self).get_queryset(request)
        # add .prefetch_related('content_type') for reduce queries
        if user.is_superuser:
            return qs.filter(start_stamp__gte=today_a)
        else:
            usercompany = Person.objects.get(user=user)
        return unicode(qs.filter(customer=usercompany.company).filter(start_stamp__gte=today_c).filter(effective_duration__gt="0"))

    def get_export_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_export()]


admin.site.register(CDR, CDRAdmin)

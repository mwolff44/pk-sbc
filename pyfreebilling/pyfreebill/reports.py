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


from django.db.models import Sum, Avg, Count

from pyfreebilling.cdr.models import CDR

from model_report.report import reports, ReportAdmin
from model_report.utils import (usd_format, avg_column, sum_column, count_column)


class CDRReport(ReportAdmin):
    title = 'CDR stats'
    model = CDR
    fields = [
        'customer__name',
        'effective_duration',
        'total_sell',
        'total_cost']
    list_order_by = ('customer__name',)
    list_group_by = ('customer__name',)
    list_filter = ('start_stamp',)
    type = 'report'
    group_totals = {
        'total_sell': sum_column,
        'total_cost': sum_column,
        'effective_duration': sum_column,
    }
    report_totals = {
        'total_sell': sum_column,
        'total_cost': sum_column,
        'effective_duration': sum_column,
    }

    # verbose_name = 'CDR stats'
    # annotate = (
    #     ('id', Count, 'Nb Calls'),
    #     ('effective_duration', Sum),
    #     ('effective_duration', Avg),
    #     ('billsec', Sum),
    #     ('total_cost', Sum),
    #     ('total_sell', Sum),
    # )
    # aggregate = (
    #     ('id', Count, 'Nb Calls'),
    #     ('effective_duration', Sum),
    #     ('effective_duration', Avg),
    #     ('billsec', Sum),
    #     ('total_cost', Sum),
    #     ('total_sell', Sum),
    # )
    # group_by = [
    #     'customer__name',
    #     ('customer__name', 'sell_destination'),
    #     'sell_destination',
    #     'lcr_carrier_id__name',
    #     ('lcr_carrier_id__name', 'cost_destination'),
    #     'cost_destination',
    # ]
    # list_filter = [
    #     'sell_destination',
    #     'lcr_carrier_id__name',
    # ]

    # date_hierarchy = 'start_stamp'

reports.register('CDR-report', CDRReport)

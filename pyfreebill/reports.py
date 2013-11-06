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

import reporting
from django.db.models import Sum, Avg, Count
from pyfreebill.models import CDR

class CDRReport(reporting.Report):
    model = CDR
    verbose_name = 'CDR stats'
    annotate = (
        ('id', Count, 'Nb Calls'),
        ('effective_duration', Sum),
        ('effective_duration', Avg),
        ('billsec', Sum),
        ('total_cost', Sum),
        ('total_sell', Sum),
    )
    aggregate = (
        ('id', Count, 'Nb Calls'),
        ('effective_duration', Sum),
        ('effective_duration', Avg),
        ('billsec', Sum),
        ('total_cost', Sum),
        ('total_sell', Sum),
    )
    group_by = [
        'customer__name',
        ('customer__name', 'sell_destination'),
        'sell_destination',
        'lcr_carrier_id__name',
        ('lcr_carrier_id__name', 'cost_destination'),
        'cost_destination',
    ]
    list_filter = [
        'sell_destination',
        'lcr_carrier_id__name',
    ]

    date_hierarchy = 'start_stamp'

reporting.register('CDR', CDRReport)

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

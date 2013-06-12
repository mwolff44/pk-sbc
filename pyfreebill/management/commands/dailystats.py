from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import CDR
import datetime, qsstats
from django.db.models import Sum, Avg, Count, Max, Min
from django.db import connection
from pprint import pprint

class Command(BaseCommand):
    args = '<date>'
    help = 'calculate on daily basis stats'

    def handle(self, *args, **options):
        for daystats in args:
            try:
#                qs = CDR.objects.all().exclude(effective_duration="0").filter(hangup_cause="NORMAL_CLEARING").aggregate(Count('total_sell'))
#                qs2 = CDR.objects.all().exclude(effective_duration="0").filter(hangup_cause="NORMAL_CLEARING").aggregate(Count('total_sell'))
                qsall = CDR.objects.values('customer').annotate(count=Count('id'))
#exclude(effective_duration="0").filter(hangup_cause="NORMAL_CLEARING")
#qss = CDR.objects.all().values('customer','hangup_cause').annotate(Avg('effective_duration'), Max('effective_duration')).order_by('customer','hangup_cause')


# Filtre sur date
                today = datetime.date.today()
                yesterday = today - datetime.timedelta(days=1)
 
                qs = CDR.objects.all().filter(start_stamp__gte=yesterday).filter(start_stamp__lt=today)

# Filtre clients uuid unique - prendre celui avec id le plus eleve -  evite les cdr duplique pour cause de failover

# Filtre fournisseurs uuid unique - prendre celui avec id le plus eleve -  evite les cdr duplique pour cause de failover


# DimCustomerHangucause recuperation des stats globales tous les appels UNIQUE uuid
                qss = qs.values('customer','sell_destination','hangup_cause','sip_hangup_cause').annotate(Count('id')).order_by('customer','sell_destination','hangup_cause','sip_hangup_cause')

# DimProviderHangucause
                qss1 = CDR.objects.all().values('lcr_carrier_id','cost_destination','hangup_cause','sip_hangup_cause').exclude(lcr_carrier_id__isnull=True).annotate(Count('id')).order_by('lcr_carrier_id','cost_destination','hangup_cause','sip_hangup_cause')

# Stats sur les appels aboutits
                qss2 = qs.exclude(effective_duration__gt="0").filter(hangup_cause="NORMAL_CLEARING")
                qss3 = qss2.values('customer','sell_destination').annotate(Avg('effective_duration'), Max('effective_duration'), Min('effective_duration'), Count('id'), Sum('total_sell'), Sum('total_cost')).order_by('customer','sell_destination')
# Customers


# Providers
#.values('lcr_carrier_id','cost_destination'.annotate(------).order_by('lcr_caller_id','sell_destination')

#    provider
#    destination
#    success_calls
#    total_duration
#    avg_duration
#    max_duration
#    min_duration
#    total_sell
#    total_cost


#                qss_sum_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Sum('effective_duration'))
#                qss_avg_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Avg('effective_duration'))                
#                qss_min_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Min('effective_duration'))
#                qss_max_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Max('effective_duration'))
#                qss_success_calls = qsstats.QuerySetStats(qs, 'start_stamp')
                today = datetime.date.today()
                print 'daily stats : %s ' % (qss3)
                pprint(connection.queries)   
            except CDR.DoesNotExist:
                raise CommandError('stats does not exist')

            #poll.opened = False
            #poll.save()

            self.stdout.write('Successfully stats ')

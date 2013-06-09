from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import CDR, DailyStats
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

#                qss_sum_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Sum('effective_duration'))
#                qss_avg_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Avg('effective_duration'))                
#                qss_min_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Min('effective_duration'))
#                qss_max_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Max('effective_duration'))
#                qss_success_calls = qsstats.QuerySetStats(qs, 'start_stamp')
                today = datetime.date.today()
                print 'daily stats : %s ' % (qsall)
                pprint(connection.queries)   
            except CDR.DoesNotExist:
                raise CommandError('stats does not exist')

            #poll.opened = False
            #poll.save()

            self.stdout.write('Successfully stats ')

from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import CDR, DailyStats
import datetime, qsstats
from django.db.models import Sum

class Command(BaseCommand):
    args = '<date>'
    help = 'calculate on daily basis stats'

    def handle(self, *args, **options):
        for daystats in args:
            try:
                qs = CDR.objects.all()
                qss = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Sum('effective_duration'))
                today = datetime.date.today()
                print 'daily stats : %s' % qss.this_month()   
            except CDR.DoesNotExist:
                raise CommandError('stats does not exist')

            #poll.opened = False
            #poll.save()

            self.stdout.write('Successfully stats "%s"' % qss.this_day())

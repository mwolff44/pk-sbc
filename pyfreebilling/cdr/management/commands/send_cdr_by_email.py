# Guillaume Genty, Waycom
# Dec. 2017

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from pyfreebilling.cdr.models import CDR, Company, RateCard
from datetime import date, time, timedelta, datetime
import calendar
from django.db import connection
from django.utils import timezone
from pprint import pprint
from dateutil.tz import tzlocal
from StringIO import StringIO
import csv
from django.core.mail import EmailMessage, mail_admins

TODAY = date.today()
MIDNIGHT = datetime.combine(TODAY, time.min)

CDR_PERIODS = {
    'cdr_day': (MIDNIGHT - timedelta(days=1), MIDNIGHT),
    'cdr_week': (MIDNIGHT - timedelta(days=TODAY.weekday()+7), MIDNIGHT - timedelta(days=TODAY.weekday())),
    'cdr_month': (datetime.combine((TODAY.replace(day=1)-timedelta(days=1)).replace(day=1), time.min), MIDNIGHT - timedelta(days=TODAY.day-1))
}
#print CDR_PERIODS

class Command(BaseCommand):
    help = 'Send all CDR exports by email.'
    
    def add_arguments(self, parser):
        parser.add_argument('period', nargs=1, type=str, choices=CDR_PERIODS.keys()+['all'])

    def handle(self, *args, **options):

        tz = tzlocal()
        wantperiod = options['period'][0]
        
        rc_didin = [x.id for x in RateCard.objects.all().filter(rctype='DIDIN')]
        rc_emerg = [x.id for x in RateCard.objects.all().filter(rctype='EMERGENCY')]
        
        customers = Company.objects.all().filter(customer_enabled=True)
        for cust in customers:

            emails = cust.email_address.all().filter(location__startswith='cdr_')
            if not emails:
                continue
            
            targets = {}
            for e in emails:
                if not e.location in targets:
                    targets[e.location] = []
                targets[e.location].append(e.email_address)
            
            for period in CDR_PERIODS:
                if wantperiod != 'all' and period != wantperiod:
                    continue
                if not period in targets:
                    continue
                #print CDR_PERIODS[period]
                try:
                    p_start = CDR_PERIODS[period][0].replace(tzinfo=tz)
                    p_end = CDR_PERIODS[period][1].replace(tzinfo=tz)
                    #p_end = datetime.now().replace(tzinfo=tz) # DEBUG
                    list = CDR.objects.all().filter(end_stamp__gte=p_start, end_stamp__lt=p_end, customer_id=cust.id, billsec__gt=0)
                    csvfile = StringIO()
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(['direction', 'start', 'end', 'billed_sec', 'from', 'to', 'ip', 'destination', 'price', 'uuid'])
                    for l in list:
                        if l.ratecard_id_id in rc_emerg:
                            continue
                        if l.ratecard_id_id in rc_didin:
                            csvwriter.writerow(['IN',
                                                timezone.localtime(l.start_stamp),
                                                timezone.localtime(l.end_stamp),
                                                l.billsec,
                                                l.caller_id_number.lstrip("+"),
                                                l.destination_number.lstrip("+"),
                                                None,
                                                l.sell_destination.encode('ascii',errors='ignore'),
                                                l.total_sell,
                                                l.bleg_uuid
                                              ])
                        else:
                            csvwriter.writerow(['OUT',
                                                timezone.localtime(l.start_stamp),
                                                timezone.localtime(l.end_stamp),
                                                l.billsec,
                                                l.caller_id_number.lstrip("+"),
                                                l.destination_number.lstrip("+"),
                                                l.customer_ip,
                                                l.sell_destination.encode('ascii',errors='ignore'),
                                                l.total_sell,
                                                l.uuid
                                              ])

                    message = EmailMessage("%s - CDR for customer %s"%(settings.EMAIL_SIGNATURE, cust.name),
                                           "Extract of call data records from %s to %s.\nCSV file attached."%(timezone.localtime(p_start), timezone.localtime(p_end)),
                                           None,
                                           targets[period])
                    message.attach('%s-%s-%s.csv'%(period.replace('_','-'), cust.slug, p_start.strftime('%Y%m%d')), csvfile.getvalue(), 'text/csv')
                    message.send()
                    self.stdout.write('CDRs for %s sent to %s'%(cust.name, ', '.join(targets[period])))
                except Exception, e:
                    self.stderr.write(str(e))

        self.stdout.write('OK')
        
        #pprint(connection.queries)


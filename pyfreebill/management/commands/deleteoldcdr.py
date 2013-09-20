from django.core.management.base import BaseCommand, CommandError
from pyfreebill.models import CDR
import datetime
from django.db import connection
from django.utils import timezone
from pprint import pprint
#import dse
import math
import decimal
import pytz

class Command(BaseCommand):
    args = '<date>'
    help = 'delete old cdr from database - failed : delete failed cdr older than 7 days -'

    def handle(self, *args, **options):
        for var in args:
            try:

                current_tz = pytz.utc
                if var == "failed":
                    dt = datetime.datetime.now()
                    today = datetime.datetime(dt.year, dt.month, dt.day, 00, 00, 00).replace(tzinfo=current_tz)
                    yesterday = today - datetime.timedelta(days=7)
                elif var == "past":
                    today = datetime.datetime(2013, 7, 8, 00, 00, 00).replace(tzinfo=current_tz)
                    yesterday = today - datetime.timedelta(days=1)
                elif var == "custom":
                    pass
                else:
                    return

# Query construction and delete
                qs_delete_cdr = CDR.objects.all().filter(start_stamp__lt=yesterday).filter(effective_duration="0").delete()

#                pprint(connection.queries)   
            except CDR.DoesNotExist:
                raise CommandError('cdr does not exist')

            self.stdout.write('Successfully operations ')

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

from django.core.management.base import BaseCommand, CommandError
from pyfreebilling.cdr.models import CDR
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
    help = 'delete old cdr from database - failed : delete failed cdr older than 3 days -'

    def handle(self, *args, **options):
        for var in args:
            try:

                current_tz = pytz.utc
                if var == "failed":
                    dt = datetime.datetime.now()
                    today = datetime.datetime(dt.year, dt.month, dt.day, 00, 00, 00).replace(tzinfo=current_tz)
                    yesterday = today - datetime.timedelta(days=3) # better to add a settings
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

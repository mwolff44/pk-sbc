# Copyright 2013-2016 Mathias WOLFF
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
                qs = CDR.objects.all().filter(customer="12").filter(effective_duration__gt="0")
#.filter(lcr_carrier_id="20")
# sixtocom = 20 _ Lvoip = 11

                qss_sell = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Sum('total_sell'))
                qss_sum_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Sum('effective_duration'))
                qss_avg_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Avg('effective_duration'))                
                qss_max_duration = qsstats.QuerySetStats(qs, 'start_stamp', aggregate=Max('effective_duration'))

                qs1 = CDR.objects.all().filter(customer="13").filter(effective_duration__gt="0")
#.filter(lcr_carrier_id="20")

                qss1_sell = qsstats.QuerySetStats(qs1, 'start_stamp', aggregate=Sum('total_sell'))
                qss_sum_duration1 = qsstats.QuerySetStats(qs1, 'start_stamp', aggregate=Sum('effective_duration'))
                qss_avg_duration1 = qsstats.QuerySetStats(qs1, 'start_stamp', aggregate=Avg('effective_duration'))
                qss_max_duration1 = qsstats.QuerySetStats(qs1, 'start_stamp', aggregate=Max('effective_duration'))

                qs2 = CDR.objects.all().filter(customer="7").filter(effective_duration__gt="0").filter(ratecard_id="9")
#.filter(lcr_carrier_id="20")

                qss_sum_duration2 = qsstats.QuerySetStats(qs2, 'start_stamp', aggregate=Sum('effective_duration'))
                qss_avg_duration2 = qsstats.QuerySetStats(qs2, 'start_stamp', aggregate=Avg('effective_duration'))
                qss_max_duration2 = qsstats.QuerySetStats(qs2, 'start_stamp', aggregate=Max('effective_duration'))

                today = datetime.date.today()
                seven_days_ago = today - datetime.timedelta(days=8)
                time_series = qss1_sell.time_series(seven_days_ago, today)
                time_series1 = qss_sell.time_series(seven_days_ago, today)
                print '----------------------------------'
                print 'weeky stats delta : day :  - Total sell : %s' % [t[1] for t in time_series]
                print 'weeky stats keyyo : day :  - Total seconds : %s' % [t[1] for t in time_series1]
                print '------------DAILY-----------------'
                print 'daily stats keyyo : Sum : %s - Avg : %s - Max : %s - Total sell : %s' % (qss_sum_duration.this_day(), qss_avg_duration.this_day(), qss_max_duration.this_day(), qss_sell.this_day())
                print 'daily stats delta : Sum : %s - Avg : %s - Max : %s ' % (qss_sum_duration1.this_day(), qss_avg_duration1.this_day(), qss_max_duration1.this_day())
                print 'daily stats coinfru : Sum : %s - Avg : %s - Max : %s ' % (qss_sum_duration2.this_day(), qss_avg_duration2.this_day(), qss_max_duration2.this_day())
                print '------------MONTHLY---------------'
                print 'monthly stats keyyo : Sum : %s - Avg : %s - Max : %s - Total sell : %s' % (qss_sum_duration.this_month(), qss_avg_duration.this_month(), qss_max_duration.this_month(), qss_sell.this_month())
                print 'monthly stats delta : Sum : %s - Avg : %s - Max : %s ' % (qss_sum_duration1.this_month(), qss_avg_duration1.this_month(), qss_max_duration1.this_month())
                print 'monthly stats coinfru : Sum : %s - Avg : %s - Max : %s ' % (qss_sum_duration2.this_month(), qss_avg_duration2.this_month(), qss_max_duration2.this_month())

            except CDR.DoesNotExist:
                raise CommandError('stats does not exist')

            #poll.opened = False
            #poll.save()

            self.stdout.write('Successfully stats ')


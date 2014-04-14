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
from pyfreebill.models import CDR, DimDate, DimCustomerHangupcause, DimCustomerSipHangupcause, DimProviderHangupcause, DimProviderSipHangupcause, DimCustomerDestination, DimProviderDestination
import datetime
from django.db.models import Sum, Avg, Count, Max, Min
from django.db import connection
from django.utils import timezone
from pprint import pprint
#import dse
import math
import decimal
import pytz

class Command(BaseCommand):
    args = '<date>'
    help = 'calculate stats - lastday, for last day stats - past, for past stats - custom + options for specific stats - first = [2013, 06, 14, 00, 00, 00], last = [2013, 06, 18, 00, 00, 00] '

    def handle(self, *args, **options):
        for var in args:
            try:

# date filter
# today = datetime.datetime(2013, 06, 14, 00, 00, 00)
                current_tz = pytz.utc
                if var == "lastday":
                    dt = datetime.datetime.now()
                    today = datetime.datetime(dt.year, dt.month, dt.day, 00, 00, 00).replace(tzinfo=current_tz)
                    yesterday = today - datetime.timedelta(days=1)
                elif var == "past":
                    today = datetime.datetime(2014, 04, 15, 00, 00, 00).replace(tzinfo=current_tz)
                    yesterday = today - datetime.timedelta(days=1)
                elif var == "custom":
                    for fd in first:
                        try:
                            today = datetime.datetime(fd[0], fd[1], fd[2], fd[3], fd[4], fd[5]).replace(tzinfo=current_tz)
                        except:
                            return
                    for ld in last:
                        try:
                            yesterday = datetime.datetime(fd[0], fd[1], fd[2], fd[3], fd[4], fd[5]).replace(tzinfo=current_tz)
                        except:
                            return
                else:
                    return
# Query construction
                qs = CDR.objects.all().filter(start_stamp__gte=yesterday).filter(start_stamp__lt=today)
                #exclude(sell_destination='did')
                qs_uuid_unique = qs.order_by('-start_stamp')
# Customer filter - take unique uuid with late start_stamp
# DimCustomerHangupCause
                qss_hangup_unique_customer = qs_uuid_unique.values('customer','sell_destination','hangup_cause').annotate(total_calls=Count('uuid', distinct = True)).order_by('customer','sell_destination')
# DimCustomerSipHangupCause
                qss_siphangup_unique_customer = qs_uuid_unique.values('customer','sell_destination','sip_hangup_cause').annotate(total_calls=Count('uuid', distinct = True)).order_by('customer','sell_destination')
# Provider filter - take unique uuid with late start_stamp
# DimProviderHangupCause
                qss_hangup_unique_provider = qs_uuid_unique.values('lcr_carrier_id','cost_destination','hangup_cause').exclude(lcr_carrier_id__isnull=True).annotate(total_calls=Count('uuid', distinct = True)).order_by('lcr_carrier_id','cost_destination')
# DimProviderSipHangupCause
                qss_siphangup_unique_provider = qs_uuid_unique.values('lcr_carrier_id','cost_destination','sip_hangup_cause').exclude(lcr_carrier_id__isnull=True).annotate(total_calls=Count('uuid', distinct = True)).order_by('lcr_carrier_id','cost_destination')
# Stats on successful calls 
                qss2 = qs.filter(effective_duration__gt="0")
# Customers
# DimCustomerDestination
                qss_success_customer = qss2.extra(select={'destination': 'sell_destination'}).values('customer','destination').annotate(total_duration=Sum('effective_duration'), avg_duration=Avg('effective_duration'), max_duration=Max('effective_duration'), min_duration=Min('effective_duration'), success_calls=Count('id'), total_sell=Sum('total_sell'), total_cost=Sum('total_cost')).order_by('customer','sell_destination')
# Providers
# DimProviderDestination
                qss_success_provider = qss2.extra(select={'provider': 'lcr_carrier_id_id', 'destination': 'cost_destination'}).values('provider','destination').annotate(total_duration=Sum('effective_duration'), avg_duration=Avg('effective_duration'), max_duration=Max('effective_duration'), min_duration=Min('effective_duration'), success_calls=Count('id'), total_sell=Sum('total_sell'), total_cost=Sum('total_cost')).order_by('lcr_carrier_id','cost_destination')

                # get or set dim date
                try :
                    workingdate = DimDate.objects.get(date=yesterday)
                except DimDate.DoesNotExist:
                    workingdate = DimDate(
                        date = yesterday,
                        day = yesterday.day,
                        day_of_week = yesterday.isoweekday(),
                        hour = yesterday.hour,
                        month = yesterday.month,
                        quarter = " ",
                        year = yesterday.year
                    ) 
                    workingdate.save()
                    current_date = DimDate.objects.get(date=yesterday).id

# DimCustomerHangupCause
                    for item in qss_hangup_unique_customer:

                        data_dchc = DimCustomerHangupcause(
                            customer_id = item["customer"],
                            destination = item["sell_destination"],
                            hangupcause = item["hangup_cause"],
                            date_id = current_date,
                            total_calls = int(item["total_calls"])
                        )
                        data_dchc.save()

# DimCustomerSipHangupCause
                    for item in qss_siphangup_unique_customer:

                        data_dcshc = DimCustomerSipHangupcause(
                            customer_id = item["customer"],
                            destination = item["sell_destination"],
                            sip_hangupcause = item["sip_hangup_cause"],
                            date_id = current_date,
                            total_calls = int(item["total_calls"])
                        )
                        data_dcshc.save()

# DimProviderHangupCause
                    for item in qss_hangup_unique_provider:

                        data_dphc = DimProviderHangupcause(
                            provider_id = item["lcr_carrier_id"],
                            destination = item["cost_destination"],
                            hangupcause = item["hangup_cause"],
                            date_id = current_date,
                            total_calls = int(item["total_calls"])
                        )
                        data_dphc.save()

# DimProviderSipHangupCause
                    for item in qss_siphangup_unique_provider:

                        data_dpshc = DimProviderSipHangupcause(
                            provider_id = item["lcr_carrier_id"],
                            destination = item["cost_destination"],
                            sip_hangupcause = item["sip_hangup_cause"],
                            date_id = current_date,
                            total_calls = int(item["total_calls"])
                        )
                        data_dpshc.save()

# DimCustomerDestination
                    for item in qss_success_customer:

                        data_dcd = DimCustomerDestination(
                            customer_id=item["customer"],
                            destination=item["destination"],
                            date_id = current_date,
                            total_calls = "0",
                            success_calls = int(item["success_calls"]),
                            total_duration=item["total_duration"],
                            avg_duration=int(math.ceil(item["avg_duration"])),
                            max_duration=int(math.ceil(item["max_duration"])),
                            min_duration=int(math.ceil(item["min_duration"])),
                            total_sell=item["total_sell"],
                            total_cost=item["total_cost"]
                        )
                        data_dcd.save()

# DimProviderDestination
                    for item in qss_success_provider:
                        
                        data_dpd = DimProviderDestination(
                            provider_id=item["provider"],
                            destination=item["destination"],
                            date_id = current_date,
                            total_calls = "0",
                            success_calls = int(item["success_calls"]),
                            total_duration=item["total_duration"],
                            avg_duration=int(math.ceil(item["avg_duration"])),
                            max_duration=int(math.ceil(item["max_duration"])),
                            min_duration=int(math.ceil(item["min_duration"])),
                            total_sell=item["total_sell"],
                            total_cost=item["total_cost"]
                        )
                        data_dpd.save()

#                pprint(connection.queries)   
            except CDR.DoesNotExist:
                raise CommandError('stats does not exist')

            self.stdout.write('Successfully stats ')

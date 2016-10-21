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

from import_export import resources
from .models import CDR, CalleridPrefix


class CDRResourceExtra(resources.ModelResource):

    class Meta:
        model = CDR
        exclude = ('id',
                   'country',
                   'uuid',
                   'bleg_uuid',
                   'chan_name',
                   'answered_stamp',
                   'end_stamp',
                   'duration',
                   'effeciv_duration',
                   'total_cost',
                   'cost_rate',
                   'gateway',
                   'ratecard_id',
                   'lcr_carrier_id',
                   'lcr_group_id',
                   'sip_rtp_rxstat',
                   'sip_rtp_txstat',
                   'switchname',
                   'switch_ipv4',
                   'cost_destination',
                   'hangup_disposition',
                   'sip_hangup_cause')
        fields = ('customer__name',
                  'caller_id_number',
                  'destination_number',
                  'start_stamp',
                  'billsec',
                  'prefix',
                  'sell_destination',
                  'rate',
                  'init_block',
                  'block_min_duration',
                  'total_sell',
                  'customer_ip',
                  'sip_user_agent')
        export_order = ('customer__name',
                        'caller_id_number',
                        'destination_number',
                        'start_stamp',
                        'billsec',
                        'prefix',
                        'sell_destination',
                        'rate',
                        'init_block',
                        'block_min_duration',
                        'total_sell',
                        'customer_ip',
                        'sip_user_agent')


class CalleridPrefixResource(resources.ModelResource):

    class Meta:
        model = CalleridPrefix
        exlude = ('id',
                  'date_added',
                  'date_modified')
        fields = ('prefix', )

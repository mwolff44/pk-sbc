from import_export import resources, fields
from pyfreebill.models import ProviderRates, CustomerRates, CDR

class CDRResource(resources.ModelResource):

    class Meta:
        model = CDR
        exclude = ('id', 'country', 'uuid', 'bleg_uuid', 'chan_name', 'answered_stamp', 'end_stamp', 'duration', 'effectiv_duration', 'lcr_group_id', 'sip_rtp_rxstat', 'sip_rtp_txstat', 'switchname', 'switch_ipv4')

class CDRResourceExtra(resources.ModelResource):

    class Meta:
        model = CDR
        exclude = ('id', 'country', 'uuid', 'bleg_uuid', 'chan_name', 'answered_stamp', 'end_stamp', 'duration', 'effectiv_duration', 'total_cost', 'cost_rate', 'gateway', 'ratecard_id', 'lcr_carrier_id', 'lcr_group_id', 'sip_rtp_rxstat', 'sip_rtp_txstat', 'switchname', 'switch_ipv4', 'cost_destination', 'hangup_disposition', 'sip_hangup_cause')
        fields = ('customer__name', 'caller_id_number', 'destination_number', 'start_stamp', 'billsec', 'prefix', 'sell_destination', 'rate', 'init_block', 'block_min_duration', 'total_sell', 'customer_ip', 'sip_user_agent')
        export_order = ('customer__name', 'caller_id_number', 'destination_number', 'start_stamp', 'billsec', 'prefix', 'sell_destination', 'rate', 'init_block', 'block_min_duration', 'total_sell', 'customer_ip', 'sip_user_agent')

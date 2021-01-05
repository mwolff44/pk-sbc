from django import forms

from .models import CDR, DimDate, DimCustomerHangupcause, DimCustomerSipHangupcause, DimProviderHangupcause, DimProviderSipHangupcause, DimCustomerDestination, DimProviderDestination


class CDRForm(forms.ModelForm):
    class Meta:
        model = CDR
        fields = [
            'customer_ip',
            'aleg_uuid',
            'caller_number',
            'callee_number',
            'start_time',
            'answered_time',
            'end_time',
            'duration',
            'billsec',
            'costsec',
            'read_codec',
            'write_codec',
            'sip_code',
            'sip_reason',
            'cost_rate',
            'total_sell',
            'total_cost',
            'rate',
            'sip_charge_info',
            'sip_user_agent',
            'sip_rtp_rxstat',
            'sip_rtp_txstat',
            'kamailio_server',
            'hangup_disposition',
            'direction',
            'customer',
            'provider',
            'caller_destination',
            'callee_destination',
            'media_server',
            'call_class',
            'cdr_acc',
            'rated'
        ]


class DimDateForm(forms.ModelForm):
    class Meta:
        model = DimDate
        fields = ['date', 'day', 'day_of_week', 'hour', 'month', 'quarter', 'year']


class DimCustomerHangupcauseForm(forms.ModelForm):
    class Meta:
        model = DimCustomerHangupcause
        fields = ['hangupcause', 'total_calls', 'direction', 'customer', 'date', 'destination']


class DimCustomerSipHangupcauseForm(forms.ModelForm):
    class Meta:
        model = DimCustomerSipHangupcause
        fields = ['sip_hangupcause', 'total_calls', 'direction', 'customer', 'date', 'destination']


class DimProviderHangupcauseForm(forms.ModelForm):
    class Meta:
        model = DimProviderHangupcause
        fields = ['hangupcause', 'total_calls', 'direction', 'provider', 'date', 'destination']


class DimProviderSipHangupcauseForm(forms.ModelForm):
    class Meta:
        model = DimProviderSipHangupcause
        fields = ['sip_hangupcause', 'total_calls', 'direction', 'provider', 'date', 'destination']


class DimCustomerDestinationForm(forms.ModelForm):
    class Meta:
        model = DimCustomerDestination
        fields = ['total_calls', 'success_calls', 'total_duration', 'avg_duration', 'max_duration', 'min_duration', 'total_sell', 'total_cost', 'direction', 'customer', 'date', 'destination']


class DimProviderDestinationForm(forms.ModelForm):
    class Meta:
        model = DimProviderDestination
        fields = ['total_calls', 'success_calls', 'total_duration', 'avg_duration', 'max_duration', 'min_duration', 'total_sell', 'total_cost', 'direction', 'provider', 'date', 'destination']

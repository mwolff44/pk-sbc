from . import models

from rest_framework import serializers


class CDRSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CDR
        fields = (
            'pk',
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
        )


class DimDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimDate
        fields = (
            'pk',
            'date',
            'day',
            'day_of_week',
            'hour',
            'month',
            'quarter',
            'year',
        )


class DimCustomerHangupcauseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimCustomerHangupcause
        fields = (
            'pk',
            'hangupcause',
            'total_calls',
            'direction',
        )


class DimCustomerSipHangupcauseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimCustomerSipHangupcause
        fields = (
            'pk',
            'sip_hangupcause',
            'total_calls',
            'direction',
        )


class DimProviderHangupcauseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimProviderHangupcause
        fields = (
            'pk',
            'hangupcause',
            'total_calls',
            'direction',
        )


class DimProviderSipHangupcauseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimProviderSipHangupcause
        fields = (
            'pk',
            'sip_hangupcause',
            'total_calls',
            'direction',
        )


class DimCustomerDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimCustomerDestination
        fields = (
            'pk',
            'total_calls',
            'success_calls',
            'total_duration',
            'avg_duration',
            'max_duration',
            'min_duration',
            'total_sell',
            'total_cost',
            'direction',
        )


class DimProviderDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DimProviderDestination
        fields = (
            'pk',
            'total_calls',
            'success_calls',
            'total_duration',
            'avg_duration',
            'max_duration',
            'min_duration',
            'total_sell',
            'total_cost',
            'direction',
        )

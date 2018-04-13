from . import models

from rest_framework import serializers


class AccSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Acc
        fields = (
            'pk',
            'method',
            'from_tag',
            'to_tag',
            'callid',
            'sip_code',
            'sip_reason',
            'time',
            'time_attr',
            'time_exten',
        )


class AccCdrSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AccCdr
        fields = (
            'pk',
            'start_time',
            'end_time',
            'duration',
        )


class MissedCallSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MissedCall
        fields = (
            'pk',
            'method',
            'from_tag',
            'to_tag',
            'callid',
            'sip_code',
            'sip_reason',
            'time',
        )

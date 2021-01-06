from . import models

from rest_framework import serializers


class CustomerEndpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerEndpoint
        fields = (
            'pk', 
            'registration', 
            'password', 
            'description', 
            'name', 
            'rtp_ip', 
            'sip_ip', 
            'sip_port', 
            'max_calls', 
            'calls_per_second', 
            'outbound_caller_id_name', 
            'outbound_caller_id_number', 
            'force_caller_id', 
            'masq_caller_id', 
            'urgency_number', 
            'insee_code', 
            'enabled', 
            'fake_ring', 
            'cli_debug', 
            'created', 
            'modified', 
            'transcoding_allowed', 
            'recording_allowed', 
            'recording_always', 
            'recording_limit', 
            'recording_retention', 
            'sip_transport', 
            'rtp_transport', 
            'rtp_tos', 
            'pai', 
            'pid', 
            'ha1', 
            'ha1b', 
        )


class CodecSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Codec
        fields = (
            'pk', 
            'name', 
            'created', 
            'modified', 
            'number', 
            'ptime', 
            'stereo', 
            'rfc_name', 
            'description', 
        )


class ProviderEndpointSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderEndpoint
        fields = (
            'pk', 
            'name', 
            'created', 
            'modified', 
            'max_calls', 
            'enabled', 
            'prefix', 
            'suffix', 
            'username', 
            'password', 
            'register', 
            'sip_proxy', 
            'sip_transport', 
            'sip_port', 
            'realm', 
            'from_domain', 
            'expire_seconds', 
            'retry_seconds', 
            'caller_id_in_from',
            'add_plus_in_caller',
            'pid', 
            'pai', 
            'calls_per_second', 
            'rtp_transport', 
            'rtp_tos', 
        )



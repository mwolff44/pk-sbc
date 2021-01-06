from django import forms

from .models import CustomerEndpoint, Codec, ProviderEndpoint


class CustomerEndpointForm(forms.ModelForm):
    class Meta:
        model = CustomerEndpoint
        fields = ['registration', 'password', 'description', 'name', 'rtp_ip', 'sip_ip', 'sip_port', 'max_calls', 'calls_per_second', 'outbound_caller_id_name', 'outbound_caller_id_number', 'force_caller_id', 'masq_caller_id', 'urgency_number', 'insee_code', 'enabled', 'fake_ring', 'cli_debug', 'transcoding_allowed', 'recording_allowed', 'recording_always', 'recording_limit', 'recording_retention', 'sip_transport', 'rtp_transport', 'rtp_tos', 'pai', 'pid', 'ha1', 'ha1b', 'customer', 'callerid_norm', 'callee_norm', 'callerid_norm_in', 'callee_norm_in', 'codec_list']


class CodecForm(forms.ModelForm):
    class Meta:
        model = Codec
        fields = ['name', 'number', 'ptime', 'stereo', 'rfc_name', 'description']


class ProviderEndpointForm(forms.ModelForm):
    class Meta:
        model = ProviderEndpoint
        fields = ['name', 'max_calls', 'enabled', 'prefix', 'suffix', 'username', 'password', 'register', 'sip_proxy', 'sip_transport', 'sip_port', 'realm', 'from_domain', 'expire_seconds', 'retry_seconds', 'caller_id_in_from', 'pid', 'ppi', 'pai', 'calls_per_second', 'rtp_transport', 'rtp_tos', 'provider', 'add_plus_in_caller', 'callerid_norm', 'callee_norm', 'callerid_norm_in', 'callee_norm_in', 'codec_list']

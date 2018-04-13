from django import forms
from .models import UacReg, Trusted


class UacRegForm(forms.ModelForm):
    class Meta:
        model = UacReg
        fields = ['l_uuid', 'l_username', 'l_domain', 'r_username', 'r_domain', 'realm', 'auth_username', 'auth_password', 'auth_ha1', 'auth_proxy', 'expires', 'flags', 'reg_delay']


class TrustedForm(forms.ModelForm):
    class Meta:
        model = Trusted
        fields = ['src_ip', 'proto', 'from_pattern', 'ruri_pattern', 'tag', 'priority']



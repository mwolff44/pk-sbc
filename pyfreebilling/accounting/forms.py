from django import forms
from .models import Acc, AccCdr, MissedCall


class AccForm(forms.ModelForm):
    class Meta:
        model = Acc
        fields = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time', 'time_attr', 'time_exten']


class AccCdrForm(forms.ModelForm):
    class Meta:
        model = AccCdr
        fields = ['start_time', 'end_time', 'duration']


class MissedCallForm(forms.ModelForm):
    class Meta:
        model = MissedCall
        fields = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time']

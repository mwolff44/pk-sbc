from django import forms
from .models import Dialog, DialogVar


class DialogForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = ['hash_entry', 'hash_id', 'callid', 'from_uri', 'from_tag', 'to_uri', 'to_tag', 'caller_cseq', 'callee_cseq', 'caller_route_set', 'callee_route_set', 'caller_contact', 'callee_contact', 'caller_sock', 'callee_stock', 'state', 'start_time', 'timeout', 'sflags', 'iflags', 'toroute_name', 'req_uri', 'xdata']


class DialogVarForm(forms.ModelForm):
    class Meta:
        model = DialogVar
        fields = ['hash_entry', 'hash_id', 'dialog_key', 'dialog_value']



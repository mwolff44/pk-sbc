from django.contrib import admin
from django import forms
from .models import Dialog, DialogVar

class DialogAdminForm(forms.ModelForm):

    class Meta:
        model = Dialog
        fields = '__all__'


class DialogAdmin(admin.ModelAdmin):
    form = DialogAdminForm
    list_display = ['hash_entry', 'hash_id', 'callid', 'from_uri', 'from_tag', 'to_uri', 'to_tag', 'caller_cseq', 'callee_cseq', 'caller_route_set', 'callee_route_set', 'caller_contact', 'callee_contact', 'caller_sock', 'callee_stock', 'state', 'start_time', 'timeout', 'sflags', 'iflags', 'toroute_name', 'req_uri', 'xdata']
    readonly_fields = ['hash_entry', 'hash_id', 'callid', 'from_uri', 'from_tag', 'to_uri', 'to_tag', 'caller_cseq', 'callee_cseq', 'caller_route_set', 'callee_route_set', 'caller_contact', 'callee_contact', 'caller_sock', 'callee_stock', 'state', 'start_time', 'timeout', 'sflags', 'iflags', 'toroute_name', 'req_uri', 'xdata']

admin.site.register(Dialog, DialogAdmin)


class DialogVarAdminForm(forms.ModelForm):

    class Meta:
        model = DialogVar
        fields = '__all__'


class DialogVarAdmin(admin.ModelAdmin):
    form = DialogVarAdminForm
    list_display = ['hash_entry', 'hash_id', 'dialog_key', 'dialog_value']
    readonly_fields = ['hash_entry', 'hash_id', 'dialog_key', 'dialog_value']

admin.site.register(DialogVar, DialogVarAdmin)



from django.contrib import admin
from django import forms
from .models import Acc, AccCdr, MissedCall

class AccAdminForm(forms.ModelForm):

    class Meta:
        model = Acc
        fields = '__all__'


class AccAdmin(admin.ModelAdmin):
    form = AccAdminForm
    list_display = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time', 'time_attr', 'time_exten']
    readonly_fields = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time', 'time_attr', 'time_exten']

admin.site.register(Acc, AccAdmin)


class AccCdrAdminForm(forms.ModelForm):

    class Meta:
        model = AccCdr
        fields = '__all__'


class AccCdrAdmin(admin.ModelAdmin):
    form = AccCdrAdminForm
    list_display = ['start_time', 'end_time', 'duration']
    readonly_fields = ['start_time', 'end_time', 'duration']

admin.site.register(AccCdr, AccCdrAdmin)


class MissedCallAdminForm(forms.ModelForm):

    class Meta:
        model = MissedCall
        fields = '__all__'


class MissedCallAdmin(admin.ModelAdmin):
    form = MissedCallAdminForm
    list_display = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time']
    readonly_fields = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time']

admin.site.register(MissedCall, MissedCallAdmin)

# -*- coding: utf-8 -*-
from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from import_export.admin import ExportMixin
from import_export.formats import base_formats


from .models import CDR, DimDate, DimCustomerHangupcause, DimCustomerSipHangupcause, DimProviderHangupcause, DimProviderSipHangupcause, DimCustomerDestination, DimProviderDestination


DEFAULT_FORMATS = (base_formats.CSV, )


class CDRAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['start_time', 'customer', 'direction', 'caller_number', 'callee_number', 'min_effective_duration', 'provider', 'call_class', 'sip_rtp_rxstat', 'margin', 'sip_code_colored']
    search_fields = ('caller_number', 'callee_number', '^customer__company__name', '^provider__company__name')
    ordering = ('-start_time',)
    list_filter = ('start_time',)

    fieldsets = (
        (_(u'General'), {
            'fields': (('customer', 'provider'),
                       ('start_time', 'direction', 'call_class'),
                       ('callee_number', 'callee_destination'),
                       ('caller_number', 'caller_destination'),
                       'duration')
        }),
        (_(u'Advanced date / duration infos'), {
            'fields': (('answered_time', 'end_time'))
        }),
        (_(u'Financial infos'), {
            'fields': (('total_cost', 'cost_rate', 'costsec'),
                       ('total_sell', 'rate', 'billsec'))
        }),
        (_(u'Call detailed infos'), {
            'fields': (('sip_rtp_rxstat', 'sip_rtp_txstat'),
                       ('sip_code', 'sip_reason', 'hangup_disposition'),
                       ('read_codec', 'write_codec'),
                       'sip_charge_info',
                       ('aleg_uuid', 'cdr_acc'),
                       ('kamailio_server', 'media_server'))
        }),
    )

    actions = None
    has_add_permission = False
    has_delete_permission = False
    log_change = False
    message_user = False
    save_model = False
    show_full_result_count = False
    view_on_site = False

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many] +
            ['min_effective_duration']
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_export_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_export()]


admin.site.register(CDR, CDRAdmin)


""" class DimDateAdminForm(forms.ModelForm):

    class Meta:
        model = DimDate
        fields = '__all__' """


class DimDateAdmin(admin.ModelAdmin):
    # form = DimDateAdminForm
    list_display = ['date', 'day', 'day_of_week', 'hour', 'month', 'quarter', 'year']
    readonly_fields = ['date', 'day', 'day_of_week', 'hour', 'month', 'quarter', 'year']


admin.site.register(DimDate, DimDateAdmin)


""" class DimCustomerHangupcauseAdminForm(forms.ModelForm):

    class Meta:
        model = DimCustomerHangupcause
        fields = '__all__' """


class DimCustomerHangupcauseAdmin(admin.ModelAdmin):
    # form = DimCustomerHangupcauseAdminForm
    list_display = ['hangupcause', 'total_calls', 'direction']
    readonly_fields = ['hangupcause', 'total_calls', 'direction']


admin.site.register(DimCustomerHangupcause, DimCustomerHangupcauseAdmin)


# class DimCustomerSipHangupcauseAdminForm(forms.ModelForm):

#     class Meta:
#         model = DimCustomerSipHangupcause
#         fields = '__all__'

# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CustomerEndpoint, Codec, ProviderEndpoint


class CustomerEndpointAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerEndpoint
        fields = '__all__'


class CustomerEndpointAdmin(admin.ModelAdmin):
    form = CustomerEndpointAdminForm
    list_display = ['name', 'domain', 'customer', 'registration', 'sip_ip', 'max_calls', 'calls_per_second', 'enabled']
    readonly_fields = ['created', 'modified', 'ha1', 'ha1b']
    ordering = ['customer', 'enabled', 'name']
    list_filter = ['enabled']
    search_fields = ['^sip_ip', '^customer__company__name', '^name']
    save_on_top = True
    exclude = ['ha1', 'ha1b']
    affix = True
    fieldsets = (
        (_(u'general'), {
            'fields': (('customer',
                        'enabled'),
                       ('registration','password'),
                       ('name', 'domain'),
                       'codec_list',
                       'transcoding_allowed',),
            'description': _(u'general sip account informations')
        }),
        (_(u'IP Settings'), {
            'fields': (('sip_ip', 'sip_port', 'sip_transport'),
                       'rtp_ip', 'rtp_transport', 'rtp_tos'),
            'classes': ('collapse',),
            'description': _(u'If no registration, SIP IP CIDR is needed')
        }),
        (_(u'caller/callee settings'), {
            'fields': (('outbound_caller_id_name',
                        'outbound_caller_id_number'),
                       ('force_caller_id','masq_caller_id'),
                       ('pai', 'ppi', 'pid'),
                       ('callerid_norm', 'callerid_norm_in'),
                       ('callee_norm', 'callee_norm_in'),),
            'classes': ('collapse',),
            'description': _(u'caller/callee parameters')
        }),
        (_(u'limit settings'), {
            'fields': ('max_calls',
                       'calls_per_second'),
            'classes': ('collapse',),
            'description': _(u'limit settings')
        }),
        (_(u'recording settings'), {
            'fields': (('recording_allowed',
                       'recording_always'),
                       ('recording_limit',
                       'recording_retention'),),
            'classes': ('collapse',),
            'description': _(u'recording parameters')
        }),
        (_(u'advanced settings'), {
            'fields': ('fake_ring',
                       'cli_debug'),
            'classes': ('collapse',),
            'description': _(u'advanced parameters')
        }),
        # (_(u'Urgency settings'), {
        #     'fields': ('urgency_numbr',
        #                'insee_code'),
        #     'classes': ('collapse',),
        #     'description': _(u'Urgency routing numbers parameters')
        # }),
        (_(u'more'), {
            'fields': ('description',
                       ('created', 'modified'),),
            'classes': ('collapse',),
            'description': _(u'more informations')
        }),
    )

admin.site.register(CustomerEndpoint, CustomerEndpointAdmin)


class CodecAdminForm(forms.ModelForm):

    class Meta:
        model = Codec
        fields = '__all__'


class CodecAdmin(admin.ModelAdmin):
    form = CodecAdminForm
    list_display = ['name', 'number', 'ptime', 'stereo', 'rfc_name']
    # readonly_fields = ['created', 'modified', 'number', 'ptime', 'stereo', 'rfc_name', 'description']

admin.site.register(Codec, CodecAdmin)


class ProviderEndpointAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderEndpoint
        fields = '__all__'


class ProviderEndpointAdmin(admin.ModelAdmin):
    form = ProviderEndpointAdminForm
    list_display = ['name', 'provider', 'register', 'sip_proxy', 'prefix', 'max_calls', 'calls_per_second', 'enabled']
    readonly_fields = ['created', 'modified']
    ordering = ['provider', 'enabled', 'name']
    list_filter = ['enabled']
    search_fields = ['^sip_proxy', '^provider__company__name', '^name']
    save_on_top = True
    affix = True
    fieldsets = (
        (_(u'general'), {
            'fields': (('name', 'provider', 'enabled'),
                       ('sip_proxy', 'register'),
                       ('uacreg'),
                       #('username', 'password'),
                       #'realm',
                       #'from_domain',
                       #('expire_seconds', 'retry_seconds'),
                       ('prefix', 'suffix'),
                       'codec_list',),
            'description': _(u'general sip account informations')
        }),
        (_(u'protocol settings'), {
            'fields': (('sip_port', 'sip_transport'),
                       ('rtp_transport', 'rtp_tos')),
            'classes': ('collapse',),
            'description': _(u'If no registration, SIP IP CIDR is needed')
        }),
        (_(u'caller/callee settings'), {
            'fields': (('add_plus_in_caller'),
                       ('caller_id_in_from', 'pai', 'ppi', 'pid'),
                       ('callerid_norm', 'callerid_norm_in'),
                       ('callee_norm', 'callee_norm_in'),),
            'classes': ('collapse',),
            'description': _(u'caller/callee parameters')
        }),
        (_(u'limit settings'), {
            'fields': ('max_calls',
                       'calls_per_second'),
            'classes': ('collapse',),
            'description': _(u'limit settings')
        }),
        (_(u'more'), {
            'fields': (('created', 'modified'),),
            'classes': ('collapse',),
            'description': _(u'more informations')
        }),
    )

admin.site.register(ProviderEndpoint, ProviderEndpointAdmin)

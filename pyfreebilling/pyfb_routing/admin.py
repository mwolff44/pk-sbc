# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from pyfb_company.models import Customer
from pyfb_company.admin import CustomerAdmin

from pyfb_rating.models import ProviderRatecard
from pyfb_rating.admin import CustomerRCAdmin, CustomerRcAllocationInline

from .models import CustomerRoutingGroup, RoutingGroup, PrefixRule, DestinationRule, CountryTypeRule, CountryRule, RegionTypeRule, RegionRule, DefaultRule


class CustomerRAllocationInline(admin.TabularInline):
    model = CustomerRoutingGroup
    fields = ['customer', 'routinggroup', 'description']
    description = _(u'select the Routing group to be affected to customer account !')
    max_num = 1
    extra = 0
    modal = True


class CustomerRAdmin(CustomerAdmin):
    inlines = [CustomerRcAllocationInline, CustomerRAllocationInline]

admin.site.unregister(Customer)
admin.site.register(Customer, CustomerRAdmin)


class CustomerRoutingGroupAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerRoutingGroup
        fields = '__all__'


class CustomerRoutingGroupAdmin(admin.ModelAdmin):
    form = CustomerRoutingGroupAdminForm
    fields = ['customer', 'routinggroup', 'description']
    list_display = ['customer', 'routinggroup', 'description']
    list_filter = ['customer', 'routinggroup']
    #readonly_fields = ['description']

admin.site.register(CustomerRoutingGroup, CustomerRoutingGroupAdmin)


class PrefixRuleInline(admin.TabularInline):
    model = PrefixRule
    fields = ['provider_ratecard', 'prefix', 'destnum_length', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_ratecard', 'provider_gateway_list']


class DestinationRuleInline(admin.TabularInline):
    model = DestinationRule
    fields = ['provider_ratecard', 'destination', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_ratecard', 'destination', 'provider_gateway_list']


class CountryTypeRuleInline(admin.TabularInline):
    model = CountryTypeRule
    fields = ['provider_ratecard', 'country', 'type', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_gateway_list']


class CountryRuleInline(admin.TabularInline):
    model = CountryRule
    fields = ['provider_ratecard', 'country', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_gateway_list']


class RegionTypeRuleInline(admin.TabularInline):
    model = RegionTypeRule
    fields = ['provider_ratecard', 'region', 'type', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_gateway_list']


class RegionRuleInline(admin.TabularInline):
    model = RegionRule
    fields = ['provider_ratecard', 'region', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_gateway_list']


class DefaultRuleInline(admin.TabularInline):
    model = DefaultRule
    fields = ['provider_ratecard', 'route_type', 'weight', 'priority', 'provider_gateway_list', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0
    autocomplete_fields = ['provider_gateway_list']


class RoutingGroupAdminForm(forms.ModelForm):

    class Meta:
        model = RoutingGroup
        fields = '__all__'


class RoutingGroupAdmin(admin.ModelAdmin):
    form = RoutingGroupAdminForm
    list_display = ['id', 'name', 'status', 'created', 'modified']
    readonly_fields = ['slug', 'status_changed', 'created', 'modified']
    list_filter = ['status']
    search_fields = ['description', '^name']
    fieldsets = (
        (_(u'Ratecard details'), {
            'fields': (
                ('name', 'status'),
            ),
        }),
        (_(u'More -- view description and event dates'), {
            'fields': (
                'description',
                ('created', 'modified'),
                'status_changed',
            ),
            'classes': ('collapse',),
        }),
    )
    inlines = [
        PrefixRuleInline,
        DestinationRuleInline,
        CountryTypeRuleInline,
        CountryRuleInline,
        RegionTypeRuleInline,
        RegionRuleInline,
        DefaultRuleInline,
    ]

admin.site.register(RoutingGroup, RoutingGroupAdmin)


class PrefixRuleAdminForm(forms.ModelForm):

    class Meta:
        model = PrefixRule
        fields = '__all__'


class PrefixRuleAdmin(admin.ModelAdmin):
    form = PrefixRuleAdminForm
    list_display = ['prefix', 'destnum_length', 'status', 'route_type', 'weight', 'priority']
    readonly_fields = ['prefix', 'destnum_length', 'status', 'route_type', 'weight', 'priority']

admin.site.register(PrefixRule, PrefixRuleAdmin)


class DestinationRuleAdminForm(forms.ModelForm):

    class Meta:
        model = DestinationRule
        fields = '__all__'


class DestinationRuleAdmin(admin.ModelAdmin):
    form = DestinationRuleAdminForm
    list_display = ['status', 'route_type', 'weight', 'priority']
    readonly_fields = ['status', 'route_type', 'weight', 'priority']

admin.site.register(DestinationRule, DestinationRuleAdmin)


class CountryTypeRuleAdminForm(forms.ModelForm):

    class Meta:
        model = CountryTypeRule
        fields = '__all__'


class CountryTypeRuleAdmin(admin.ModelAdmin):
    form = CountryTypeRuleAdminForm
    list_display = ['status', 'route_type', 'weight', 'priority']
    readonly_fields = ['status', 'route_type', 'weight', 'priority']

admin.site.register(CountryTypeRule, CountryTypeRuleAdmin)


class CountryRuleAdminForm(forms.ModelForm):

    class Meta:
        model = CountryRule
        fields = '__all__'


class CountryRuleAdmin(admin.ModelAdmin):
    form = CountryRuleAdminForm
    list_display = ['status', 'route_type', 'weight', 'priority']
    readonly_fields = ['status', 'route_type', 'weight', 'priority']

admin.site.register(CountryRule, CountryRuleAdmin)


class RegionTypeRuleAdminForm(forms.ModelForm):

    class Meta:
        model = RegionTypeRule
        fields = '__all__'


class RegionTypeRuleAdmin(admin.ModelAdmin):
    form = RegionTypeRuleAdminForm
    list_display = ['status', 'route_type', 'weight', 'priority']
    readonly_fields = ['status', 'route_type', 'weight', 'priority']

admin.site.register(RegionTypeRule, RegionTypeRuleAdmin)


class RegionRuleAdminForm(forms.ModelForm):

    class Meta:
        model = RegionRule
        fields = '__all__'


class RegionRuleAdmin(admin.ModelAdmin):
    form = RegionRuleAdminForm
    list_display = ['status', 'route_type', 'weight', 'priority']
    readonly_fields = ['status', 'route_type', 'weight', 'priority']

admin.site.register(RegionRule, RegionRuleAdmin)


class DefaultRuleAdminForm(forms.ModelForm):

    class Meta:
        model = DefaultRule
        fields = '__all__'


class DefaultRuleAdmin(admin.ModelAdmin):
    form = DefaultRuleAdminForm
    list_display = ['status', 'route_type', 'weight', 'priority']
    readonly_fields = ['status', 'route_type', 'weight', 'priority']

admin.site.register(DefaultRule, DefaultRuleAdmin)

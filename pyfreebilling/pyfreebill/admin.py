# -*- coding: utf-8 -*-
# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

from django.contrib import admin
from django.contrib import messages
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from django.db.models.functions import Trunc, Coalesce
from django.db.models import DateTimeField, Sum, Avg, Count, Max, Min, Value as V
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.contrib.admin.views.main import ChangeList
from django.forms.models import BaseInlineFormSet
from django.template import Context, loader
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportMixin, ImportMixin
from import_export.formats import base_formats

import datetime

from pyfreebilling.antifraud.models import Fraud

from pyfreebilling.switch import esl
from pyfreebilling.switch.models import VoipSwitchProfile

from pyfreebilling.customerdirectory.models import CustomerDirectory

from .models import *
from .forms import CustomerRateCardsAdminForm, CompanyAdminForm, CustomerRatesAdminForm, ProviderRatesAdminForm, ProviderTariffAdminForm, RateCardAdminForm, CustomerDirectoryAdminForm
from .resources import CalleridPrefixResource


APP_LABEL = _(u'CDR report')

DEFAULT_FORMATS = (base_formats.CSV, )


# def sofiaupdate(modeladmin, request, queryset):
#     """ generate new sofia xml config file """
#     try:
#         t = loader.get_template('xml/sofia.conf.xml')
#     except IOError:
#         messages.error(request,
#                        _(u"""sofia config xml file update failed. Can not load
#                        template file !"""))
#     sipprofiles = SipProfile.objects.all()
#     accounts = Company.objects.filter(supplier_enabled=True)
#     c = Context({"sipprofiles": sipprofiles, "accounts": accounts})
#     try:
#         f = open('/usr/local/freeswitch/conf/autoload_configs/sofia.conf.xml',
#                  'w')
#         try:
#             f.write(t.render(c))
#             f.close()
#             try:
#                 fs = esl.getReloadGateway()
#                 messages.success(request, _(u"FS successfully reload"))
#             except IOError:
#                 messages.error(request, _(u"""customer sip config xml file update
#                     failed. FS ACL update failed ! Try manually -- %s""" % fs))
#         finally:
#             #f.close()
#             messages.success(request, _(u"sofia config xml file update success"))
#     except IOError:
#         messages.error(request, _(u"""sofia config xml file update failed. Can
#             not create file !"""))
# sofiaupdate.short_description = _(u"update sofia config xml file")
#
#
# def aclupdate(modeladmin, request, queryset):
#     """ generate new ACL xml config file """
#     try:
#         t = loader.get_template('xml/acl.conf.xml')
#     except IOError:
#         messages.error(request, _(u"""ACL config xml file update failed. Can
#             not load template file !"""))
#     acllists = AclLists.objects.all()
#     aclnodes = AclNodes.objects.all()
#     c = Context({"acllists": acllists, "aclnodes": aclnodes})
#     try:
#         f = open('/usr/local/freeswitch/conf/autoload_configs/acl.conf.xml',
#                  'w')
#         try:
#             f.write(t.render(c))
#             f.close()
#             try:
#                 fs = esl.getReloadACL()
#                 messages.success(request, _(u"FS successfully reload"))
#             except IOError:
#                 messages.error(request, _(u"""ACL config xml file update failed.
#                     FS ACL update failed ! Try manually--- %s""" % fs))
#         finally:
#             messages.success(request, _(u"ACL config xml file update success"))
#     except IOError:
#         messages.error(request, _(u"""ACL xml file update failed. Can not
#             create file !"""))
# aclupdate.short_description = _(u"update ACL config xml file")
#
#
# admin.site.add_action(sofiaupdate, _(u"generate sofia configuration file"))
# admin.site.add_action(aclupdate, _(u"generate acl configuration file"))

# Company - Contatcs


class AntiFraudInline(admin.TabularInline):
    model = Fraud
    collapse = True
    max_num = 1
    description = _(u'AntiFraud system parameters')
    readonly_fields = ('high_amount_alert_sent',
                       'high_minutes_alert_sent',
                       'account_blocked_alert_sent')


class CustomerDirectoryInline(GenericStackedInline):
    model = CustomerDirectory
    extra = 0


class EmailAddressInline(GenericTabularInline):
    model = EmailAddress
    extra = 0
    collapse = True


class PhoneNumberInline(GenericTabularInline):
    model = PhoneNumber
    extra = 0
    collapse = True


class WebSiteInline(GenericTabularInline):
    model = WebSite
    extra = 0
    collapse = True


class StreetAddressInline(GenericStackedInline):
    model = StreetAddress
    extra = 0
    collapse = True
    modal = True


class CustomerRateCardsInline(admin.TabularInline):
    model = CustomerRateCards
    description = _(u'select the Ratecards affected to customer account. Order is important !')
    form = CustomerRateCardsAdminForm
    max_num = 7
    extra = 0
    modal = True
    # sortable = True
    # sortable_order_field = 'priority'


class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        CustomerRateCardsInline,
        AntiFraudInline,
        #CustomerDirectoryInline,
        PhoneNumberInline,
        EmailAddressInline,
        WebSiteInline,
        StreetAddressInline,
    ]
    # form = CompanyAdminForm
    save_on_top = True
    title_icon = 'fa-group'

    search_fields = ['^name', ]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = (
        'customer_balance',
        'supplier_balance',
        'vat_number_validated'
    )
    fieldsets = (
        (_(u'General'), {
            'fields': (('name', 'nickname'),
                       ('slug', 'about'),
                       'account_number',
                       ('vat', 'vat_number'),
                       'vat_number_validated'),
            'description': _(u'General company informations')
        }),
        (_(u'Customer settings'), {
            'fields': ('customer_enabled',
                       ('max_calls', 'calls_per_second'),
                       'billing_cycle',
                       ('prepaid', 'credit_limit'),
                       ('customer_balance',)),
        }),
        (_(u'Customer alerts'), {
            'fields': ('low_credit_alert',
                       'email_alert',
                       'low_credit_alert_sent',
                       'account_blocked_alert_sent'),
            'classes': ('collapse',),
            'description': _(u'All the customer alert parameters')
        }),
        (_(u'Provider settings'), {
            'fields': ('supplier_enabled',
                       'supplier_balance'),
            'classes': ('collapse',),
            'description': _(u'If this company is your provider, this is right place to manage its parameters')
        }),
    )

    def get_customer_enabled_display(self, obj):
        if obj.customer_enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_customer_enabled_display.short_description = _(u'Customer')
    get_customer_enabled_display.admin_order_field = _(u'customer_enabled')

    def get_supplier_enabled_display(self, obj):
        if obj.supplier_enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_supplier_enabled_display.short_description = _(u'Provider')
    get_supplier_enabled_display.admin_order_field = _(u'provider_enabled')

    def get_prepaid_display(self, obj):
        if obj.prepaid:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_prepaid_display.short_description = _(u'Prepaid')
    get_prepaid_display.admin_order_field = _(u'prepaid')

    def get_vat_display(self, obj):
        if obj.vat:
            return mark_safe('<span class="label label-info"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_vat_display.short_description = _(u'VAT')
    get_vat_display.admin_order_field = _(u'vat')

    def get_vat_number_validated_display(self, obj):
        if obj.vat_number_validated:
            return mark_safe('<span class="label label-info"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_vat_number_validated_display.short_description = _(u'VIES')
    get_vat_number_validated_display.admin_order_field = _(u'vies')

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_actions(self, request):
        if request.user.is_superuser:
            actions = super(CompanyAdmin, self).get_actions(request)
            if 'delete_selected' in actions:
                del actions['delete_selected']
            return actions
        return

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display_links = ['name', ]
            return super(CompanyAdmin, self).changelist_view(request, extra_context=None)
        else:
            self.list_display_links = ['None', ]
            return super(CompanyAdmin, self).changelist_view(request, extra_context=None)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('id',
                    'name',
                    'get_prepaid_display',
                    'get_vat_display',
                    'get_vat_number_validated_display',
                    'get_customer_enabled_display',
                    'customer_balance',
                    'get_supplier_enabled_display',
                    'supplier_balance',
                    'balance_history')
        else:
            return ('name',
                    'get_prepaid_display',
                    'get_customer_enabled_display',
                    'customer_balance')

#     def get_list_filter(self, request):
#         if request.user.is_superuser:
#             #return ('name',)
#             return ['prepaid', 'customer_enabled', 'supplier_enabled']
#         else:
#             return []

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['customer_balance',
                    'supplier_balance',
                    'low_credit_alert_sent',
                    'account_blocked_alert_sent']
        else:
            return ['name',
                    'prepaid',
                    'customer_enabled',
                    'customer_balance',
                    'vat_number',
                    'max_calls',
                    'billing_cycle']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('supplier_enabled')
            self.exclude.append('supplier_balance')
            self.exclude.append('vat')
            self.exclude.append('nickname')
            self.exclude.append('slug')
            self.exclude.append('about')

        return super(CompanyAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(CompanyAdmin, self).get_queryset(request)
        if user.is_superuser:
            return qs
        else:
            usercompany = Person.objects.get(user=user)
        return qs.filter(name=usercompany.company)


class PersonAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberInline,
    ]

    list_display_links = ('first_name',
                          'last_name')
    list_display = ('first_name',
                    'last_name',
                    'company')
    list_filter = ('company', )
    ordering = ('last_name',
                'first_name')
    search_fields = ['^first_name',
                     '^last_name',
                     '^company__name']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class GroupAdmin(admin.ModelAdmin):
    list_display_links = ('name', )
    list_display = ('name',
                    'date_modified')
    ordering = ('-date_modified',
                'name')
    search_fields = ['^name',
                     '^about']
    prepopulated_fields = {'slug': ('name',)}

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class CompanyBalanceHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('company', )
    list_display = ('company',
                    'amount_debited',
                    'amount_refund',
                    'customer_balance',
                    'supplier_balance',
                    'operation_type',
                    'reference',
                    'date_modified')
    ordering = ('-date_modified',
                'company')
    search_fields = ['^company__name',
                     '^reference']

    def save_model(self, request, obj, form, change):
        if change:
            messages.info(request, _(u"No need to update balance"))
        else:
            company = form.cleaned_data['company']
            amount_debited = form.cleaned_data['amount_debited']
            amount_refund = form.cleaned_data['amount_refund']
            if form.cleaned_data['operation_type'] == "customer":
                balance = Company.objects.get(pk=company.id)
                balance.customer_balance = balance.customer_balance - amount_debited + amount_refund
                balance.save()
                obj.customer_balance = balance.customer_balance
            elif form.cleaned_data['operation_type'] == "supplier":
                balance = Company.objects.get(pk=company.id)
                balance.supplier_balance = balance.supplier_balance - amount_debited + amount_refund
                balance.save()
                obj.supplier_balance = balance.supplier_balance
            else:
                pass
            messages.success(request, _(u"balance updated"))
        obj.save()

    fieldsets = (
        (_(u'General'), {
            'fields': ('company',
                       'operation_type',
                       'reference',
                       'description')}),
        (_(u'Amount'), {
            'fields': ('amount_debited',
                       'amount_refund')}),
        (_(u'Balances'), {
            'fields': ('customer_balance',
                       'supplier_balance')}),
    )

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['company', 'operation_type']
        else:
            return []

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        if request.user.is_superuser:
            return
        else:
            return

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created. it's an edit
            return ['company',
                    'amount_debited',
                    'amount_refund',
                    'customer_balance',
                    'supplier_balance',
                    'operation_type']
        else:
            return ['customer_balance', 'supplier_balance']

# CallerID prefix list


class CalleridPrefixAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['calleridprefixlist',
                    'prefix',
                    'date_added',
                    'date_modified']
    ordering = ('calleridprefixlist',
                'prefix')
    list_filter = ('calleridprefixlist', )
    search_fields = ('^prefix', )
    resource_class = CalleridPrefixResource

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_import_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_import()]


class CalleridPrefixListAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'description',
                    'prefix',
                    'date_added',
                    'date_modified']
    ordering = ('name', )
    list_filter = ['name', ]
    search_fields = ('^name',
                     'description')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# Provider Rates


class ProviderRatesFormSet(BaseInlineFormSet):

    def get_queryset(self):
        qs = super(ProviderRatesFormSet, self).get_queryset()
        return qs[:40]


class ProviderRatesInline(admin.TabularInline):
    model = ProviderRates
    formset = ProviderRatesFormSet
    max_count = 40
    extra = 1


class ProviderTariffAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'name',
                    'carrier',
                    'prefix',
                    'quality',
                    'reliability',
                    'date_start',
                    'date_end',
                    'get_boolean_display',
                    'rates']
    ordering = ['name', ]
    readonly_fields = ['id', ]
    form = ProviderTariffAdminForm

    def get_boolean_display(self, obj):
        if obj.enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-warning"><i class="icon-thumbs-down"></i> NO</span>')
    get_boolean_display.short_description = _(u'Enabled')
    get_boolean_display.admin_order_field = _(u'enabled')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class ProviderRatesAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id',
                    'provider_tariff',
                    'destination',
                    'digits',
                    'cost_rate',
                    'block_min_duration',
                    'init_block',
                    'get_boolean_display',
                    'date_added',
                    'date_modified']
    ordering = ['provider_tariff',
                'digits']
    list_filter = ['provider_tariff',
                   'enabled',]
    search_fields = ['^digits',
                     '^destination']
    actions = ['make_enabled',
               'make_disabled']
    form = ProviderRatesAdminForm

    def get_boolean_display(self, obj):
        if obj.enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-warning"><i class="icon-thumbs-down"></i> NO</span>')
    get_boolean_display.short_description = _(u'Enabled')
    get_boolean_display.admin_order_field = _(u'enabled')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def make_enabled(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        if rows_updated == 1:
            message_bit = _(u"1 item was")
        else:
            message_bit = _(u"%s items were") % rows_updated
        self.message_user(request, _(u"%s successfully marked as enabled.") % message_bit)
    make_enabled.short_description = _(u"mark selected items as enabled")

    def make_disabled(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        if rows_updated == 1:
            message_bit = _(u"1 item was")
        else:
            message_bit = _(u"%s items were") % rows_updated
        self.message_user(request, _(u"%s successfully marked as disabled.") % message_bit)
    make_disabled.short_description = _(u"mark selected items as disabled")

    def get_import_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_import()]

    def get_export_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_export()]

# LCR


class LCRProvidersInline(admin.TabularInline):
    model = LCRProviders
#    formset = LCRProvidersFormSet
#    fields = ('rates',)
    extra = 0


class LCRGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'lcrtype']
    ordering = ('name', 'lcrtype')
    list_filter = ('lcrtype',)
    inlines = [
        LCRProvidersInline,
    ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class LCRProvidersAdmin(admin.ModelAdmin):
    list_display = ['lcr', 'provider_tariff', 'rates']
    list_filter = ('lcr',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# Customer Rates


class CustomerRatesFormSet(BaseInlineFormSet):
    def get_queryset(self):
        qs = super(CustomerRatesFormSet, self).get_queryset()
        return qs[:40]


class CustomerRatesInline(admin.TabularInline):
    model = CustomerRates
    #formset = CustomerRatesFormSet
    max_num = 40
    extra = 1


class CustomerRatesAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id',
                    'ratecard',
                    'destination',
                    'prefix',
                    'destnum_length',
                    'rate',
                    'init_block',
                    'block_min_duration',
                    'minimal_time',
                    'get_boolean_display',
                    ]
    ordering = ['ratecard',
                'prefix']
    list_filter = ['ratecard',
                   'enabled']
    search_fields = ['^prefix',
                     '^destination']
    actions = ['make_enabled', 'make_disabled']
    readonly_fields = ['id', ]
    form = CustomerRatesAdminForm

    def get_boolean_display(self, obj):
        if obj.enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-warning"><i class="icon-thumbs-down"></i> NO</span>')
    get_boolean_display.short_description = _(u'Enabled')
    get_boolean_display.admin_order_field = _(u'enabled')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def make_enabled(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        if rows_updated == 1:
            message_bit = _(u"1 item was")
        else:
            message_bit = _(u"%s items were") % rows_updated
        self.message_user(request,
                          _(u"%s successfully marked as enabled.") % message_bit)
    make_enabled.short_description = _(u"mark selected items as enabled")

    def make_disabled(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        if rows_updated == 1:
            message_bit = _(u"1 item was")
        else:
            message_bit = _(u"%s items were") % rows_updated
        self.message_user(request,
                          _(u"%s successfully marked as disabled.") % message_bit)
    make_disabled.short_description = _(u"mark selected items as disabled")

    def get_import_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_import()]

    def get_export_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_export()]


class RateCardAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'name',
                    'rctype',
                    'lcrgroup',
                    'lcr',
                    'get_boolean_display',
                    'rates',
                    'date_start',
                    'date_end',
                    'callerid_filter',
                    'callerid_list']
    ordering = ['name', 'enabled', 'lcrgroup']
    list_filter = ['enabled', 'lcrgroup']
    search_fields = ['description', '^name']
    form = RateCardAdminForm
#     inlines = [
#         CustomerRatesInline,
#     ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_boolean_display(self, obj):
        if obj.enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-warning"><i class="icon-thumbs-down"></i> NO</span>')
    get_boolean_display.short_description = _(u'Enabled')
    get_boolean_display.admin_order_field = _(u'enabled')


class CustomerRateCardsAdmin(admin.ModelAdmin):  # (SortableModelAdmin):
    list_display = ['company',
                    'ratecard',
                    'tech_prefix',
                    'priority',
                    'description']
    ordering = ['company', ]
    raw_id_fields = ('ratecard',)
    list_filter = ['ratecard', 'company']
    search_fields = ['^company__company', ]
    form = form = CustomerRateCardsAdminForm

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


# VoipSwitch

class VoipSwitchProfileInline(admin.TabularInline):
    #  form = RoutesDidForm
    description = 'FS profiles'
    model = VoipSwitchProfile
    modal = True
    extra = 0
    collapse = False


class VoipSwitchAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'ip',
                    'date_added',
                    'date_modified']
    ordering = ['name', ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# SofiaGateway


class SofiaGatewayAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'company',
                    'channels',
                    'proxy',
                    'transport',
                    'sip_port',
                    'get_enabled_display',
                    'get_register_display',
                    'date_modified']
    ordering = ['company',
                'name',
                'proxy']
    list_filter = ['company',
                   'enabled']
    search_fields = ['^company__name',
                     'proxy']
    # actions = [sofiaupdate]

    def get_enabled_display(self, obj):
        if obj.enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_enabled_display.short_description = _(u'Enabled')
    get_enabled_display.admin_order_field = _(u'enabled')

    def get_register_display(self, obj):
        if obj.register:
            return mark_safe('<span class="label label-info"><i class="icon-thumbs-up"></i> ON</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> OFF</span>')
    get_register_display.short_description = _(u'Register')
    get_register_display.admin_order_field = _(u'register')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class SipProfileAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'ext_sip_ip',
                    'sip_ip',
                    'sip_port',
                    'auth_calls',
                    'apply_inbound_acl',
                    'disable_register',
                    'log_auth_failures',
                    'disable_transcoding',
                    'enabled',
                    'date_modified']
    ordering = ['name', ]
    list_filter = ['sip_port', ]
    search_fields = ['^name', ]
    inlines = [VoipSwitchProfileInline, ]
    fieldsets = (
        (_(u'Basic settings'), {
            'fields': (('name', 'sip_port'),
                       ('sip_ip', 'rtp_ip'),
                       ('ext_sip_ip', 'ext_rtp_ip'),
                       'enabled'),
            'description': _(u'General sip profile informations')
        }),
        # ('Media Related Options', {
        #     'fields': (''),
        #     'classes': ('collapse',),
        #     'description': 'Manage Media Related Options'
        # }),
        (_(u'Codecs Related Options'), {
            'fields': ('disable_transcoding',
                       ('inbound_codec_prefs', 'outbound_codec_prefs')),
            'classes': ('collapse',),
            'description': _(u'Manage Codecs Related Options')
        }),
        (_(u'NAT'), {
            'fields': ('aggressive_nat_detection',
                       'NDLB_rec_in_nat_reg_c',
                       'NDLB_force_rport',
                       'NDLB_broken_auth_hash'),
            'classes': ('collapse',),
            'description': _(u'NAT management')
        }),
        (_(u'DTMF Related options'), {
            'fields': ('pass_rfc2833',),
            'classes': ('collapse',),
            'description': _(u'DTMF management')
        }),
        (_(u'SIP Related Options'), {
            'fields': (('enable_timer', 'session_timeout')),
            'classes': ('collapse',),
            'description': _(u'Manage SIP Related Options')
        }),
        (_(u'RTP Related Options'), {
            'fields': ('rtp_rewrite_timestamps',),
            'classes': ('collapse',),
            'description': _(u'Manage RTP Related Options')
        }),
        (_(u'Authentification Authorization'), {
            'fields': ('apply_inbound_acl',
                       'auth_calls',
                       'log_auth_failures'),
            'classes': ('collapse',),
            'description': _(u'Authentification Authorization management')
        }),
        (_(u'Registration'), {
            'fields': ('disable_register',
                       'accept_blind_reg'),
            'classes': ('collapse',),
            'description': _(u'Registration settings management')
        }),
        (_(u'Others'), {
            'fields': ('user_agent',),
            'classes': ('collapse',),
            'description': _(u'Others parameters')
        }),
    )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# AclLists


class AclNodesAdminInline(admin.ModelAdmin):
    list_display = ('company', 'cidr', 'policy', 'list')


class AclListsAdmin(admin.ModelAdmin):
    list_display = ('acl_name', 'default_policy')
    ordering = ['acl_name', 'default_policy']
    list_filter = ['default_policy', ]
    inlines = [AclNodesAdminInline, ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# AclNodes


class AclNodesAdmin(admin.ModelAdmin):
    list_display = ('company', 'cidr', 'policy', 'list')
    ordering = ['company', 'policy', 'cidr']
    list_filter = ['company', 'list']
    search_fields = ['cidr', ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# Hangup Cause


class HangupCauseAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'code', 'enumeration', 'cause', 'description')
    search_fields = ('code', 'enumeration')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class CarrierNormalizationRulesAdmin(admin.ModelAdmin):
    list_display = ('company', 'prefix', 'remove_prefix', 'add_prefix')
    ordering = ('company', 'prefix')
    search_fields = ('^prefix',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class CustomerNormalizationRulesAdmin(admin.ModelAdmin):
    list_display = ('company', 'prefix', 'remove_prefix', 'add_prefix')
    ordering = ('company', 'prefix')
    search_fields = ('^prefix',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class CarrierCIDNormalizationRulesAdmin(admin.ModelAdmin):
    list_display = ('company', 'prefix', 'remove_prefix', 'add_prefix')
    ordering = ('company',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class CustomerCIDNormalizationRulesAdmin(admin.ModelAdmin):
    list_display = ('company', 'prefix', 'remove_prefix', 'add_prefix')
    ordering = ('company',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class DestinationNumberRulesAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'format_num', 'description')
    ordering = ('prefix',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class DimCustomerDestinationAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'destination', 'total_calls', 'success_calls', 'total_duration', 'avg_duration', 'max_duration', 'min_duration', 'total_sell', 'total_cost')
    readonly_fields = ('date', 'customer', 'destination', 'total_calls', 'success_calls', 'total_duration', 'avg_duration', 'max_duration', 'min_duration', 'total_sell', 'total_cost')
    list_filter = ('date', 'customer', 'destination')
    ordering = ('-date', 'customer', 'destination')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class DimProviderDestinationAdmin(admin.ModelAdmin):
    list_display = ('date', 'provider', 'destination', 'total_calls', 'success_calls', 'total_duration', 'avg_duration', 'max_duration', 'min_duration', 'total_sell', 'total_cost')
    readonly_fields = ('date', 'provider', 'destination', 'total_calls', 'success_calls', 'total_duration', 'avg_duration', 'max_duration', 'min_duration', 'total_sell', 'total_cost')
    list_filter = ('date', 'provider', 'destination')
    ordering = ('-date', 'provider', 'destination')
#    list_display = ('get_day_stats',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/sale_summary_change_list.html'
    date_hierarchy = 'date__date'
    search_fields = ('^customer__name',)

    # orderable

    list_filter = (
        'destination',
        'customer__name',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super(SaleSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        def get_next_in_date_hierarchy(request, date_hierarchy):
            if date_hierarchy + '__day' in request.GET:
                return 'day'

            if date_hierarchy + '__month' in request.GET:
                return 'day'

            if date_hierarchy + '__year' in request.GET:
                return 'week'

            return 'month'

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Coalesce(Count('id'), V(0)),  # not OK
            'total_sales': Coalesce(Sum('total_sell'), V(0)),
            'margin': Coalesce(Sum('total_sell'), V(0)) - Coalesce(Sum('total_cost'), V(0)),
            'total_calls': Coalesce(Sum('total_calls'), V(0)),
            'success_calls': Coalesce(Sum('success_calls'), V(0)),
            'total_duration': Coalesce(Sum('total_duration'), V(0)),
            'max_duration': Coalesce(Max('max_duration'), V(0)),
            'min_duration': Coalesce(Min('min_duration'), V(0)),
        }

        summary_stats = qs\
            .values('customer__name')\
            .annotate(**metrics)\
            .order_by('-total_sales')

        response.context_data['summary'] = list(summary_stats)

        summary_totals = dict(
            qs.aggregate(**metrics)
        )
        response.context_data['summary_total'] = summary_totals

        period = get_next_in_date_hierarchy(
            request,
            self.date_hierarchy,
        )
        response.context_data['period'] = period

        metrics2 = {
            'total_sales': Coalesce(Sum('total_sell'), V(0)),
            'margin': Coalesce(Sum('total_sell'), V(0)) - Coalesce(Sum('total_cost'), V(0)),
            'total_calls': Coalesce(Sum('total_calls'), V(0)),
            'success_calls': Coalesce(Sum('success_calls'), V(0)),
            'total_duration': Coalesce(Sum('total_duration'), V(0)),
        }

        summary_over_time = qs.annotate(
            period=Trunc(
                'date__date',
                period,
                output_field=DateTimeField()
            )
        ).values('period').annotate(**metrics2).order_by('period')

        # generate data for graph

        # revenue repartition / 5 customers
        chart_label = []
        chart_data = []
        top5sales = 0
        if len(summary_stats) < 5:
            max_cust = len(summary_stats)
        else:
            max_cust = 5
        for i in range(max_cust):
            chart_label.append(summary_stats[i]['customer__name'])
            chart_data.append(int(summary_stats[i]['total_sales']))
            top5sales = top5sales + int(summary_stats[i]['total_sales'])

        # Add others to graphs
        chart_label.append(_(u'others'))
        chart_data.append(int(summary_totals['total_sales']) - top5sales)

        # transform unicode text to strings
        response.context_data['chart_label'] = map(str, chart_label)
        # Example of datas ["Africa", "Asia", "Europe", "Latin America", "North America"]
        response.context_data['chart_data'] = chart_data
        # Example of datas [2478,5267,734,784,433]
                # response.context_data['chart_color'] = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]

        # timeseries stats
        callvolume_data = []
        successcallvolume_data = []
        timeserie_data = []
        revenue_data = []
        margin_data = []
        for j in range(len(summary_over_time)):
            callvolume_data.append(int(summary_over_time[j]['total_calls']))
            successcallvolume_data.append(int(summary_over_time[j]['success_calls']))
            revenue_data.append(int(summary_over_time[j]['total_sales']))
            margin_data.append(int(summary_over_time[j]['margin']))
            if period == 'day':
                timeserie_data.append(summary_over_time[j]['period'].strftime('%Y-%m-%d'))
            elif period == 'week':
                timeserie_data.append(summary_over_time[j]['period'].strftime('%W'))
            else:
                timeserie_data.append(summary_over_time[j]['period'].strftime('%Y-%b'))

        response.context_data['callvolume_data'] = callvolume_data
        response.context_data['successcallvolume_data'] = successcallvolume_data
        response.context_data['revenue_data'] = revenue_data
        response.context_data['margin_data'] = margin_data
        response.context_data['timeserie_data'] = timeserie_data
        response.context_data['summary_over_time'] = period

        return response


class CostSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/cost_summary_change_list.html'
    date_hierarchy = 'date__date'
    search_fields = ('^provider__name',)

    # orderable

    list_filter = (
        'destination',
        'provider__name',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super(CostSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        def get_next_in_date_hierarchy(request, date_hierarchy):
            if date_hierarchy + '__day' in request.GET:
                return 'day'

            if date_hierarchy + '__month' in request.GET:
                return 'day'

            if date_hierarchy + '__year' in request.GET:
                return 'week'

            return 'month'

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Coalesce(Count('id'), V(0)),  # not OK
            'total_buy': Coalesce(Sum('total_cost'), V(0)),
            'margin': Coalesce(Sum('total_sell'), V(0)) - Coalesce(Sum('total_cost'), V(0)),
            'total_calls': Coalesce(Sum('total_calls'), V(0)),
            'success_calls': Coalesce(Sum('success_calls'), V(0)),
            'total_duration': Coalesce(Sum('total_duration'), V(0)),
            'max_duration': Coalesce(Max('max_duration'), V(0)),
            'min_duration': Coalesce(Min('min_duration'), V(0)),
        }

        summary_stats = qs\
            .values('provider__name')\
            .annotate(**metrics)\
            .order_by('-total_buy')

        response.context_data['summary'] = list(summary_stats)

        # Calculate total line
        summary_totals = dict(
            qs.aggregate(**metrics)
        )
        response.context_data['summary_total'] = summary_totals

        period = get_next_in_date_hierarchy(
            request,
            self.date_hierarchy,
        )
        response.context_data['period'] = period

        # generate period data for graph
        metrics2 = {
            'total_buy': Coalesce(Sum('total_cost'), V(0)),
            'margin': Coalesce(Sum('total_sell'), V(0)) - Coalesce(Sum('total_cost'), V(0)),
            'total_calls': Coalesce(Sum('total_calls'), V(0)),
            'success_calls': Coalesce(Sum('success_calls'), V(0)),
            'total_duration': Coalesce(Sum('total_duration'), V(0)),
        }

        summary_over_time = qs.annotate(
            period=Trunc(
                'date__date',
                period,
                output_field=DateTimeField()
            )
        ).values('period').annotate(**metrics2).order_by('period')

        # generate data for graph

        # revenue repartition / 5 customers
        chart_label = []
        chart_data = []
        top5sales = 0
        if len(summary_stats) < 5:
            max_cust = len(summary_stats)
        else:
            max_cust = 5
        for i in range(max_cust):
            chart_label.append(summary_stats[i]['provider__name'])
            chart_data.append(int(summary_stats[i]['total_buy']))
            top5sales = top5sales + int(summary_stats[i]['total_buy'])

        # Add others to graphs
        chart_label.append(_(u'others'))
        chart_data.append(int(summary_totals['total_buy']) - top5sales)

        # transform unicode text to strings
        response.context_data['chart_label'] = map(str, chart_label)
        # Example of datas ["Africa", "Asia", "Europe", "Latin America", "North America"]
        response.context_data['chart_data'] = chart_data
        # Example of datas [2478,5267,734,784,433]
                # response.context_data['chart_color'] = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]

        # timeseries stats
        callvolume_data = []
        successcallvolume_data = []
        timeserie_data = []
        revenue_data = []
        margin_data = []
        for j in range(len(summary_over_time)):
            callvolume_data.append(int(summary_over_time[j]['total_calls']))
            successcallvolume_data.append(int(summary_over_time[j]['success_calls']))
            revenue_data.append(int(summary_over_time[j]['total_buy']))
            margin_data.append(int(summary_over_time[j]['margin']))
            if period == 'day':
                timeserie_data.append(summary_over_time[j]['period'].strftime('%Y-%m-%d'))
            elif period == 'week':
                timeserie_data.append(summary_over_time[j]['period'].strftime('%W'))
            else:
                timeserie_data.append(summary_over_time[j]['period'].strftime('%Y-%b'))

        response.context_data['callvolume_data'] = callvolume_data
        response.context_data['successcallvolume_data'] = successcallvolume_data
        response.context_data['revenue_data'] = revenue_data
        response.context_data['margin_data'] = margin_data
        response.context_data['timeserie_data'] = timeserie_data
        response.context_data['summary_over_time'] = period

        return response


#----------------------------------------
# register
#----------------------------------------
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CompanyBalanceHistory, CompanyBalanceHistoryAdmin)
admin.site.register(CalleridPrefix, CalleridPrefixAdmin)
admin.site.register(CalleridPrefixList, CalleridPrefixListAdmin)
admin.site.register(ProviderTariff, ProviderTariffAdmin)
admin.site.register(ProviderRates, ProviderRatesAdmin)
admin.site.register(LCRGroup, LCRGroupAdmin)
#admin.site.register(LCRProviders, LCRProvidersAdmin)
admin.site.register(RateCard, RateCardAdmin)
admin.site.register(CustomerRates, CustomerRatesAdmin)
admin.site.register(CustomerRateCards, CustomerRateCardsAdmin)
#admin.site.register(AclLists, AclListsAdmin)
#admin.site.register(AclNodes, AclNodesAdmin)
#admin.site.register(VoipSwitch, VoipSwitchAdmin)
admin.site.register(SipProfile, SipProfileAdmin)
admin.site.register(SofiaGateway, SofiaGatewayAdmin)
#admin.site.register(HangupCause, HangupCauseAdmin)
admin.site.register(CarrierNormalizationRules, CarrierNormalizationRulesAdmin)
admin.site.register(CustomerNormalizationRules,
                    CustomerNormalizationRulesAdmin)
admin.site.register(CarrierCIDNormalizationRules,
                    CarrierCIDNormalizationRulesAdmin)
admin.site.register(CustomerCIDNormalizationRules,
                    CustomerCIDNormalizationRulesAdmin)
admin.site.register(DestinationNumberRules, DestinationNumberRulesAdmin)
#admin.site.register(DimCustomerHangupcause, DimCustomerHangupcauseAdmin)
#admin.site.register(DimCustomerSipHangupcause, DimCustomerSipHangupcauseAdmin)
#admin.site.register(DimProviderHangupcause, DimProviderHangupcauseAdmin)
#admin.site.register(DimProviderSipHangupcause, DimProviderSipHangupcauseAdmin)
admin.site.register(DimCustomerDestination, DimCustomerDestinationAdmin)
admin.site.register(DimProviderDestination, DimProviderDestinationAdmin)
admin.site.register(SaleSummary, SaleSummaryAdmin)
admin.site.register(CostSummary, CostSummaryAdmin)

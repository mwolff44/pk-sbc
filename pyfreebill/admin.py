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

import os
from django.contrib import admin 
from django.db import models
from django import forms
from django.contrib import messages
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ERROR_FLAG, ChangeList
from django.core import serializers
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.template import Context, loader
from django.core.files import File
from django.conf.urls import patterns, url
from django.contrib.admin.widgets import *
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext
from import_export.admin import ImportExportMixin, ExportMixin
from import_export.formats import base_formats
from pyfreebill.models import *
from pyfreebill.forms import CustomerRateCardsForm
from pyfreebill.resources import *
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
import datetime

APP_LABEL = _('CDR report')

DEFAULT_FORMATS = (
            base_formats.CSV,
            )

def sofiaupdate(modeladmin, request, queryset):
    """ generate new sofia xml config file """
    try:
        t = loader.get_template('xml/sofia.conf.xml')
    except IOError:
        messages.error(request, "sofia config xml file update failed. Can not load template file !")
    sipprofiles = SipProfile.objects.all()
    accounts = Company.objects.filter(supplier_enabled=True)
    c = Context({"sipprofiles": sipprofiles, "accounts": accounts})
    try:
        pwd = os.path.dirname(__file__)
        f = open('/usr/local/freeswitch/conf/autoload_configs/sofia.conf.xml', 'w')
        try:
            f.write(t.render(c))
        finally:
            f.close()
            messages.success(request, "sofia config xml file update success")
    except IOError:
        messages.error(request, "sofia config xml file update failed. Can not create file !")
sofiaupdate.short_description = _(u"update sofia config xml file")

def directoryupdate(modeladmin, request, queryset):
    """ generate new directory xml config file """
    try:
        t = loader.get_template('xml/directory.conf.xml')
    except IOError:
        messages.error(request, "customer sip config xml file update failed. Can not load template file !")
    customerdirectorys = CustomerDirectory.objects.filter(company__customer_enabled__exact=True, enabled=True)
    accounts = Company.objects.filter(customer_enabled=True)
    c = Context({"customerdirectorys": customerdirectorys, "accounts": accounts})
    try:
        pwd = os.path.dirname(__file__)
        f = open('/usr/local/freeswitch/conf/directory/default.xml', 'w')
        try:
            f.write(t.render(c))
        finally:
            f.close()
            messages.success(request, "customer sip config xml file update success")
    except IOError:
        messages.error(request, "customer sip config xml file update failed. Can not create file !")
directoryupdate.short_description = _(u"update customer sip config xml file")

admin.site.add_action(directoryupdate, _(u"generate customer sip configuration file"))
admin.site.add_action(sofiaupdate, _(u"generate sofia configuration file"))

# Company - Contatcs

class EmailAddressInline(generic.GenericTabularInline):
    model = EmailAddress
    extra = 1

class PhoneNumberInline(generic.GenericTabularInline):
    model = PhoneNumber
    extra = 1

class InstantMessengerInline(generic.GenericTabularInline):
    model = InstantMessenger
    extra = 1

class WebSiteInline(generic.GenericTabularInline):
    model = WebSite
    extra = 1

class StreetAddressInline(generic.GenericStackedInline):
    model = StreetAddress
    extra = 1

class SpecialDateInline(generic.GenericStackedInline):
    model = SpecialDate
    extra = 1

class CommentInline(generic.GenericStackedInline):
    model = Comment
    ct_fk_field = 'object_pk'
    extra = 1

class CustomerRateCardsInline(admin.TabularInline):
    model = CustomerRateCards
    form = CustomerRateCardsForm
    max_num = 3
    extra = 3

class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        CustomerRateCardsInline,
        PhoneNumberInline,
        EmailAddressInline,
        InstantMessengerInline,
        WebSiteInline,
        StreetAddressInline,
        SpecialDateInline,
        CommentInline,
    ]

#    list_display = ('colored_name', 'prepaid', 'customer_balance', 'supplier_balance')
    search_fields = ['^name',]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('customer_balance', 'supplier_balance')
    fieldsets = (
        ('General', {
            'fields': (('name', 'nickname'), ('slug', 'about'), 'account_number', ('vat', 'vat_number'), ('swift_bic', 'iban'))
        }),
        ('Customer', {
            'fields': ('customer_enabled', 'max_calls', ('prepaid', 'credit_limit', 'customer_balance'), 'billing_cycle')
        }),
        ('Provider', {
            'fields': ('supplier_enabled', 'supplier_balance')
        }),
    )


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
            self.list_display_links = ['colored_name',]
            return super(CompanyAdmin, self).changelist_view(request, extra_context=None)
        else:
            self.list_display_links = ['None',]
            return super(CompanyAdmin, self).changelist_view(request, extra_context=None)

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['colored_name', 'prepaid', 'vat', 'customer_enabled', 'customer_balance', 'supplier_enabled', 'supplier_balance']
        else:
            return ['colored_name', 'prepaid', 'customer_enabled', 'customer_balance']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['prepaid', 'customer_enabled', 'supplier_enabled', 'vat']
        else:
            return []

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['customer_balance', 'supplier_balance']
        else:
            return ['name', 'prepaid', 'customer_enabled', 'customer_balance', 'vat_number', 'max_calls', 'billing_cycle']

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

    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(CompanyAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        else:
            usercompany = Person.objects.get(user=user)
        return qs.filter(name=usercompany.company)

class PersonAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberInline,
        EmailAddressInline,
        InstantMessengerInline,
        WebSiteInline,
        StreetAddressInline,
        SpecialDateInline,
        CommentInline,
        ]

    list_display_links = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'company',)
    list_filter = ('company',)
    ordering = ('last_name', 'first_name')
    search_fields = ['^first_name', '^last_name', '^company__name']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

class GroupAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('name', 'date_modified')
    ordering = ('-date_modified', 'name',)
    search_fields = ['^name', '^about',]
    prepopulated_fields = {'slug': ('name',)}

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

class CompanyBalanceHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('company',)
    list_display = ('company', 'amount_debited', 'amount_refund', 'customer_balance', 'supplier_balance', 'operation_type', 'reference', 'date_modified')
    ordering = ('-date_modified', 'company')
    readonly_fields = ('customer_balance', 'supplier_balance')
    search_fields = ['company', '^reference']

    def save_model(self, request, obj, form, change):
      if change:
        messages.info(request, "No need to update balance")
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
        messages.success(request, "balance updated")
      obj.save()

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
    list_display = ['id', 'name', 'carrier', 'prefix', 'description', 'quality', 'reliability', 'date_start', 'date_end', 'enabled']
    ordering = ['name',]
    readonly_fields = ['id',]
    inlines = [
        ProviderRatesInline,
    ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

class ProviderRatesAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['provider_tariff', 'destination', 'digits', 'cost_rate', 'block_min_duration', 'init_block', 'date_start', 'date_end', 'enabled', 'date_added', 'date_modified']
    ordering = ['provider_tariff', 'digits']
    list_filter = ['provider_tariff', 'enabled', 'destination']
    search_fields = ['^digits', 'date_start', 'date_end', '^destination']
    actions = ['make_enabled', 'make_disabled']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def make_enabled(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        if rows_updated == 1 :    
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as enabled." % message_bit)
    make_enabled.short_description = _(u"mark selected items as enabled")

    def make_disabled(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        if rows_updated == 1 :
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as disabled." % message_bit)
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
    extra = 3

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
    list_display = ['lcr', 'provider_tariff']
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
    formset = CustomerRatesFormSet
    max_num = 40
    extra = 1

class CustomerRatesAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'ratecard', 'destination', 'prefix', 'rate', 'block_min_duration', 'init_block', 'date_start', 'date_end', 'enabled', 'date_added', 'date_modified']
    ordering = ['ratecard', 'prefix']
    list_filter = ['ratecard', 'enabled', 'destination']
    search_fields = ['^prefix', 'date_start', 'date_end', '^destination']
    actions = ['make_enabled', 'make_disabled']
    readonly_fields = ['id',]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def make_enabled(self, request, queryset):
        rows_updated = queryset.update(enabled=True)
        if rows_updated == 1 :
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as enabled." % message_bit)
    make_enabled.short_description = _(u"mark selected items as enabled")

    def make_disabled(self, request, queryset):
        rows_updated = queryset.update(enabled=False)
        if rows_updated == 1 :
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as disabled." % message_bit)
    make_disabled.short_description = _(u"mark selected items as disabled")

    def get_import_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_import()]

    def get_export_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_export()]

class RateCardAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'lcrgroup', 'enabled']
    ordering = ['name', 'enabled', 'lcrgroup']
    list_filter = ['enabled', 'lcrgroup']
    search_fields = ['description', '^name']
    inlines = [
        CustomerRatesInline,
    ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

class CustomerRateCardsAdmin(admin.ModelAdmin):
    list_display = ['company', 'ratecard', 'tech_prefix', 'priority', 'description']
    ordering = ['company',]
    list_filter = ['ratecard', 'company']
    search_fields = ['^company__company',]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# CustomerDirectory
class CustomerDirectoryAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'password', 'rtp_ip', 'sip_ip', 'max_calls', 'enabled', 'description'] 
    ordering = ['company', 'enabled']
    list_filter = ['enabled',]
    search_filter = ['^sip_ip', '^company', '^name']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# VoipSwitch
class VoipSwitchAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip','date_added', 'date_modified']
    ordering = ['name',]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# SofiaGateway
class SofiaGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'sip_profile', 'company', 'channels', 'proxy', 'enabled', 'register', 'date_added', 'date_modified']
    ordering = ['company', 'name', 'proxy']
    list_filter = ['company', 'proxy', 'enabled', 'sip_profile']
    search_fields = ['^company__name', 'proxy']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

class SipProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'ext_rtp_ip', 'ext_sip_ip', 'rtp_ip', 'sip_ip', 'sip_port', 'auth_calls', 'log_auth_failures']
    ordering = ['name',]
    list_filter = ['sip_port',]
    search_fields = ['^name',]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

# AclLists
class AclListsAdmin(admin.ModelAdmin):
    list_display = ('acl_name', 'default_policy')
    ordering = ['acl_name', 'default_policy']
    list_filter = ['default_policy',]

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
    search_fields = ['cidr',]

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

# CDR
class TotalAveragesChangeList(ChangeList):

    def get_min_duration(self, sec_duration):
        if sec_duration:
            min = int(sec_duration / 60)
            sec = int(sec_duration % 60)
        else:
            min = 0
            sec = 0
        return "%02d:%02d" % (min, sec)

    def get_results(self, *args, **kwargs):
        super(TotalAveragesChangeList, self).get_results(*args, **kwargs)
        self.total_sell_total = 0
        self.total_cost_total = 0
        try:
            q = self.result_list.aggregate(total_sell_sum=Sum('total_sell'), total_cost_sum=Sum('total_cost'), effective_duration_sum=Sum('effective_duration'), effective_duration_avg=Avg('effective_duration'))
        except:
            self.total_effective_duration = 0
            self.total_cost_total = 0
            self.total_sell_total = 0
            self.avg_effective_duration = 0
            self.margin = 0
            return
        self.total_effective_duration = q['effective_duration_sum']
        self.total_cost_total = q['total_cost_sum']
        self.total_sell_total = q['total_sell_sum']
        self.avg_effective_duration = q['effective_duration_avg']
        try:
            self.margin = self.total_sell_total - self.total_cost_total
        except:
            self.margin = 0
        self.min_avg_effective_duration = self.get_min_duration(q['effective_duration_avg'])
        self.min_total_effective_duration = self.get_min_duration(q['effective_duration_sum'])

class CDRAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ['^prefix', '^destination_number', '^customer__name', '^cost_destination', '^start_stamp']
    date_hierarchy = 'start_stamp'
    change_list_template = 'admin/pyfreebill/cdr/change_list.html'
    resource_class = CDRResourceExtra
    fieldsets = (
        ('General', {
            'fields': ('customer', 'start_stamp', 'destination_number', ('min_effective_duration', 'billsec'), ('sell_destination', 'cost_destination'))
        }),
        ('Advanced date / duration infos', {
            'classes': ('collapse',),
            'fields': (('answered_stamp', 'end_stamp', 'duration', 'effectiv_duration'))
        }),
        ('Financial infos', {
#            'classes': ('collapse',),
            'fields': (('total_cost', 'cost_rate'), ('total_sell', 'rate'), ('init_block', 'block_min_duration'))
        }),
        ('LCR infos', {
            'classes': ('collapse',),
            'fields': ('prefix',('ratecard_id', 'lcr_group_id'), ('lcr_carrier_id', 'gateway'))
        }),
        ('Call detailed infos', {
            'classes': ('collapse',),
            'fields': ('caller_id_number' , ('hangup_cause', 'hangup_cause_q850', 'hangup_disposition', 'sip_hangup_cause'), ('read_codec', 'write_codec'), 'sip_user_agent', 'customer_ip', ('uuid', 'bleg_uuid', 'chan_name', 'country'))
        }),
    )

    class Media:
        js = ("/media/javascript/list_filter_collapse.js",)

    def has_add_permission(self, request, obj=None):
      return False

    def has_delete_permission(self, request, obj=None):
      return False

    def get_actions(self, request):
        if request.user.is_superuser:
            return
        else:
            return

    def get_changelist(self, request, **kwargs):
        return TotalAveragesChangeList

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            self.list_display_links = ['start_stamp',]
            return super(CDRAdmin, self).changelist_view(request, extra_context=None)
        else:
            self.list_display_links = ['None',]
            return super(CDRAdmin, self).changelist_view(request, extra_context=None)

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ['-start_stamp', 'customer', 'gateway']
        else:
            return ['-start_stamp', 'customer']

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['start_stamp', 'customer', 'sell_destination', 'destination_number', 'min_effective_duration', 'hangup_cause_colored', 'lcr_carrier_id', 'cost_rate', 'rate', 'total_cost', 'total_sell', 'prefix', 'ratecard_id', 'lcr_group_id']
        else:
            return ['start_stamp', 'customer', 'customer_ip', 'sell_destination', 'destination_number', 'min_effective_duration', 'hangup_cause', 'rate', 'total_sell']

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['start_stamp', 'customer', 'lcr_carrier_id', 'ratecard_id', 'hangup_cause', 'sip_hangup_cause', 'sell_destination', 'cost_destination']
        else:
            return ['start_stamp', 'sell_destination']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['customer_ip', 'customer', 'caller_id_number', 'destination_number', 'start_stamp', 'answered_stamp', 'end_stamp', 'duration', 'min_effective_duration', 'billsec', 'hangup_cause', 'hangup_cause_q850', 'gateway', 'lcr_carrier_id', 'prefix', 'country','cost_rate', 'total_cost', 'total_sell', 'rate', 'init_block', 'block_min_duration', 'ratecard_id', 'lcr_group_id', 'uuid', 'bleg_uuid', 'chan_name', 'read_codec', 'write_codec', 'sip_user_agent', 'hangup_disposition', 'effectiv_duration', 'sip_hangup_cause', 'sell_destination', 'cost_destination']
        else:
            return ['start_stamp', 'customer', 'customer_ip', 'sell_destination', 'destination_number', 'min_effective_duration', 'hangup_cause', 'rate', 'total_sell']

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['effectiv_duration', 'effective_duration', 'sip_rtp_rxstat', 'sip_rtp_txstat', 'switchname', 'switch_ipv4']
        if not request.user.is_superuser:
            self.exclude.append('cost_rate')
            self.exclude.append('total_cost')
            self.exclude.append('gateway')
            self.exclude.append('lcr_carrier_id')
            self.exclude.append('lcr_group_id')
            self.exclude.append('cost_destination')
        return super(CDRAdmin, self).get_form(request, obj, **kwargs)

    def queryset(self, request):
        today = date.today()-datetime.timedelta(days=30)
        user = getattr(request, 'user', None)
        qs = super(CDRAdmin, self).queryset(request)
        if user.is_superuser:
            return qs.filter(start_stamp__gte=today)
        else:
            usercompany = Person.objects.get(user=user)
        return qs.filter(customer=usercompany.company).filter(start_stamp__gte=today).filter(effective_duration__gt="0")

    def get_export_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_export()]

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

# STATS
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

# Extranet logs
class LogEntryAdmin(admin.ModelAdmin):
    """ based on djangosnippets.org/snippets/2484/ """
    date_hierarchy = 'action_time'
    readonly_fields = LogEntry._meta.get_all_field_names()+ \
                      ['object_link', 'action_description']
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]
    search_fields = [
        'object_repr',
        'change_message'
    ]
    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'action_description',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'

    def action_description(self, obj):
        action_names = {
            ADDITION: 'Addition',
            DELETION: 'Deletion',
            CHANGE: 'Change',
        }
        return action_names[obj.action_flag]
    action_description.short_description = 'Action'

#    admin.site.disable_action('delete_selected')

#----------------------------------------
# register
#----------------------------------------
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CompanyBalanceHistory, CompanyBalanceHistoryAdmin)
admin.site.register(ProviderTariff, ProviderTariffAdmin)
admin.site.register(ProviderRates, ProviderRatesAdmin)
admin.site.register(LCRGroup, LCRGroupAdmin)
#admin.site.register(LCRProviders, LCRProvidersAdmin)
admin.site.register(RateCard, RateCardAdmin)
admin.site.register(CustomerRates, CustomerRatesAdmin)
admin.site.register(CustomerRateCards, CustomerRateCardsAdmin)
admin.site.register(CustomerDirectory, CustomerDirectoryAdmin)
admin.site.register(AclLists, AclListsAdmin)
#admin.site.register(AclNodes, AclNodesAdmin)
#admin.site.register(VoipSwitch, VoipSwitchAdmin)
admin.site.register(SipProfile, SipProfileAdmin)
admin.site.register(SofiaGateway, SofiaGatewayAdmin)
#admin.site.register(HangupCause, HangupCauseAdmin)
admin.site.register(CDR, CDRAdmin)
admin.site.register(CarrierNormalizationRules, CarrierNormalizationRulesAdmin)
admin.site.register(CustomerNormalizationRules, CustomerNormalizationRulesAdmin)
admin.site.register(CarrierCIDNormalizationRules, CarrierCIDNormalizationRulesAdmin)
admin.site.register(CustomerCIDNormalizationRules, CustomerCIDNormalizationRulesAdmin)
admin.site.register(DestinationNumberRules, DestinationNumberRulesAdmin)
#admin.site.register(DimCustomerHangupcause, DimCustomerHangupcauseAdmin)
#admin.site.register(DimCustomerSipHangupcause, DimCustomerSipHangupcauseAdmin)
#admin.site.register(DimProviderHangupcause, DimProviderHangupcauseAdmin)
#admin.site.register(DimProviderSipHangupcause, DimProviderSipHangupcauseAdmin)
admin.site.register(DimCustomerDestination, DimCustomerDestinationAdmin)
admin.site.register(DimProviderDestination, DimProviderDestinationAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
#admin.site.register()

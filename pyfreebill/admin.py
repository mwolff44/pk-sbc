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
from django.contrib import messages
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.core import serializers
from django.template import Context, loader
from django.core.files import File
from django.utils.translation import ugettext_lazy as _
from pyfreebill.models import Company, Person, Group, PhoneNumber, EmailAddress, InstantMessenger, WebSite, StreetAddress, SpecialDate, CompanyBalanceHistory, LCRGroup, Lcr, RateCard, Rates, CustomerRateCards, CustomerDirectory, AclLists, AclNodes, VoipSwitch, SipProfile, SofiaGateway, CDR

# site-wide actions

def sofiaupdate(modeladmin, request, queryset):
    """ generate new sofia xml config file """
    t = loader.get_template('xml/sofia.conf.xml')
    sipprofiles = SipProfile.objects.all()
    accounts = Company.objects.filter(enabled=True)
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
    t = loader.get_template('xml/directory.conf.xml')
    customerdirectorys = CustomerDirectory.objects.filter(company__enabled__exact=True, enabled=True)
    accounts = Company.objects.filter(enabled=True)
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

class PhoneNumberInline(generic.GenericTabularInline):
    model = PhoneNumber

class InstantMessengerInline(generic.GenericTabularInline):
    model = InstantMessenger

class WebSiteInline(generic.GenericTabularInline):
    model = WebSite

class StreetAddressInline(generic.GenericStackedInline):
    model = StreetAddress

class SpecialDateInline(generic.GenericStackedInline):
    model = SpecialDate

class CommentInline(generic.GenericStackedInline):
    model = Comment
    ct_fk_field = 'object_pk'

class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        PhoneNumberInline,
        EmailAddressInline,
        InstantMessengerInline,
        WebSiteInline,
        StreetAddressInline,
        SpecialDateInline,
        CommentInline,
    ]

    list_display = ('name', 'prepaid', 'balance')
    search_fields = ['^name',]
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('balance',)

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

class GroupAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ('name', 'date_modified')
    ordering = ('-date_modified', 'name',)
    search_fields = ['^name', '^about',]
    prepopulated_fields = {'slug': ('name',)}

class CompanyBalanceHistoryAdmin(admin.ModelAdmin):
    list_display_links = ('company',)
    list_display = ('company', 'amount_debited', 'amount_refund', 'balance', 'reference', 'date_modified')
    ordering = ('-date_modified', 'company')
    readonly_fields = ('balance',)
    search_fields = ['company', '^reference']

    def save_model(self, request, obj, form, change):
      if change:
        messages.info(request, "No need to update balance")
      else:
        company = form.cleaned_data['company']
        amount_debited = form.cleaned_data['amount_debited']
        amount_refund = form.cleaned_data['amount_refund']
        balance = Company.objects.get(pk=company.id)
        balance.balance = balance.balance - amount_debited + amount_refund
        balance.save()
        obj.balance = balance.balance
        messages.success(request, "balance updated")
      obj.save()

# LCR

class LCRGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'lcrtype']
    ordering = ('name', 'lcrtype')
    list_filter = ('lcrtype',)

class LcrAdmin(admin.ModelAdmin):
    list_display = ['country', 'digits', 'cost_rate', 'carrier', 'lead_strip', 'tail_strip', 'prefix', 'suffix', 'lcr_profile', 'quality', 'enabled']
    ordering = ['digits', 'country', 'carrier']
    list_filter = ['enabled', 'carrier']
    search_fields = ['^digits',]

# Rates

class RatesAdmin(admin.ModelAdmin):
    list_display = ['ratecard', 'country', 'prefix', 'rate', 'block_min_duration', 'init_block', 'date_start', 'date_end', 'enabled', 'date_added', 'date_modified']
    ordering = ['ratecard', 'country', 'prefix']
    list_filter = ['ratecard', 'enabled']
    search_fields = ['prefix', 'date_start', 'date_end']
    actions = ['make_enabled', 'make_disabled']

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

class RateCardAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'lcrgroup', 'enabled']
    ordering = ['name', 'enabled', 'lcrgroup']
    list_filter = ['enabled', 'lcrgroup']
    search_fields = ['description', '^name']

class CustomerRateCardsAdmin(admin.ModelAdmin):
    list_display = ['company', 'ratecard', 'tech_prefix', 'priority', 'description']
    ordering = ['company',]
    list_filter = ['ratecard', 'company']
    search_fields = ['^company__company',]

# CustomerDirectory
class CustomerDirectoryAdmin(admin.ModelAdmin):
    list_display = ['company', 'name', 'password', 'rtp_ip', 'sip_ip', 'enabled', 'description'] 
    ordering = ['company', 'enabled']
    list_filter = ['enabled',]
    search_filter = ['^sip_ip', '^company', '^name']

# VoipSwitch
class VoipSwitchAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip','date_added', 'date_modified']
    ordering = ['name',]

# SofiaGateway
class SofiaGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'sip_profile', 'company', 'channels', 'proxy', 'register', 'date_added', 'date_modified']
    ordering = ['company', 'name', 'proxy']
    list_filter = ['company', 'proxy']
    search_fields = ['^company__name', 'proxy']

class SipProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'ext_rtp_ip', 'ext_sip_ip', 'rtp_ip', 'sip_ip', 'sip_port', 'auth_calls', 'log_auth_failures']
    ordering = ['name',]
    list_filter = ['sip_port',]
    search_fields = ['^name',]

# AclLists
class AclListsAdmin(admin.ModelAdmin):
    list_display = ('acl_name', 'default_policy')
    ordering = ['acl_name', 'default_policy']
    list_filter = ['default_policy',]

# AclNodes
class AclNodesAdmin(admin.ModelAdmin):
    list_display = ('company', 'cidr', 'policy', 'list')
    ordering = ['company', 'policy', 'cidr']
    list_filter = ['company', 'list']
    search_fields = ['cidr',]

# CDR
class CDRAdmin(admin.ModelAdmin):
    list_display = ('start_stamp', 'customer', 'caller_id_number', 'destination_number', 'duration', 'billsec', 'hangup_cause', 'hangup_cause_q850', 'gateway', 'lcr_carrier_id', 'cost_rate', 'prefix', 'rate', 'ratecard_id', 'lcr_group_id')
    list_display_links = ('start_stamp',)
#    _links = ('customer', 'gateway', 'lcr_carrier_id', 'ratecard_id', 'lcr_group_id')
    ordering = ['-start_stamp', 'customer', 'gateway']
    list_filter = ['customer', 'gateway', 'lcr_carrier_id']
    search_fields = ['^destination_number', '^company__customer']
    readonly_fields =('customer_ip', 'customer', 'caller_id_number', 'destination_number', 'start_stamp', 'answered_stamp', 'end_stamp', 'duration', 'billsec', 'hangup_cause', 'hangup_cause_q850', 'gateway', 'lcr_carrier_id', 'cost_rate', 'prefix', 'country', 'rate', 'init_block', 'block_min_duration', 'ratecard_id', 'lcr_group_id', 'uuid', 'bleg_uuid', 'chan_name', 'read_codec', 'write_codec', 'sip_user_agent', 'sip_rtp_rxstat', 'sip_rtp_txstat', 'switchname', 'switch_ipv4', 'hangup_disposition')
    list_per_page = 20

    def has_add_permission(self, request, obj=None):
      return False

    def has_delete_permission(self, request, obj=None):
      return False

#    admin.site.disable_action('delete_selected')

#----------------------------------------
# register
#----------------------------------------
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CompanyBalanceHistory, CompanyBalanceHistoryAdmin)
admin.site.register(LCRGroup, LCRGroupAdmin)
admin.site.register(Lcr, LcrAdmin)
admin.site.register(RateCard, RateCardAdmin)
admin.site.register(Rates, RatesAdmin)
admin.site.register(CustomerRateCards, CustomerRateCardsAdmin)
admin.site.register(CustomerDirectory, CustomerDirectoryAdmin)
admin.site.register(AclLists, AclListsAdmin)
admin.site.register(AclNodes, AclNodesAdmin)
admin.site.register(VoipSwitch, VoipSwitchAdmin)
admin.site.register(SipProfile, SipProfileAdmin)
admin.site.register(SofiaGateway, SofiaGatewayAdmin)
admin.site.register(CDR, CDRAdmin)
#admin.site.register()

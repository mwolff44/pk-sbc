import os
from django.contrib import admin 
from django.contrib import messages
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.core import serializers
from django.template import Context, loader
from django.core.files import File
from django.utils.translation import ugettext_lazy as _
from pyfreebill.models import Company, Person, Group, PhoneNumber, EmailAddress, InstantMessenger, WebSite, StreetAddress, SpecialDate, CompanyBalanceHistory, LCRGroup, Lcr, RateCard, Rates, CustomerRateCards, CustomerDirectory, AclLists, AclNodes, SipProfile, SofiaGateway

# site-wide actions

def sofiaupdate(modeladmin, request, queryset):
    """ generate new sofia xml config file """
    t = loader.get_template('xml/sofia.conf.xml')
    sipprofiles = SipProfile.objects.all()
    accounts = Company.objects.filter(enabled=True)
    c = Context({"sipprofiles": sipprofiles, "accounts": accounts})
    try:
        pwd = os.path.dirname(__file__)
        f = open('/usr/local/venv/pyfreebilling/freeswitch/conf/sofia.conf.xml', 'w')
        #f = open(os.path.join(pwd, '../freeswitch/conf/sofia.xml'), 'w')
        try:
            f.write(t.render(c))
            #for line in sofiaxml:
            #    sofiaxmlline = sofiaxml.readline()
            #    f.write(sofiaxmlline)
        finally:
            #sofiaxml.close()
            f.close()
            messages.success(request, "sofia config xml file update success")
    except IOError:
        messages.error(request, "sofia config xml file update failed. Can not create file !")
sofiaupdate.short_description = _(u"update sofia config xml file")

def directoryupdate(modeladmin, request, queryset):
    """ generate new directory xml config file """
    t = loader.get_template('xml/directory.conf.xml')
    customerdirectory = CustomerDirectory.objects.all(enabled=True)
    accounts = Company.objects.filter(enabled=True)
    c = Context({"customerdirectory": customerdirectory, "accounts": accounts})
    try:
        pwd = os.path.dirname(__file__)
        f = open('/usr/local/venv/pyfreebilling/freeswitch/conf/directory.conf.xml', 'w')
        try:
            f.write(t.render(c))
        finally:
            f.close()
            messages.success(request, "customer sip config xml file update success")
    except IOError:
        messages.error(request, "customer sip config xml file update failed. Can not create file !")
sofiaupdate.short_description = _(u"update customer sip config xml file")

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

    list_display = ('name',)
    search_fields = ['^name',]
    prepopulated_fields = {'slug': ('name',)}

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

# SofiaGateway
class SofiaGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'sip_profile', 'company', 'channels', 'proxy', 'register', 'date_added', 'date_modified']
    ordering = ['company', 'name', 'proxy']
    list_filter = ['company', 'proxy']
    search_fields = ['company__name', 'proxy']

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

#----------------------------------------
# register
#----------------------------------------
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(CompanyBalanceHistory)
admin.site.register(LCRGroup)
admin.site.register(Lcr)
admin.site.register(RateCard)
admin.site.register(Rates, RatesAdmin)
admin.site.register(CustomerRateCards)
admin.site.register(CustomerDirectory)
admin.site.register(AclLists, AclListsAdmin)
admin.site.register(AclNodes, AclNodesAdmin)
admin.site.register(SipProfile)
admin.site.register(SofiaGateway, SofiaGatewayAdmin)
#admin.site.register()

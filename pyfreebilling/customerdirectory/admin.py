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

from django.contrib import admin, messages
from django.template import Context, loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

# from pyfreebilling.switch import esl
from pyfreebilling.pyfreebill.models import Company

from .models import CustomerDirectory


# def directoryupdate(modeladmin, request, queryset):
#     """ generate new directory xml config file """
#     try:
#         t = loader.get_template('xml/directory.conf.xml')
#     except IOError:
#         messages.error(request, _(u"""customer sip config xml file update failed.
#             Can not load template file !"""))
#     customerdirectorys = CustomerDirectory.objects.filter(company__customer_enabled__exact=True, enabled=True)
#     accounts = Company.objects.filter(customer_enabled=True)
#     c = Context({"customerdirectorys": customerdirectorys,
#                  "accounts": accounts})
#     try:
#         f = open('/usr/local/freeswitch/conf/directory/default.xml', 'w')
#         try:
#             f.write(t.render(c))
#             f.close()
#             try:
#                 fs = esl.getReloadACL()
#                 messages.success(request, _(u"FS successfully reload"))
#             except IOError:
#                 messages.error(request, _(u"""customer sip config xml file update
#                     failed. FS ACL update failed ! Try manually - %s""" % fs))
#         finally:
#             #f.close()
#             messages.success(request, _(u"""customer sip config xml file update
#                 success"""))
#     except IOError:
#         messages.error(request, _(u"""customer sip config xml file update failed.
#             Can not create file !"""))
# directoryupdate.short_description = _(u"update customer sip config xml file")
#
#
# admin.site.add_action(directoryupdate, _(u"""generate customer sip
#     configuration file"""))

# CustomerDirectory


class CustomerDirectoryAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'company',
                    'domain',
                    'get_registration_display',
                    'sip_ip',
                    'max_calls',
                    'calls_per_second',
                    'get_enabled_display',
                    'get_fake_ring_display',
                    'get_cli_debug_display']
    ordering = ['company', 'enabled', 'name']
    list_filter = (
        'enabled',
        'domain__domain')
    # list_editable = ['max_calls', 'calls_per_second']
    search_fields = ['^sip_ip', '^company__name', '^name']
    exclude = ['vmd', ]
    # actions = [directoryupdate]
    save_on_top = True
    affix = True
    fieldsets = (
        (_(u'General'), {
            'fields': (('company',
                        'enabled'),
                       'registration',
                       ('name',
                        'domain'),
                       'codecs'),
            'description': _(u'General sip account informations')
        }),
        (_(u'Registration settings'), {
            'fields': (('password',
                        'multiple_registrations'),
                       'log_auth_failures'),
            'classes': ('collapse',),
            'description': _(u'If registration, you must set a password')
        }),
        (_(u'IP Settings'), {
            'fields': (('sip_ip',
                        'sip_port'),
                       'rtp_ip'),
            'classes': ('collapse',),
            'description': _(u'If no registration, SIP IP CIDR is needed')
        }),
        (_(u'Caller/Callee settings'), {
            'fields': (('outbound_caller_id_name',
                        'outbound_caller_id_number'),
                       ('force_caller_id','masq_caller_id'),
                       ('callerid_norm', 'callerid_norm_in'),
                       ('callee_norm', 'callee_norm_in'),),
            'classes': ('collapse',),
            'description': _(u'Caller/Callee parameters')
        }),
        (_(u'Limit settings'), {
            'fields': ('max_calls',
                       'calls_per_second'),
            'classes': ('collapse',),
            'description': _(u'Limit settings')
        }),
        (_(u'Advanced settings'), {
            'fields': ('ignore_early_media',
                       'fake_ring',
                       'cli_debug'),
            'classes': ('collapse',),
            'description': _(u'Advanced parameters')
        }),
        (_(u'Urgency settings'), {
            'fields': ('urgency_numbr',
                       'insee_code'),
            'classes': ('collapse',),
            'description': _(u'Urgency routing numbers parameters')
        }),
        (_(u'Description'), {
            'fields': ('description',),
            'classes': ('collapse',),
            'description': _(u'Description informations')
        }),
    )

    def get_registration_display(self, obj):
        if obj.registration:
            return mark_safe('<span class="label label-warning"><i class="icon-ok-sign"></i> Registration</span>')
        return mark_safe('<span class="label label-info"><i class="icon-minus-sign"></i> IP Auth</span>')
    get_registration_display.short_description = _(u'Registration')
    get_registration_display.admin_order_field = _(u'registration')

    def get_enabled_display(self, obj):
        if obj.enabled:
            return mark_safe('<span class="label label-success"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_enabled_display.short_description = _(u'Enabled')
    get_enabled_display.admin_order_field = _(u'enabled')

    def get_fake_ring_display(self, obj):
        if obj.fake_ring:
            return mark_safe('<span class="label label-info"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_fake_ring_display.short_description = _(u'Fake ring')
    get_fake_ring_display.admin_order_field = _(u'fake_ring')

    def get_cli_debug_display(self, obj):
        if obj.cli_debug:
            return mark_safe('<span class="label label-warning"><i class="icon-thumbs-up"></i> YES</span>')
        return mark_safe('<span class="label label-danger"><i class="icon-thumbs-down"></i> NO</span>')
    get_cli_debug_display.short_description = _(u'cli_debug')
    get_cli_debug_display.admin_order_field = _(u'cli_debug')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


admin.site.register(CustomerDirectory, CustomerDirectoryAdmin)

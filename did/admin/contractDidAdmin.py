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

from django import forms

from django.contrib import admin

from yawdadmin import admin_site
from yawdadmin.admin import SortableModelAdmin

from did.models import RoutesDid, ContractDid

from pyfreebill.models import CustomerDirectory


class RoutesDidAdmin(SortableModelAdmin):
    list_display = ('contract_did', 'order', 'type', 'trunk', 'number')
    readonly_fields = ('date_added', 'date_modified')
    list_filter = ('contract_did', )
    ordering = ('contract_did', )
    sortable_order_field = 'order'

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class RoutesDidForm(forms.ModelForm):
    class Meta:
        model = RoutesDid

    def __init__(self, *args, **kwargs):
        super(RoutesDidForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        customer_directories = CustomerDirectory.objects.filter(
            company=instance.contract_did.customer)
                #self.fields['trunk']= self.fields['trunk'].widget
        customer_directory_choices = []
        if customer_directories is None:
            customer_directory_choices.append(('', '---------'))
        for cd in customer_directories:
            customer_directory_choices.append((cd.__unicode__))
        self.fields['trunk'].choices = customer_directory_choices


class RoutesDidInline(admin.StackedInline):
    #form = RoutesDidForm
    description = 'Did routes'
    model = RoutesDid
    modal = True
    extra = 0
    collapse = False


class ContractDidAdmin(admin.ModelAdmin):
    list_display = ('did', 'customer', 'max_channels',
                    'date_modified')
    readonly_fields = ('date_added', 'date_modified')
    list_filter = ('customer',)
    ordering = ('did',)
    inlines = [RoutesDidInline, ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

#----------------------------------------
# register
#----------------------------------------
admin_site.register(RoutesDid, RoutesDidAdmin)
admin_site.register(ContractDid, ContractDidAdmin)

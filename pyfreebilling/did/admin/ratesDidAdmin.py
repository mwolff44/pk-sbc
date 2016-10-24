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

from pyfreebilling.did.models import CustomerRatesDid, ProviderRatesDid


class CustomerRatesDidAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'enabled',
                    'rate',
                    'block_min_duration',
                    'interval_duration',
                    'date_modified')
    readonly_fields = ('date_added', 'date_modified')
    list_display_links = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    save_on_top = True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class ProviderRatesDidAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'provider',
                    'enabled',
                    'rate',
                    'block_min_duration',
                    'interval_duration',
                    'date_modified')
    readonly_fields = ('date_added', 'date_modified')
    list_filter = ('provider',)
    list_display_links = ('name',)
    ordering = ('provider', 'name')
    search_fields = ('provider', 'name')
    save_on_top = True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


#  ----------------------------------------
#   register
#  ----------------------------------------
admin.site.register(CustomerRatesDid, CustomerRatesDidAdmin)
admin.site.register(ProviderRatesDid, ProviderRatesDidAdmin)

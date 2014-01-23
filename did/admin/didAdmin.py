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
from django.utils.safestring import mark_safe

from yawdadmin import admin_site

from did.models import Did, ContractDid


class ContractDidInline(admin.StackedInline):
    description = 'Did affectation'
    model = ContractDid
    extra = 0
    collapse = False


class DidAdmin(admin.ModelAdmin):
    list_display = ('get_reserved', 'number', 'city', 'provider',
                    'max_channels', 'date_modified')
    readonly_fields = ('date_added', 'date_modified')
    list_filter = ('provider',)
    list_display_links = ('number',)
    ordering = ('number',)
    search_fields = ('number',)
    save_on_top = True
    inlines = [ContractDidInline, ]

    def get_reserved(self, obj):
        if ContractDid.objects.get(did=obj):
            return mark_safe("""<span class="label label-success">
                                <i class="icon-thumbs-up">
                                </i> Reserved</span>""")
        return mark_safe("""<span class="label label-danger">
                            <i class="icon-thumbs-down">
                            </i> NO</span>""")
    get_reserved.short_description = 'Reserved'
    get_reserved.admin_order_field = 'reserved'

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

#----------------------------------------
# register
#----------------------------------------
admin_site.register(Did, DidAdmin)

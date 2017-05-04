from __future__ import absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from pyfreebilling.did.resources import DidResource, RoutesDidResource

from pyfreebilling.did.models import RoutesDid


DEFAULT_FORMATS = (base_formats.CSV, )


class RoutesDidAdmin(ImportExportModelAdmin):
    list_display = ('id',
                    'contract_did',
                    'order',
                    'type',
                    'trunk',
                    'number',
                    'description',
                    'date_modified')
    readonly_fields = ('date_added',
                       'date_modified')
    list_filter = ('trunk',)
    list_display_links = ('id', 'contract_did')
    ordering = ('contract_did',)
    search_fields = ('^contract_did__number',)
    resource_class = RoutesDidResource

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_import_formats(self):
        format_csv = DEFAULT_FORMATS
        return [f for f in format_csv if f().can_import()]

#  ----------------------------------------
#  register
#  ----------------------------------------
admin.site.register(RoutesDid, RoutesDidAdmin)

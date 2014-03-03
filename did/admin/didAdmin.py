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
from django.template import Context, loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from yawdadmin import admin_site

from import_export.admin import ImportMixin

from switch import esl

from did.models import Did, RoutesDid
from did.resources import DidResource


def didupdate(modeladmin, request, queryset):
    """ generate new did xml config file """
    try:
        t = loader.get_template('xml/00_did.xml')
    except IOError:
        messages.error(request, """did config xml file update failed.
            Can not load template file !""")
    dids = Did.objects.all()
    c = Context({"dids": dids, })
    try:
        f = open('/usr/local/freeswitch/conf/dialplan/public/00_did.xml', 'w')
        try:
            f.write(t.render(c))
            f.close()
            try:
                esl.getReloadDialplan()
                messages.success(request, "FS successfully reload")
            except IOError:
                messages.error(request, """DID config xml file update failed.
                    FS update failed ! Try manually""")
        finally:
            #f.close()
            messages.success(request, "DID config xml file update success")
    except IOError:
        messages.error(request, """DID config xml file update failed. Can not
            create file !""")
didupdate.short_description = _(u"update DID config xml file")

admin.site.add_action(didupdate, _(u"generate DID configuration file"))


class RoutesDidInline(admin.StackedInline):
    #form = RoutesDidForm
    description = 'Did routes'
    model = RoutesDid
    modal = True
    extra = 0
    collapse = False


class DidAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('number',
                    'city',
                    'provider',
                    'prov_max_channels',
                    'customer',
                    'cust_max_channels',
                    'date_modified')
    readonly_fields = ('date_added',
                       'date_modified')
    list_filter = ('provider',
                   'customer')
    list_display_links = ('number',)
    ordering = ('number',)
    search_fields = ('number',)
    resource_class = DidResource
    inlines = [RoutesDidInline, ]
    actions = [didupdate]

    # def get_reserved(self, obj):
    #     if ContractDid.objects.get(did=obj):
    #         return mark_safe("""<span class="label label-success">
    #                             <i class="icon-thumbs-up">
    #                             </i> Reserved</span>""")
    #     return mark_safe("""<span class="label label-danger">
    #                         <i class="icon-thumbs-down">
    #                         </i> NO</span>""")
    # get_reserved.short_description = 'Reserved'
    # get_reserved.admin_order_field = 'reserved'

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

#----------------------------------------
# register
#----------------------------------------
admin_site.register(Did, DidAdmin)

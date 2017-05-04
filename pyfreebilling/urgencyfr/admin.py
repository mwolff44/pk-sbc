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

from .models import Pdau, Caau, UrgencyNumber, InseeCityCode


class InseeCityCodeAdmin(admin.ModelAdmin):
    search_fields = ['^insee_code', '^city']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class UrgencyNumberAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class CaauAdmin(admin.ModelAdmin):
    search_fields = ['^caau_code', ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False


class PdauAdmin(admin.ModelAdmin):
    list_filter = ('urgencynumber', 'caau')
    search_fields = ['^caau__caau_code', 'insee_code', ]

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

admin.site.register(InseeCityCode, InseeCityCodeAdmin)
admin.site.register(UrgencyNumber, UrgencyNumberAdmin)
admin.site.register(Caau, CaauAdmin)
admin.site.register(Pdau, PdauAdmin)

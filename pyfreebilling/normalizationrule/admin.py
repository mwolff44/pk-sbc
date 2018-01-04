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

from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _

from .models import NormalizationRule, NormalizationGroup, NormalizationRuleGroup, CallMappingRule


class NormalizationRuleGroupInline(TabularInline):
    model = NormalizationRuleGroup
    extra = 0
    collapse = True
    modal = True


class NormalizationRuleAdmin(admin.ModelAdmin):
    ordering = ['name', 'match_exp']
    list_filter = ['match_op', ]
    search_filter = ['^name']
    save_on_top = True


class NormalizationGroupAdmin(admin.ModelAdmin):
    inlines = [NormalizationRuleGroupInline, ]
    list_display = ['id', 'name', 'date_modified']
    ordering = ['name', ]
    search_filter = ['^name']
    save_on_top = True


class NormalizationRuleGroupAdmin(admin.ModelAdmin):
    ordering = ['dpid', 'pr']
    save_on_top = True


class CallMappingRuleAdmin(admin.ModelAdmin):
    ordering = ['dpid', 'pr']
    list_filter = ['attrs', ]
    search_filter = ['^name']
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created. it's an edit
            return ['dpid', ]
        else:
            return ['dpid', ]


admin.site.register(NormalizationGroup, NormalizationGroupAdmin)
admin.site.register(NormalizationRuleGroup, NormalizationRuleGroupAdmin)
admin.site.register(NormalizationRule, NormalizationRuleAdmin)
admin.site.register(CallMappingRule, CallMappingRuleAdmin)

# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import CallMappingRule, NormalizationGrp, NormalizationRule, NormalizationRuleGrp

class CallMappingRuleAdminForm(forms.ModelForm):

    class Meta:
        model = CallMappingRule
        fields = '__all__'


class CallMappingRuleAdmin(admin.ModelAdmin):
    form = CallMappingRuleAdminForm
    ordering = ['dpid', 'pr']
    list_filter = ['attrs', ]
    search_filter = ['^name']
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created. it's an edit
            return ['dpid', ]
        else:
            return ['dpid', ]

admin.site.register(CallMappingRule, CallMappingRuleAdmin)


class NormalizationRuleAdminForm(forms.ModelForm):

    class Meta:
        model = NormalizationRule
        fields = '__all__'


class NormalizationRuleGroupInline(TabularInline):
    model = NormalizationRuleGrp
    extra = 0
    collapse = True
    modal = True


class NormalizationRuleAdmin(admin.ModelAdmin):
    form = NormalizationRuleAdminForm
    ordering = ['name', 'match_exp']
    list_filter = ['match_op', ]
    search_filter = ['^name']
    save_on_top = True

admin.site.register(NormalizationRule, NormalizationRuleAdmin)


class NormalizationGrpAdminForm(forms.ModelForm):

    class Meta:
        model = NormalizationGrp
        fields = '__all__'


class NormalizationGrpAdmin(admin.ModelAdmin):
    form = NormalizationGrpAdminForm
    inlines = [NormalizationRuleGroupInline, ]
    list_display = ['id', 'name', 'modified']
    ordering = ['name', ]
    search_filter = ['^name']
    save_on_top = True

admin.site.register(NormalizationGrp, NormalizationGrpAdmin)


class NormalizationRuleGrpAdminForm(forms.ModelForm):

    class Meta:
        model = NormalizationRuleGrp
        fields = '__all__'


class NormalizationRuleGrpAdmin(admin.ModelAdmin):
    form = NormalizationRuleGrpAdminForm
    ordering = ['dpid', 'pr']
    save_on_top = True

admin.site.register(NormalizationRuleGrp, NormalizationRuleGrpAdmin)

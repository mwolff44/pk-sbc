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
from django import forms
from django.db.models import Count

from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.admin import ImportExportModelAdmin

import easy

from .models import Destination, Prefix, Carrier, Region, Country, Type


class PrefixInline(admin.TabularInline):
    model = Prefix
    extra = 0
    max_num = 0
    readonly_fields = ['prefix', 'created', 'last_updated']


class DestinationAdminForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = '__all__'


class DestinationAdmin(ImportExportMixin, admin.ModelAdmin):
    form = DestinationAdminForm
    list_display = ['name', 'country_iso2', 'carrier', 'type', 'prefix_count', 'created', 'last_updated', ]
    readonly_fields = ['slug', 'created', 'last_updated']
    list_select_related = ['carrier', 'type',]
    inlines = [ PrefixInline, ]
    search_fields = ['name']
    show_full_result_count = False

    def prefix_count(self, obj):
        return obj._prefix_count

    def get_queryset(self, request):
        queryset = super(DestinationAdmin, self).get_queryset(request)
        queryset = queryset.annotate(_prefix_count=Count('prefix', distinct=True))
        return queryset

    #prefix_count.short_description = _('Prefix count')
    #prefix_count.admin_order_field = 'prefix_count'

admin.site.register(Destination, DestinationAdmin)


class PrefixAdminForm(forms.ModelForm):

    class Meta:
        model = Prefix
        fields = '__all__'


class PrefixAdmin(ImportExportMixin, admin.ModelAdmin):
    form = PrefixAdminForm
    # resource_class = PrefixResource
    list_display = ['prefix', 'destination', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']
    list_select_related = ['destination']
    show_full_result_count = False

admin.site.register(Prefix, PrefixAdmin)


class CarrierAdminForm(forms.ModelForm):

    class Meta:
        model = Carrier
        fields = '__all__'


class CarrierAdmin(admin.ModelAdmin):
    form = CarrierAdminForm
    list_display = ['name', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']

admin.site.register(Carrier, CarrierAdmin)


class CountryInline(admin.TabularInline):
    model = Country
    extra = 0
    max_num = 0
    readonly_fields = ['country_iso2', 'created', 'last_updated']


class RegionAdminForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = '__all__'


class RegionAdmin(admin.ModelAdmin):
    form = RegionAdminForm
    inlines = [ CountryInline, ]
    list_display = ['name', 'created', 'last_updated', 'country_count']
    readonly_fields = ['slug', 'created', 'last_updated']

    def country_count(self, obj):
        return obj._country_count

    def get_queryset(self, request):
        queryset = super(RegionAdmin, self).get_queryset(request)
        queryset = queryset.annotate(_country_count=Count('country', distinct=True))
        return queryset

admin.site.register(Region, RegionAdmin)


class CountryAdminForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = '__all__'


class CountryAdmin(ImportExportMixin, admin.ModelAdmin):
    form = CountryAdminForm
    list_display = ['country_iso2', 'region', 'created', 'last_updated', 'destination_count']
    readonly_fields = ['created', 'last_updated']
    list_select_related = ['region',]

    def destination_count(self, obj):
        return obj._destination_count

    def get_queryset(self, request):
        queryset = super(CountryAdmin, self).get_queryset(request)
        queryset = queryset.annotate(_destination_count=Count('country_iso2', distinct=True))
        return queryset

admin.site.register(Country, CountryAdmin)


class TypeAdminForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = '__all__'


class TypeAdmin(admin.ModelAdmin):
    form = TypeAdminForm
    list_display = ['name', 'created', 'last_updated']
    readonly_fields = ['slug', 'created', 'last_updated']

admin.site.register(Type, TypeAdmin)

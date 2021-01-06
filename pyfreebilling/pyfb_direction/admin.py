# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.db.models import Count

from import_export import resources
from import_export.admin import ImportExportMixin
from import_export.admin import ImportExportModelAdmin

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Destination, Prefix, Carrier, Region, Country, Risk, Type


class PrefixInline(admin.TabularInline):
    model = Prefix
    extra = 0
    max_num = 0
    readonly_fields = ['prefix', 'created', 'modified']


class DestinationAdminForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = '__all__'
        widgets = {'country_iso2': CountrySelectWidget()}


class DestinationAdmin(ImportExportMixin, admin.ModelAdmin):
    form = DestinationAdminForm
    list_display = ['name', 'country', 'carrier', 'type', 'prefix_count']
    readonly_fields = ['slug', 'created', 'modified']
    list_select_related = ['carrier', 'type']
    #  list_filter = ['country']
    inlines = [ PrefixInline]
    search_fields = ['^name']
    show_full_result_count = False

    def prefix_count(self, obj):
        return obj._prefix_count

    def get_queryset(self, request):
        queryset = super(DestinationAdmin, self).get_queryset(request)
        queryset = queryset.annotate(_prefix_count=Count('prefix', distinct=True))
        return queryset

    #  prefix_count.short_description = _('Prefix count')
    #  prefix_count.admin_order_field = 'prefix_count'


admin.site.register(Destination, DestinationAdmin)


class PrefixAdminForm(forms.ModelForm):

    class Meta:
        model = Prefix
        fields = '__all__'


class PrefixAdmin(ImportExportMixin, admin.ModelAdmin):
    form = PrefixAdminForm
    # resource_class = PrefixResource
    list_display = ['prefix', 'destination', 'created', 'modified']
    readonly_fields = ['slug', 'created', 'modified']
    list_select_related = ['destination']
    list_filter = ['destination']
    search_fields = ['^prefix', '^destination']
    show_full_result_count = False


admin.site.register(Prefix, PrefixAdmin)


class CarrierAdminForm(forms.ModelForm):

    class Meta:
        model = Carrier
        fields = '__all__'


class CarrierAdmin(admin.ModelAdmin):
    form = CarrierAdminForm
    list_display = ['name', 'created', 'modified']
    readonly_fields = ['slug', 'created', 'modified']
    search_fields = ['^name']


admin.site.register(Carrier, CarrierAdmin)


class CountryInline(admin.TabularInline):
    model = Country
    extra = 0
    max_num = 0
    readonly_fields = ['country_iso2', 'risk', 'created', 'modified']


class RegionAdminForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = '__all__'


class RegionAdmin(admin.ModelAdmin):
    form = RegionAdminForm
    inlines = [CountryInline, ]
    list_display = ['name', 'created', 'modified', 'country_count']
    readonly_fields = ['slug', 'created', 'modified']
    search_fields = ['^name']

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
        widgets = {'country_iso2': CountrySelectWidget()}


class CountryAdmin(ImportExportMixin, admin.ModelAdmin):
    form = CountryAdminForm
    list_display = ['country_iso2', 'region', 'risk', 'destination_count']
    readonly_fields = ['created', 'modified']
    list_filter = ['region', 'risk']
    list_select_related = ['region', 'risk']
    search_fields = ['^region__name', '^country_iso2']

    def destination_count(self, obj):
        return obj._destination_count

    def get_queryset(self, request):
        queryset = super(CountryAdmin, self).get_queryset(request)
        queryset = queryset.annotate(_destination_count=Count('destination', distinct=True))
        return queryset


admin.site.register(Country, CountryAdmin)


class TypeAdminForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = '__all__'


class TypeAdmin(admin.ModelAdmin):
    form = TypeAdminForm
    list_display = ['name', 'created', 'modified']
    readonly_fields = ['slug', 'created', 'modified']


admin.site.register(Type, TypeAdmin)


class RiskAdminForm(forms.ModelForm):

    class Meta:
        model = Type
        fields = '__all__'


class RiskAdmin(admin.ModelAdmin):
    form = RiskAdminForm
    list_display = ['id', 'name', 'created', 'modified']
    readonly_fields = ['id', 'created', 'modified']


admin.site.register(Risk, RiskAdmin)

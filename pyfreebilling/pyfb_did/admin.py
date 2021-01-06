# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from .models import Did, RoutesDid


class RoutesDidInline(admin.TabularInline):
    #  form = RoutesDidForm
    description = 'Did routes'
    model = RoutesDid
    fields = ['order', 'type', 'number', 'trunk', 'weight', 'description']
    modal = True
    extra = 0
    collapse = False


class DidAdminForm(forms.ModelForm):

    class Meta:
        model = Did
        fields = '__all__'


class DidAdmin(admin.ModelAdmin):
    form = DidAdminForm
    fields = ('number',
                    'provider', 'provider_free',
                    'prov_max_channels',
                    'customer', 'customer_free',
                    'cust_max_channels',
                    'description',
                    'created', 'modified')
    list_display = ('id',
                    'number',
                    'provider',
                    'prov_max_channels',
                    'provider_free',
                    'customer',
                    'cust_max_channels',
                    'customer_free',
                    'modified')
    readonly_fields = ('created',
                       'modified')
    list_filter = ('provider',
                   'customer',
                   'provider_free',
                   'customer_free',)
    list_display_links = ('number',)
    ordering = ('number',)
    search_fields = ('number',)
    inlines = [RoutesDidInline, ]
admin.site.register(Did, DidAdmin)


class RoutesDidAdminForm(forms.ModelForm):

    class Meta:
        model = RoutesDid
        fields = ['order', 'type', 'number', 'trunk', 'weight', 'description']


class RoutesDidAdmin(admin.ModelAdmin):
    form = RoutesDidAdminForm
    list_display = ['order', 'type', 'number', 'description', 'created', 'modified', 'weight']
    # readonly_fields = ['order', 'type', 'number', 'description', 'created', 'modified', 'weight']

admin.site.register(RoutesDid, RoutesDidAdmin)

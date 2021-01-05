# -*- coding: utf-8 -*-
from django import forms
from .models import Carrier, Type, Region, Country, Destination, Prefix

from django_countries.widgets import CountrySelectWidget


class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = ['name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name']


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_iso2', 'region']
        widgets = {'country_iso2': CountrySelectWidget()}


class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination
        fields = ['name', 'country_iso2', 'carrier', 'type']
        widgets = {'country_iso2': CountrySelectWidget()}


class PrefixForm(forms.ModelForm):
    class Meta:
        model = Prefix
        fields = ['prefix', 'destination']

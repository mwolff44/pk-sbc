from django import forms
from .models import Destination, Prefix, Carrier, Region, Country, Type


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country_iso2', 'carrier', 'type']


class PrefixForm(forms.ModelForm):
    class Meta:
        model = Prefix
        fields = ['prefix', 'destination']


class CarrierForm(forms.ModelForm):
    class Meta:
        model = Carrier
        fields = ['name']


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name',]


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_iso2', 'region']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

from django import forms
from .models import Did, RoutesDid


class DidForm(forms.ModelForm):
    class Meta:
        model = Did
        fields = ['number', 'prov_max_channels', 'cust_max_channels', 'insee_code', 'description', 'provider_free', 'customer_free', 'provider', 'customer']


class RoutesDidForm(forms.ModelForm):
    class Meta:
        model = RoutesDid
        fields = ['order', 'type', 'number', 'description', 'weight', 'contract_did', 'trunk']

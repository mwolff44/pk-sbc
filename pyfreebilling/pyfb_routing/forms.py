from django import forms

from .models import CustomerRoutingGroup, RoutingGroup, PrefixRule, DestinationRule, CountryTypeRule, CountryRule, RegionTypeRule, RegionRule, DefaultRule


class CustomerRoutingGroupForm(forms.ModelForm):
    class Meta:
        model = CustomerRoutingGroup
        fields = ['description', 'customer', 'routinggroup']

        
class RoutingGroupForm(forms.ModelForm):
    class Meta:
        model = RoutingGroup
        fields = ['name', 'status', 'status_changed', 'description']


class PrefixRuleForm(forms.ModelForm):
    class Meta:
        model = PrefixRule
        fields = ['prefix', 'destnum_length', 'status', 'route_type', 'weight', 'priority', 'c_route', 'provider_ratecard', 'provider_gateway_list']


class DestinationRuleForm(forms.ModelForm):
    class Meta:
        model = DestinationRule
        fields = ['status', 'route_type', 'weight', 'priority', 'c_route', 'destination', 'provider_ratecard', 'provider_gateway_list']


class CountryTypeRuleForm(forms.ModelForm):
    class Meta:
        model = CountryTypeRule
        fields = ['status', 'route_type', 'weight', 'priority', 'c_route', 'country', 'type', 'provider_ratecard', 'provider_gateway_list']


class CountryRuleForm(forms.ModelForm):
    class Meta:
        model = CountryRule
        fields = ['status', 'route_type', 'weight', 'priority', 'c_route', 'country', 'provider_ratecard', 'provider_gateway_list']


class RegionTypeRuleForm(forms.ModelForm):
    class Meta:
        model = RegionTypeRule
        fields = ['status', 'route_type', 'weight', 'priority', 'c_route', 'region', 'type', 'provider_ratecard', 'provider_gateway_list']


class RegionRuleForm(forms.ModelForm):
    class Meta:
        model = RegionRule
        fields = ['status', 'route_type', 'weight', 'priority', 'c_route', 'region', 'provider_ratecard', 'provider_gateway_list']


class DefaultRuleForm(forms.ModelForm):
    class Meta:
        model = DefaultRule
        fields = ['status', 'route_type', 'weight', 'priority', 'c_route', 'provider_ratecard', 'provider_gateway_list']

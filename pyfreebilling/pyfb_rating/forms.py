from django import forms
from .models import CustomerRcAllocation, CallerNumList, ProviderRatecard, CustomerRatecard, CustomerPrefixRate, ProviderPrefixRate, CustomerDestinationRate, ProviderDestinationRate, CustomerCountryTypeRate, ProviderCountryTypeRate, CustomerCountryRate, ProviderCountryRate, CustomerRegionTypeRate, ProviderRegionTypeRate, CustomerRegionRate, ProviderRegionRate, CustomerDefaultRate, ProviderDefaultRate


class CustomerRcAllocationForm(forms.ModelForm):
    class Meta:
        model = CustomerRcAllocation
        fields = ['tech_prefix', 'priority', 'discount', 'allow_negative_margin', 'description', 'customer', 'ratecard']


class CallerNumListForm(forms.ModelForm):
    class Meta:
        model = CallerNumList
        fields = ['name', 'callerid_filter', 'destination']


class ProviderRatecardForm(forms.ModelForm):
    class Meta:
        model = ProviderRatecard
        fields = ['name', 'rc_type', 'provider_prefix', 'estimated_quality', 'date_start', 'date_end', 'status', 'status_changed']


class CustomerRatecardForm(forms.ModelForm):
    class Meta:
        model = CustomerRatecard
        fields = ['rc_type', 'name', 'status', 'status_changed']


class CustomerPrefixRateForm(forms.ModelForm):
    class Meta:
        model = CustomerPrefixRate
        fields = ['prefix', 'destnum_length', 'c_ratecard', 'r_rate', 'status']


class ProviderPrefixRateForm(forms.ModelForm):
    class Meta:
        model = ProviderPrefixRate
        fields = ['prefix', 'destnum_length', 'p_ratecard', 'r_rate', 'status']


class CustomerDestinationRateForm(forms.ModelForm):
    class Meta:
        model = CustomerDestinationRate
        fields = ['c_ratecard', 'destination', 'r_rate', 'status']


class ProviderDestinationRateForm(forms.ModelForm):
    class Meta:
        model = ProviderDestinationRate
        fields = ['p_ratecard', 'destination', 'r_rate', 'status']


class CustomerCountryTypeRateForm(forms.ModelForm):
    class Meta:
        model = CustomerCountryTypeRate
        fields = ['c_ratecard', 'country', 'type', 'r_rate', 'status']


class ProviderCountryTypeRateForm(forms.ModelForm):
    class Meta:
        model = ProviderCountryTypeRate
        fields = ['p_ratecard', 'country', 'type', 'r_rate', 'status']


class CustomerCountryRateForm(forms.ModelForm):
    class Meta:
        model = CustomerCountryRate
        fields = ['c_ratecard', 'country', 'r_rate', 'status']


class ProviderCountryRateForm(forms.ModelForm):
    class Meta:
        model = ProviderCountryRate
        fields = ['p_ratecard', 'country', 'r_rate', 'status']


class CustomerRegionTypeRateForm(forms.ModelForm):
    class Meta:
        model = CustomerRegionTypeRate
        fields = ['c_ratecard', 'region', 'type', 'r_rate', 'status']


class ProviderRegionTypeRateForm(forms.ModelForm):
    class Meta:
        model = ProviderRegionTypeRate
        fields = ['p_ratecard', 'region', 'type', 'r_rate', 'status']


class CustomerRegionRateForm(forms.ModelForm):
    class Meta:
        model = CustomerRegionRate
        fields = ['c_ratecard', 'region', 'r_rate', 'status']


class ProviderRegionRateForm(forms.ModelForm):
    class Meta:
        model = ProviderRegionRate
        fields = ['p_ratecard', 'region', 'r_rate', 'status']


class CustomerDefaultRateForm(forms.ModelForm):
    class Meta:
        model = CustomerDefaultRate
        fields = ['c_ratecard', 'r_rate', 'status']


class ProviderDefaultRateForm(forms.ModelForm):
    class Meta:
        model = ProviderDefaultRate
        fields = ['p_ratecard', 'r_rate', 'status']

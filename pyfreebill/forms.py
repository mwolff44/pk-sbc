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

from django import forms
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from yawdadmin.widgets import AutoCompleteTextInput, Select2MultipleWidget, Select2Widget, SwitchWidget, BootstrapRadioRenderer
from django.contrib.admin import widgets
from pyfreebill.models import CustomerRateCards, CustomerRates, ProviderRates, ProviderTariff, RateCard, CustomerDirectory, CDR


#voip_call_disposition_list = []
#voip_call_disposition_list.append(('all', _('all').upper()))
#for i in VOIPCALL_DISPOSITION:
#    voip_call_disposition_list.append((i[0], i[1]))

class SearchForm(forms.Form):
    """General Search Form with From & To date para."""
    from_date = forms.CharField(label=_('from'), required=False,
                                max_length=10)
    to_date = forms.CharField(label=_('to'), required=False, max_length=10)

class CDRSearchForm(SearchForm):
    """VoIP call Report Search Parameters"""

    def __init__(self, user, *args, **kwargs):
        super(CDRSearchForm, self).__init__(*args, **kwargs)
        # To get user's campaign list which are attached with voipcall
        if user:
            list = []
            list.append((0, _('all').upper()))

class CustomerDirectoryAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'log_auth_failures': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'YES',
                                            'data-off-label': 'NO',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
            'enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'YES',
                                            'data-off-label': 'NO',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
            'fake_ring': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
            'cli_debug': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'warning',
                                            'data-off': 'info'}),
            'registration': SwitchWidget(attrs={'class': 'switch-medium',
                                            'data-on-label': 'Registration',
                                            'data-off-label': 'No: IP/CIDR',
                                            'data-on': 'warning',
                                            'data-off': 'info'}),
        }

class RateCardAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
        }

class ProviderTariffAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
        }

class CustomerRateCardsAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'description': forms.TextInput(attrs={"class" : "input-medium"}), 
            'allow_negative_margin': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'YES',
                                            'data-off-label': 'NO',
                                            'data-on': 'danger',
                                            'data-off': 'success'}),
        }
        

class CustomerRatesAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
        }

class ProviderRatesAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
        }
        
class CompanyAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'max_calls': forms.TextInput(attrs={"class" : "input-small"}),
            'calls_per_second': forms.TextInput(attrs={"class" : "input-small"}),
            'credit_limit': forms.TextInput(attrs={"class" : "input-small"}),
            'vat': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'Yes',
                                            'data-off-label': 'No',
                                            'data-on': 'info',
                                            'data-off': 'warning'}),
            'prepaid': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on': 'success',
                                            'data-off': 'warning'}),
            'low_credit_alert_sent': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'danger',
                                            'data-off': 'success'}),
            'account_blocked_alert_sent': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'danger',
                                            'data-off': 'success'}),
            'customer_enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
            'supplier_enabled': SwitchWidget(attrs={'class': 'switch-small',
                                            'data-on-label': 'ON',
                                            'data-off-label': 'OFF',
                                            'data-on': 'success',
                                            'data-off': 'danger'}),
        }
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
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm, Textarea
from django.contrib.admin import widgets
from pyfreebill.models import CustomerRateCards, CDR


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

class CustomerRateCardsForm(forms.ModelForm):
    """ Used to resize text input in admin form """

    class Meta:
        model = CustomerRateCards
        widgets = {
            'description': Textarea(attrs={'cols': 30, 'rows': 1}),
        }



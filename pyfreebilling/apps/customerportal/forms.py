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

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

from datetimewidget.widgets import DateTimeWidget


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(
        label="Password", required=True, widget=forms.PasswordInput)
    remember = forms.BooleanField(label="Remember Me?")

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('login', 'login', css_class='btn-primary'))


class CartForm(forms.Form):
    item = forms.CharField()
    quantity = forms.IntegerField(label="Qty")
    price = forms.DecimalField()

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
        'item',
        PrependedText('quantity', '#'),
        PrependedAppendedText('price', '$', '.00'),
        FormActions(Submit('login', 'login', css_class='btn-primary'))
    )


class CreditCardForm(forms.Form):
    fullname = forms.CharField(label="Full Name", required=True)
    card_number = forms.CharField(label="Card", required=True, max_length=16)
    expire = forms.DateField(label="Expire Date", input_formats=['%m/%y'])
    ccv = forms.IntegerField(label="ccv")
    notes = forms.CharField(label="Order Notes", widget=forms.Textarea())

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-sm-2'
    helper.field_class = 'col-sm-4'
    helper.layout = Layout(
        Field('fullname', css_class='input-sm'),
        Field('card_number', css_class='input-sm'),
        Field('expire', css_class='input-sm'),
        Field('ccv', css_class='input-sm'),
        Field('notes', rows=3),
        FormActions(Submit('purchase', 'purchase', css_class='btn-primary'))
    )


class CDRSearchForm(forms.Form):
    """VoIP call Report Search Parameters"""
    dateTimeOptions = {
        'format': 'yyyy-dd-mm hh:ii',
        'todayBtn': 'true',
        'usetz': 'true',
        'usel10n': 'true',
        'usei18n': 'true'
    }
    from_date = forms.CharField(
        label=_('From'),
        required=False,
        max_length=20,
        widget=DateTimeWidget(options=dateTimeOptions)
    )
    to_date = forms.CharField(
        label=_('To'),
        required=False,
        max_length=20,
        widget=DateTimeWidget(options=dateTimeOptions)
    )
    dest_num = forms.IntegerField(
        label=_('Destination Number'),
        required=False,
        help_text=_('Enter the full number or the first part')
    )


class RatesForm(forms.Form):
    ratecard = forms.TypedChoiceField(
        label="Select the ratecard",
        choices=((1, "Yes"), (0, "No")),
        widget=forms.RadioSelect,
        initial='1',
        required=True,
    )
    destination = forms.CharField(
        label="Destination",
        max_length="20",
        required=False,
    )
    prefix = forms.IntegerField(
        label='Prefix',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(RatesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'list_rates'
        self.helper.add_input(Submit('submit', 'Submit'))

from django import forms
from django.forms import ModelForm, Textarea
from pyfreebill.models import CustomerRateCards

class CustomerRateCardsForm(forms.ModelForm):
    """ Used to resize text input in admin form """

    class Meta:
        model = CustomerRateCards
        widgets = {
            'description': Textarea(attrs={'cols': 30, 'rows': 1}),
        }

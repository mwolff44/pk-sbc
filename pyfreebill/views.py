from django import forms
from django.forms import ModelForm, Form
from django.contrib.contenttypes.generic import generic_inlineformset_factory as inlineformset_factory

from contacts.models import Company, Person, Group, PhoneNumber, EmailAddress, InstantMessenger, WebSite, StreetAddress, SpecialDate

class CompanyCreateForm(ModelForm):
	class Meta:
		model = Company
		fields = ('name', 'nickname', 'about')

class CompanyUpdateForm(ModelForm):
	class Meta:
		model = Company

class PersonCreateForm(ModelForm):
	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'title', 'company', 'about')

class PersonUpdateForm(ModelForm):
	class Meta:
		model = Person
		fields = ('first_name', 'last_name', 'title', 'company')

class GroupCreateForm(ModelForm):
	class Meta:
		model = Group
		fields = ('name', 'about')

class GroupUpdateForm(ModelForm):
	class Meta:
		model = Group
		exclude = ('slug',)

PhoneNumberFormSet = inlineformset_factory(PhoneNumber, extra=1)
EmailAddressFormSet = inlineformset_factory(EmailAddress, extra=1)
InstantMessengerFormSet = inlineformset_factory(InstantMessenger, extra=1)
WebSiteFormSet = inlineformset_factory(WebSite, extra=1)
StreetAddressFormSet = inlineformset_factory(StreetAddress, extra=1)
SpecialDateFormSet = inlineformset_factory(SpecialDate, extra=1)

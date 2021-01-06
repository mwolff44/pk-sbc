from django import forms
from .models import Company, Customer, Provider, CompanyBalanceHistory


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'contact_name', 'contact_phone']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['account_number', 'credit_limit', 'low_credit_alert', 'max_calls', 'calls_per_second', 'customer_enabled', 'company']


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['supplier_enabled', 'company']


class CompanyBalanceHistoryForm(forms.ModelForm):
    class Meta:
        model = CompanyBalanceHistory
        fields = ['amount_debited', 'amount_refund', 'customer_balance', 'supplier_balance', 'operation_type', 'external_desc', 'internal_desc', 'company']

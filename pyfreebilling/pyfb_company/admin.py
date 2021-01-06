# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Company, Customer, Provider, CompanyBalanceHistory

class CompanyAdminForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = '__all__'


class CompanyAdmin(admin.ModelAdmin):
    save_on_top = True
    form = CompanyAdminForm
    list_display = ['name', 'contact_name', 'contact_phone']
    readonly_fields = ['slug', 'created', 'modified']
    search_fields = ['^name', ]

admin.site.register(Company, CompanyAdmin)


class CustomerAdminForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerAdmin(admin.ModelAdmin):
    # form = CustomerAdminForm
    list_display = ['company', 'customer_balance', 'customer_balance_update', 'credit_limit', 'blocking_credit_limit', 'max_calls', 'customer_enabled']
    readonly_fields = ['customer_balance', 'created', 'modified']

admin.site.register(Customer, CustomerAdmin)


class ProviderAdminForm(forms.ModelForm):

    class Meta:
        model = Provider
        fields = '__all__'


class ProviderAdmin(admin.ModelAdmin):
    #form = ProviderAdminForm
    list_display = ['company', 'supplier_balance', 'provider_balance_update', 'modified', 'supplier_enabled']
    readonly_fields = ['supplier_balance', 'created', 'modified']

admin.site.register(Provider, ProviderAdmin)


class CompanyBalanceHistoryAdminForm(forms.ModelForm):

    class Meta:
        model = CompanyBalanceHistory
        fields = '__all__'


class CompanyBalanceHistoryAdmin(admin.ModelAdmin):
    # form = CompanyBalanceHistoryAdminForm
    list_display_links = ('company', )
    list_display = ('company',
                    'amount_debited',
                    'amount_refund',
                    'customer_balance',
                    'supplier_balance',
                    'operation_type',
                    'external_desc',
                    'modified')
    ordering = ('-modified',
                'company')
    search_fields = ['^company__name',
                     '^external_desc']

    def save_model(self, request, obj, form, change):
        if change:
            messages.info(request, _(u"no need to update balance"))
        else:
            company = form.cleaned_data['company']
            amount_debited = form.cleaned_data['amount_debited']
            amount_refund = form.cleaned_data['amount_refund']
            if form.cleaned_data['operation_type'] == "customer":
                balance = Customer.objects.get(company=company)
                balance.customer_balance = balance.customer_balance - amount_debited + amount_refund
                balance.save()
                obj.customer_balance = balance.customer_balance
            elif form.cleaned_data['operation_type'] == "provider":
                balance = Provider.objects.get(company=company)
                balance.supplier_balance = balance.supplier_balance - amount_debited + amount_refund
                balance.save()
                obj.supplier_balance = balance.supplier_balance
            else:
                pass
            messages.success(request, _(u"balance updated"))
        obj.save()

    fieldsets = (
        (_(u'general'), {
            'fields': ('company',
                       'operation_type',
                       'external_desc',
                       'internal_desc')}),
        (_(u'amount'), {
            'fields': ('amount_debited',
                       'amount_refund')}),
        (_(u'balances'), {
            'fields': ('customer_balance',
                       'supplier_balance')}),
    )

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ['company', 'operation_type']
        else:
            return []

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        if request.user.is_superuser:
            return
        else:
            return

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created. it's an edit
            return ['company',
                    'amount_debited',
                    'amount_refund',
                    'customer_balance',
                    'supplier_balance',
                    'operation_type']
        else:
            return ['customer_balance', 'supplier_balance']

admin.site.register(CompanyBalanceHistory, CompanyBalanceHistoryAdmin)

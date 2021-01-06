from . import models

from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Company
        fields = (
            'slug',
            'name',
            'created',
            'modified',
            'address',
            'contact_name',
            'contact_phone',
            'customer_balance',
            'supplier_balance', 
        )


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        fields = (
            'pk',
            'created',
            'modified',
            'account_number',
            'credit_limit',
            'low_credit_alert',
            'max_calls',
            'calls_per_second',
            'customer_enabled',
        )


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Provider
        fields = (
            'pk',
            'created',
            'modified',
            'supplier_enabled',
        )


class CompanyBalanceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CompanyBalanceHistory
        fields = (
            'pk',
            'created',
            'modified',
            'amount_debited',
            'amount_refund',
            'customer_balance',
            'supplier_balance',
            'operation_type',
            'external_desc',
            'internal_desc',
        )

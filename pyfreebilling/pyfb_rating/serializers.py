from . import models

from rest_framework import serializers


class CustomerRcAllocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerRcAllocation
        fields = (
            'pk',
            'tech_prefix',
            'priority',
            'discount',
            'allow_negative_margin',
            'description',
        )
        

class CallerNumListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CallerNumList
        fields = (
            'slug',
            'name',
            'callerid_filter',
        )


class ProviderRatecardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderRatecard
        fields = (
            'slug',
            'name',
            'rc_type',
            'provider_prefix',
            'description',
            'date_start',
            'date_end',
            'estimated_quality',
            'status',
            'status_changed',
            'created',
            'modified',
        )


class CustomerRatecardSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerRatecard
        fields = (
            'slug',
            'rc_type',
            'name',
            'description',
            'date_start',
            'date_end',
            'status',
            'status_changed',
            'created',
            'modified',
        )


class CustomerPrefixRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerPrefixRate
        fields = (
            'pk',
            'prefix',
            'destnum_length',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
            'date_validity',
        )


class ProviderPrefixRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderPrefixRate
        fields = (
            'pk',
            'prefix',
            'destnum_length',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class CustomerDestinationRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerDestinationRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class ProviderDestinationRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderDestinationRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class CustomerCountryTypeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerCountryTypeRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class ProviderCountryTypeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderCountryTypeRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class CustomerCountryRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerCountryRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class ProviderCountryRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderCountryRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class CustomerRegionTypeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerRegionTypeRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class ProviderRegionTypeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderRegionTypeRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class CustomerRegionRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerRegionRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class ProviderRegionRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderRegionRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class CustomerDefaultRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerDefaultRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )


class ProviderDefaultRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProviderDefaultRate
        fields = (
            'pk',
            'r_rate',
            'r_block_min_duration',
            'r_minimal_time',
            'r_init_block',
            'status',
        )

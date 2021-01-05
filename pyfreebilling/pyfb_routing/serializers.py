from . import models

from rest_framework import serializers


class CustomerRoutingGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomerRoutingGroup
        fields = (
            'pk',
            'description',
        )

        
class RoutingGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RoutingGroup
        fields = (
            'slug',
            'name',
            'status',
            'status_changed',
            'created',
            'modified',
            'description',
        )


class PrefixRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PrefixRule
        fields = (
            'pk',
            'prefix',
            'destnum_length',
            'status',
            'route_type',
            'weight',
            'priority',
        )


class DestinationRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DestinationRule
        fields = (
            'pk',
            'status',
            'route_type',
            'weight',
            'priority',
        )


class CountryTypeRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CountryTypeRule
        fields = (
            'pk',
            'status',
            'route_type',
            'weight',
            'priority',
        )


class CountryRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CountryRule
        fields = (
            'pk',
            'status',
            'route_type',
            'weight',
            'priority',
        )


class RegionTypeRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RegionTypeRule
        fields = (
            'pk',
            'status',
            'route_type',
            'weight',
            'priority',
        )


class RegionRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RegionRule
        fields = (
            'pk',
            'status',
            'route_type',
            'weight',
            'priority',
        )


class DefaultRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DefaultRule
        fields = (
            'pk',
            'status',
            'route_type',
            'weight',
            'priority',
        )

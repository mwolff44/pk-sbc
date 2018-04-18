from . import models

from rest_framework import serializers


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Destination
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
            'country_iso2',
        )


class PrefixSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Prefix
        fields = (
            'slug',
            'prefix',
            'created',
            'last_updated',
        )


class CarrierSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Carrier
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
        )


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
        )


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = (
            'pk',
            'country_iso2',
            'created',
            'last_updated',
        )


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Type
        fields = (
            'slug',
            'name',
            'created',
            'last_updated',
        )

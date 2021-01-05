# -*- coding: utf-8 -*-
from . import models

from rest_framework import serializers


class CarrierSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Carrier
        fields = (
            'slug',
            'name',
            'created',
            'modified',
        )


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Type
        fields = (
            'slug',
            'name',
            'created',
            'modified',
        )


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = (
            'slug',
            'name',
            'created',
            'modified',
        )


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Country
        fields = (
            'pk',
            'country_iso2',
            'created',
            'modified',
        )


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Destination
        fields = (
            'slug',
            'name',
            'created',
            'modified',
        )


class PrefixSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Prefix
        fields = (
            'slug',
            'prefix',
            'created',
            'modifed',
        )

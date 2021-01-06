from . import models

from rest_framework import serializers


class DidSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Did
        fields = (
            'pk', 
            'number', 
            'prov_max_channels', 
            'cust_max_channels', 
            'insee_code', 
            'description', 
            'created', 
            'modified', 
            'provider_free', 
            'customer_free', 
        )


class RoutesDidSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RoutesDid
        fields = (
            'pk', 
            'order', 
            'type', 
            'number', 
            'description', 
            'created', 
            'modified', 
            'weight', 
        )



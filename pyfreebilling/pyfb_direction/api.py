# -*- coding: utf-8 -*-
from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CarrierViewSet(viewsets.ModelViewSet):
    """ViewSet for the Carrier class"""

    queryset = models.Carrier.objects.all()
    serializer_class = serializers.CarrierSerializer
    permission_classes = [permissions.IsAuthenticated]


class TypeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Type class"""

    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Region class"""

    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for the Country class"""

    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [permissions.IsAuthenticated]


class DestinationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Destination class"""

    queryset = models.Destination.objects.all()
    serializer_class = serializers.DestinationSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrefixViewSet(viewsets.ModelViewSet):
    """ViewSet for the Prefix class"""

    queryset = models.Prefix.objects.all()
    serializer_class = serializers.PrefixSerializer
    permission_classes = [permissions.IsAuthenticated]

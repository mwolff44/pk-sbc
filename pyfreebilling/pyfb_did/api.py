from . import models
from . import serializers
from rest_framework import viewsets, permissions


class DidViewSet(viewsets.ModelViewSet):
    """ViewSet for the Did class"""

    queryset = models.Did.objects.all()
    serializer_class = serializers.DidSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoutesDidViewSet(viewsets.ModelViewSet):
    """ViewSet for the RoutesDid class"""

    queryset = models.RoutesDid.objects.all()
    serializer_class = serializers.RoutesDidSerializer
    permission_classes = [permissions.IsAuthenticated]



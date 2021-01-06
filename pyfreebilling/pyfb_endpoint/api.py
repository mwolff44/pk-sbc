from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CustomerEndpointViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerEndpoint class"""

    queryset = models.CustomerEndpoint.objects.all()
    serializer_class = serializers.CustomerEndpointSerializer
    permission_classes = [permissions.IsAuthenticated]


class CodecViewSet(viewsets.ModelViewSet):
    """ViewSet for the Codec class"""

    queryset = models.Codec.objects.all()
    serializer_class = serializers.CodecSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderEndpointViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderEndpoint class"""

    queryset = models.ProviderEndpoint.objects.all()
    serializer_class = serializers.ProviderEndpointSerializer
    permission_classes = [permissions.IsAuthenticated]



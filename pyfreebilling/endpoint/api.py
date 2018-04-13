from . import models
from . import serializers
from rest_framework import viewsets, permissions


class UacRegViewSet(viewsets.ModelViewSet):
    """ViewSet for the UacReg class"""

    queryset = models.UacReg.objects.all()
    serializer_class = serializers.UacRegSerializer
    permission_classes = [permissions.IsAuthenticated]


class TrustedViewSet(viewsets.ModelViewSet):
    """ViewSet for the Trusted class"""

    queryset = models.Trusted.objects.all()
    serializer_class = serializers.TrustedSerializer
    permission_classes = [permissions.IsAuthenticated]



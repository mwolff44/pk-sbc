from . import models
from . import serializers
from rest_framework import viewsets, permissions


class AccViewSet(viewsets.ModelViewSet):
    """ViewSet for the Acc class"""

    queryset = models.Acc.objects.all()
    serializer_class = serializers.AccSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccCdrViewSet(viewsets.ModelViewSet):
    """ViewSet for the AccCdr class"""

    queryset = models.AccCdr.objects.all()
    serializer_class = serializers.AccCdrSerializer
    permission_classes = [permissions.IsAuthenticated]


class MissedCallViewSet(viewsets.ModelViewSet):
    """ViewSet for the MissedCall class"""

    queryset = models.MissedCall.objects.all()
    serializer_class = serializers.MissedCallSerializer
    permission_classes = [permissions.IsAuthenticated]



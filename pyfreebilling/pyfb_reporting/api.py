from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CDRViewSet(viewsets.ModelViewSet):
    """ViewSet for the CDR class"""

    queryset = models.CDR.objects.all()
    serializer_class = serializers.CDRSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimDateViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimDate class"""

    queryset = models.DimDate.objects.all()
    serializer_class = serializers.DimDateSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimCustomerHangupcauseViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimCustomerHangupcause class"""

    queryset = models.DimCustomerHangupcause.objects.all()
    serializer_class = serializers.DimCustomerHangupcauseSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimCustomerSipHangupcauseViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimCustomerSipHangupcause class"""

    queryset = models.DimCustomerSipHangupcause.objects.all()
    serializer_class = serializers.DimCustomerSipHangupcauseSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimProviderHangupcauseViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimProviderHangupcause class"""

    queryset = models.DimProviderHangupcause.objects.all()
    serializer_class = serializers.DimProviderHangupcauseSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimProviderSipHangupcauseViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimProviderSipHangupcause class"""

    queryset = models.DimProviderSipHangupcause.objects.all()
    serializer_class = serializers.DimProviderSipHangupcauseSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimCustomerDestinationViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimCustomerDestination class"""

    queryset = models.DimCustomerDestination.objects.all()
    serializer_class = serializers.DimCustomerDestinationSerializer
    permission_classes = [permissions.IsAuthenticated]


class DimProviderDestinationViewSet(viewsets.ModelViewSet):
    """ViewSet for the DimProviderDestination class"""

    queryset = models.DimProviderDestination.objects.all()
    serializer_class = serializers.DimProviderDestinationSerializer
    permission_classes = [permissions.IsAuthenticated]



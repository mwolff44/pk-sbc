from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for the Company class"""

    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for the Customer class"""

    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    """ViewSet for the Provider class"""

    queryset = models.Provider.objects.all()
    serializer_class = serializers.ProviderSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyBalanceHistoryViewSet(viewsets.ModelViewSet):
    """ViewSet for the CompanyBalanceHistory class"""

    queryset = models.CompanyBalanceHistory.objects.all()
    serializer_class = serializers.CompanyBalanceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

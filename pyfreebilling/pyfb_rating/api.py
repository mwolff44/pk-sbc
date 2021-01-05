from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CustomerRcAllocationViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerRcAllocation class"""

    queryset = models.CustomerRcAllocation.objects.all()
    serializer_class = serializers.CustomerRcAllocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    
class CallerNumListViewSet(viewsets.ModelViewSet):
    """ViewSet for the CallerNumList class"""

    queryset = models.CallerNumList.objects.all()
    serializer_class = serializers.CallerNumListSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderRatecardViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderRatecard class"""

    queryset = models.ProviderRatecard.objects.all()
    serializer_class = serializers.ProviderRatecardSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerRatecardViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerRatecard class"""

    queryset = models.CustomerRatecard.objects.all()
    serializer_class = serializers.CustomerRatecardSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerPrefixRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerPrefixRate class"""

    queryset = models.CustomerPrefixRate.objects.all()
    serializer_class = serializers.CustomerPrefixRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderPrefixRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderPrefixRate class"""

    queryset = models.ProviderPrefixRate.objects.all()
    serializer_class = serializers.ProviderPrefixRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerDestinationRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerDestinationRate class"""

    queryset = models.CustomerDestinationRate.objects.all()
    serializer_class = serializers.CustomerDestinationRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderDestinationRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderDestinationRate class"""

    queryset = models.ProviderDestinationRate.objects.all()
    serializer_class = serializers.ProviderDestinationRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerCountryTypeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerCountryTypeRate class"""

    queryset = models.CustomerCountryTypeRate.objects.all()
    serializer_class = serializers.CustomerCountryTypeRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderCountryTypeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderCountryTypeRate class"""

    queryset = models.ProviderCountryTypeRate.objects.all()
    serializer_class = serializers.ProviderCountryTypeRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerCountryRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerCountryRate class"""

    queryset = models.CustomerCountryRate.objects.all()
    serializer_class = serializers.CustomerCountryRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderCountryRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderCountryRate class"""

    queryset = models.ProviderCountryRate.objects.all()
    serializer_class = serializers.ProviderCountryRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerRegionTypeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerRegionTypeRate class"""

    queryset = models.CustomerRegionTypeRate.objects.all()
    serializer_class = serializers.CustomerRegionTypeRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderRegionTypeRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderRegionTypeRate class"""

    queryset = models.ProviderRegionTypeRate.objects.all()
    serializer_class = serializers.ProviderRegionTypeRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerRegionRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerRegionRate class"""

    queryset = models.CustomerRegionRate.objects.all()
    serializer_class = serializers.CustomerRegionRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderRegionRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderRegionRate class"""

    queryset = models.ProviderRegionRate.objects.all()
    serializer_class = serializers.ProviderRegionRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerDefaultRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerDefaultRate class"""

    queryset = models.CustomerDefaultRate.objects.all()
    serializer_class = serializers.CustomerDefaultRateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProviderDefaultRateViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProviderDefaultRate class"""

    queryset = models.ProviderDefaultRate.objects.all()
    serializer_class = serializers.ProviderDefaultRateSerializer
    permission_classes = [permissions.IsAuthenticated]

from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CustomerRoutingGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the CustomerRoutingGroup class"""

    queryset = models.CustomerRoutingGroup.objects.all()
    serializer_class = serializers.CustomerRoutingGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoutingGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for the RoutingGroup class"""

    queryset = models.RoutingGroup.objects.all()
    serializer_class = serializers.RoutingGroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrefixRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the PrefixRule class"""

    queryset = models.PrefixRule.objects.all()
    serializer_class = serializers.PrefixRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class DestinationRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the DestinationRule class"""

    queryset = models.DestinationRule.objects.all()
    serializer_class = serializers.DestinationRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountryTypeRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the CountryTypeRule class"""

    queryset = models.CountryTypeRule.objects.all()
    serializer_class = serializers.CountryTypeRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountryRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the CountryRule class"""

    queryset = models.CountryRule.objects.all()
    serializer_class = serializers.CountryRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegionTypeRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the RegionTypeRule class"""

    queryset = models.RegionTypeRule.objects.all()
    serializer_class = serializers.RegionTypeRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegionRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the RegionRule class"""

    queryset = models.RegionRule.objects.all()
    serializer_class = serializers.RegionRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class DefaultRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the DefaultRule class"""

    queryset = models.DefaultRule.objects.all()
    serializer_class = serializers.DefaultRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

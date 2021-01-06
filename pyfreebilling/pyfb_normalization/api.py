# -*- coding: utf-8 -*-
from . import models
from . import serializers
from rest_framework import viewsets, permissions


class CallMappingRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the CallMappingRule class"""

    queryset = models.CallMappingRule.objects.all()
    serializer_class = serializers.CallMappingRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class NormalizationGrpViewSet(viewsets.ModelViewSet):
    """ViewSet for the NormalizationGrp class"""

    queryset = models.NormalizationGrp.objects.all()
    serializer_class = serializers.NormalizationGrpSerializer
    permission_classes = [permissions.IsAuthenticated]


class NormalizationRuleViewSet(viewsets.ModelViewSet):
    """ViewSet for the NormalizationRule class"""

    queryset = models.NormalizationRule.objects.all()
    serializer_class = serializers.NormalizationRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class NormalizationRuleGrpViewSet(viewsets.ModelViewSet):
    """ViewSet for the NormalizationRuleGrp class"""

    queryset = models.NormalizationRuleGrp.objects.all()
    serializer_class = serializers.NormalizationRuleGrpSerializer
    permission_classes = [permissions.IsAuthenticated]

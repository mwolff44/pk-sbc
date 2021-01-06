# -*- coding: utf-8 -*-
from . import models

from rest_framework import serializers


class CallMappingRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CallMappingRule
        fields = (
            'pk',
            'name',
            'dpid',
            'pr',
            'match_op',
            'match_exp',
            'match_len',
            'subst_exp',
            'repl_exp',
            'attrs',
            'description',
            'created',
            'modified',
        )


class NormalizationGrpSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NormalizationGrp
        fields = (
            'pk',
            'name',
            'description',
            'created',
            'modified',
        )


class NormalizationRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NormalizationRule
        fields = (
            'pk',
            'name',
            'match_op',
            'match_exp',
            'match_len',
            'subst_exp',
            'repl_exp',
            'attrs',
            'description',
            'created',
            'modified',
        )


class NormalizationRuleGrpSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NormalizationRuleGrp
        fields = (
            'pk',
            'pr',
            'description',
            'created',
            'modified',
        )

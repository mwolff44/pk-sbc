# -*- coding: utf-8 -*-
from django import forms
from .models import CallMappingRule, NormalizationGrp, NormalizationRule, NormalizationRuleGrp


class CallMappingRuleForm(forms.ModelForm):
    class Meta:
        model = CallMappingRule
        fields = ['name', 'dpid', 'pr', 'match_op', 'match_exp', 'match_len', 'subst_exp', 'repl_exp', 'attrs', 'description']


class NormalizationGrpForm(forms.ModelForm):
    class Meta:
        model = NormalizationGrp
        fields = ['name', 'description']


class NormalizationRuleForm(forms.ModelForm):
    class Meta:
        model = NormalizationRule
        fields = ['name', 'match_op', 'match_exp', 'match_len', 'subst_exp', 'repl_exp', 'attrs', 'description']


class NormalizationRuleGrpForm(forms.ModelForm):
    class Meta:
        model = NormalizationRuleGrp
        fields = ['pr', 'description', 'dpid', 'rule']

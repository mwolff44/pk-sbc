# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import CallMappingRule, NormalizationGrp, NormalizationRule, NormalizationRuleGrp
from .forms import CallMappingRuleForm, NormalizationGrpForm, NormalizationRuleForm, NormalizationRuleGrpForm


class CallMappingRuleListView(ListView):
    model = CallMappingRule


class CallMappingRuleCreateView(CreateView):
    model = CallMappingRule
    form_class = CallMappingRuleForm


class CallMappingRuleDetailView(DetailView):
    model = CallMappingRule


class CallMappingRuleUpdateView(UpdateView):
    model = CallMappingRule
    form_class = CallMappingRuleForm


class NormalizationGrpListView(ListView):
    model = NormalizationGrp


class NormalizationGrpCreateView(CreateView):
    model = NormalizationGrp
    form_class = NormalizationGrpForm


class NormalizationGrpDetailView(DetailView):
    model = NormalizationGrp


class NormalizationGrpUpdateView(UpdateView):
    model = NormalizationGrp
    form_class = NormalizationGrpForm


class NormalizationRuleListView(ListView):
    model = NormalizationRule


class NormalizationRuleCreateView(CreateView):
    model = NormalizationRule
    form_class = NormalizationRuleForm


class NormalizationRuleDetailView(DetailView):
    model = NormalizationRule


class NormalizationRuleUpdateView(UpdateView):
    model = NormalizationRule
    form_class = NormalizationRuleForm


class NormalizationRuleGrpListView(ListView):
    model = NormalizationRuleGrp


class NormalizationRuleGrpCreateView(CreateView):
    model = NormalizationRuleGrp
    form_class = NormalizationRuleGrpForm


class NormalizationRuleGrpDetailView(DetailView):
    model = NormalizationRuleGrp


class NormalizationRuleGrpUpdateView(UpdateView):
    model = NormalizationRuleGrp
    form_class = NormalizationRuleGrpForm

from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .models import CustomerRoutingGroup, RoutingGroup, PrefixRule, DestinationRule, CountryTypeRule, CountryRule, RegionTypeRule, RegionRule, DefaultRule
from .forms import CustomerRoutingGroupForm, RoutingGroupForm, PrefixRuleForm, DestinationRuleForm, CountryTypeRuleForm, CountryRuleForm, RegionTypeRuleForm, RegionRuleForm, DefaultRuleForm


class CustomerRoutingGroupListView(ListView):
    model = CustomerRoutingGroup


class CustomerRoutingGroupCreateView(CreateView):
    model = CustomerRoutingGroup
    form_class = CustomerRoutingGroupForm


class CustomerRoutingGroupDetailView(DetailView):
    model = CustomerRoutingGroup


class CustomerRoutingGroupUpdateView(UpdateView):
    model = CustomerRoutingGroup
    form_class = CustomerRoutingGroupForm

    
class RoutingGroupListView(ListView):
    model = RoutingGroup


class RoutingGroupCreateView(CreateView):
    model = RoutingGroup
    form_class = RoutingGroupForm


class RoutingGroupDetailView(DetailView):
    model = RoutingGroup


class RoutingGroupUpdateView(UpdateView):
    model = RoutingGroup
    form_class = RoutingGroupForm


class PrefixRuleListView(ListView):
    model = PrefixRule


class PrefixRuleCreateView(CreateView):
    model = PrefixRule
    form_class = PrefixRuleForm


class PrefixRuleDetailView(DetailView):
    model = PrefixRule


class PrefixRuleUpdateView(UpdateView):
    model = PrefixRule
    form_class = PrefixRuleForm


class DestinationRuleListView(ListView):
    model = DestinationRule


class DestinationRuleCreateView(CreateView):
    model = DestinationRule
    form_class = DestinationRuleForm


class DestinationRuleDetailView(DetailView):
    model = DestinationRule


class DestinationRuleUpdateView(UpdateView):
    model = DestinationRule
    form_class = DestinationRuleForm


class CountryTypeRuleListView(ListView):
    model = CountryTypeRule


class CountryTypeRuleCreateView(CreateView):
    model = CountryTypeRule
    form_class = CountryTypeRuleForm


class CountryTypeRuleDetailView(DetailView):
    model = CountryTypeRule


class CountryTypeRuleUpdateView(UpdateView):
    model = CountryTypeRule
    form_class = CountryTypeRuleForm


class CountryRuleListView(ListView):
    model = CountryRule


class CountryRuleCreateView(CreateView):
    model = CountryRule
    form_class = CountryRuleForm


class CountryRuleDetailView(DetailView):
    model = CountryRule


class CountryRuleUpdateView(UpdateView):
    model = CountryRule
    form_class = CountryRuleForm


class RegionTypeRuleListView(ListView):
    model = RegionTypeRule


class RegionTypeRuleCreateView(CreateView):
    model = RegionTypeRule
    form_class = RegionTypeRuleForm


class RegionTypeRuleDetailView(DetailView):
    model = RegionTypeRule


class RegionTypeRuleUpdateView(UpdateView):
    model = RegionTypeRule
    form_class = RegionTypeRuleForm


class RegionRuleListView(ListView):
    model = RegionRule


class RegionRuleCreateView(CreateView):
    model = RegionRule
    form_class = RegionRuleForm


class RegionRuleDetailView(DetailView):
    model = RegionRule


class RegionRuleUpdateView(UpdateView):
    model = RegionRule
    form_class = RegionRuleForm


class DefaultRuleListView(ListView):
    model = DefaultRule


class DefaultRuleCreateView(CreateView):
    model = DefaultRule
    form_class = DefaultRuleForm


class DefaultRuleDetailView(DetailView):
    model = DefaultRule


class DefaultRuleUpdateView(UpdateView):
    model = DefaultRule
    form_class = DefaultRuleForm

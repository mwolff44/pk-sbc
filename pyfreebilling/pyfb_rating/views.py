# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import CustomerRcAllocation, CallerNumList, ProviderRatecard, CustomerRatecard, CustomerPrefixRate, ProviderPrefixRate, CustomerDestinationRate, ProviderDestinationRate, CustomerCountryTypeRate, ProviderCountryTypeRate, CustomerCountryRate, ProviderCountryRate, CustomerRegionTypeRate, ProviderRegionTypeRate, CustomerRegionRate, ProviderRegionRate, CustomerDefaultRate, ProviderDefaultRate
from .forms import CustomerRcAllocationForm, CallerNumListForm, ProviderRatecardForm, CustomerRatecardForm, CustomerPrefixRateForm, ProviderPrefixRateForm, CustomerDestinationRateForm, ProviderDestinationRateForm, CustomerCountryTypeRateForm, ProviderCountryTypeRateForm, CustomerCountryRateForm, ProviderCountryRateForm, CustomerRegionTypeRateForm, ProviderRegionTypeRateForm, CustomerRegionRateForm, ProviderRegionRateForm, CustomerDefaultRateForm, ProviderDefaultRateForm


class CustomerRcAllocationListView(ListView):
    model = CustomerRcAllocation


class CustomerRcAllocationCreateView(CreateView):
    model = CustomerRcAllocation
    form_class = CustomerRcAllocationForm


class CustomerRcAllocationDetailView(DetailView):
    model = CustomerRcAllocation


class CustomerRcAllocationUpdateView(UpdateView):
    model = CustomerRcAllocation
    form_class = CustomerRcAllocationForm


class CallerNumListListView(ListView):
    model = CallerNumList


class CallerNumListCreateView(CreateView):
    model = CallerNumList
    form_class = CallerNumListForm


class CallerNumListDetailView(DetailView):
    model = CallerNumList


class CallerNumListUpdateView(UpdateView):
    model = CallerNumList
    form_class = CallerNumListForm


class ProviderRatecardListView(ListView):
    model = ProviderRatecard


class ProviderRatecardCreateView(CreateView):
    model = ProviderRatecard
    form_class = ProviderRatecardForm


class ProviderRatecardDetailView(DetailView):
    model = ProviderRatecard


class ProviderRatecardUpdateView(UpdateView):
    model = ProviderRatecard
    form_class = ProviderRatecardForm


class CustomerRatecardListView(ListView):
    model = CustomerRatecard


class CustomerRatecardCreateView(CreateView):
    model = CustomerRatecard
    form_class = CustomerRatecardForm


class CustomerRatecardDetailView(DetailView):
    model = CustomerRatecard


class CustomerRatecardUpdateView(UpdateView):
    model = CustomerRatecard
    form_class = CustomerRatecardForm


class CustomerPrefixRateListView(ListView):
    model = CustomerPrefixRate


class CustomerPrefixRateCreateView(CreateView):
    model = CustomerPrefixRate
    form_class = CustomerPrefixRateForm


class CustomerPrefixRateDetailView(DetailView):
    model = CustomerPrefixRate


class CustomerPrefixRateUpdateView(UpdateView):
    model = CustomerPrefixRate
    form_class = CustomerPrefixRateForm


class ProviderPrefixRateListView(ListView):
    model = ProviderPrefixRate


class ProviderPrefixRateCreateView(CreateView):
    model = ProviderPrefixRate
    form_class = ProviderPrefixRateForm


class ProviderPrefixRateDetailView(DetailView):
    model = ProviderPrefixRate


class ProviderPrefixRateUpdateView(UpdateView):
    model = ProviderPrefixRate
    form_class = ProviderPrefixRateForm


class CustomerDestinationRateListView(ListView):
    model = CustomerDestinationRate


class CustomerDestinationRateCreateView(CreateView):
    model = CustomerDestinationRate
    form_class = CustomerDestinationRateForm


class CustomerDestinationRateDetailView(DetailView):
    model = CustomerDestinationRate


class CustomerDestinationRateUpdateView(UpdateView):
    model = CustomerDestinationRate
    form_class = CustomerDestinationRateForm


class ProviderDestinationRateListView(ListView):
    model = ProviderDestinationRate


class ProviderDestinationRateCreateView(CreateView):
    model = ProviderDestinationRate
    form_class = ProviderDestinationRateForm


class ProviderDestinationRateDetailView(DetailView):
    model = ProviderDestinationRate


class ProviderDestinationRateUpdateView(UpdateView):
    model = ProviderDestinationRate
    form_class = ProviderDestinationRateForm


class CustomerCountryTypeRateListView(ListView):
    model = CustomerCountryTypeRate


class CustomerCountryTypeRateCreateView(CreateView):
    model = CustomerCountryTypeRate
    form_class = CustomerCountryTypeRateForm


class CustomerCountryTypeRateDetailView(DetailView):
    model = CustomerCountryTypeRate


class CustomerCountryTypeRateUpdateView(UpdateView):
    model = CustomerCountryTypeRate
    form_class = CustomerCountryTypeRateForm


class ProviderCountryTypeRateListView(ListView):
    model = ProviderCountryTypeRate


class ProviderCountryTypeRateCreateView(CreateView):
    model = ProviderCountryTypeRate
    form_class = ProviderCountryTypeRateForm


class ProviderCountryTypeRateDetailView(DetailView):
    model = ProviderCountryTypeRate


class ProviderCountryTypeRateUpdateView(UpdateView):
    model = ProviderCountryTypeRate
    form_class = ProviderCountryTypeRateForm


class CustomerCountryRateListView(ListView):
    model = CustomerCountryRate


class CustomerCountryRateCreateView(CreateView):
    model = CustomerCountryRate
    form_class = CustomerCountryRateForm


class CustomerCountryRateDetailView(DetailView):
    model = CustomerCountryRate


class CustomerCountryRateUpdateView(UpdateView):
    model = CustomerCountryRate
    form_class = CustomerCountryRateForm


class ProviderCountryRateListView(ListView):
    model = ProviderCountryRate


class ProviderCountryRateCreateView(CreateView):
    model = ProviderCountryRate
    form_class = ProviderCountryRateForm


class ProviderCountryRateDetailView(DetailView):
    model = ProviderCountryRate


class ProviderCountryRateUpdateView(UpdateView):
    model = ProviderCountryRate
    form_class = ProviderCountryRateForm


class CustomerRegionTypeRateListView(ListView):
    model = CustomerRegionTypeRate


class CustomerRegionTypeRateCreateView(CreateView):
    model = CustomerRegionTypeRate
    form_class = CustomerRegionTypeRateForm


class CustomerRegionTypeRateDetailView(DetailView):
    model = CustomerRegionTypeRate


class CustomerRegionTypeRateUpdateView(UpdateView):
    model = CustomerRegionTypeRate
    form_class = CustomerRegionTypeRateForm


class ProviderRegionTypeRateListView(ListView):
    model = ProviderRegionTypeRate


class ProviderRegionTypeRateCreateView(CreateView):
    model = ProviderRegionTypeRate
    form_class = ProviderRegionTypeRateForm


class ProviderRegionTypeRateDetailView(DetailView):
    model = ProviderRegionTypeRate


class ProviderRegionTypeRateUpdateView(UpdateView):
    model = ProviderRegionTypeRate
    form_class = ProviderRegionTypeRateForm


class CustomerRegionRateListView(ListView):
    model = CustomerRegionRate


class CustomerRegionRateCreateView(CreateView):
    model = CustomerRegionRate
    form_class = CustomerRegionRateForm


class CustomerRegionRateDetailView(DetailView):
    model = CustomerRegionRate


class CustomerRegionRateUpdateView(UpdateView):
    model = CustomerRegionRate
    form_class = CustomerRegionRateForm


class ProviderRegionRateListView(ListView):
    model = ProviderRegionRate


class ProviderRegionRateCreateView(CreateView):
    model = ProviderRegionRate
    form_class = ProviderRegionRateForm


class ProviderRegionRateDetailView(DetailView):
    model = ProviderRegionRate


class ProviderRegionRateUpdateView(UpdateView):
    model = ProviderRegionRate
    form_class = ProviderRegionRateForm


class CustomerDefaultRateListView(ListView):
    model = CustomerDefaultRate


class CustomerDefaultRateCreateView(CreateView):
    model = CustomerDefaultRate
    form_class = CustomerDefaultRateForm


class CustomerDefaultRateDetailView(DetailView):
    model = CustomerDefaultRate


class CustomerDefaultRateUpdateView(UpdateView):
    model = CustomerDefaultRate
    form_class = CustomerDefaultRateForm


class ProviderDefaultRateListView(ListView):
    model = ProviderDefaultRate


class ProviderDefaultRateCreateView(CreateView):
    model = ProviderDefaultRate
    form_class = ProviderDefaultRateForm


class ProviderDefaultRateDetailView(DetailView):
    model = ProviderDefaultRate


class ProviderDefaultRateUpdateView(UpdateView):
    model = ProviderDefaultRate
    form_class = ProviderDefaultRateForm

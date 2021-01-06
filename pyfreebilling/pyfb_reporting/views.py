# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .models import CDR, DimDate, DimCustomerHangupcause, DimCustomerSipHangupcause, DimProviderHangupcause, DimProviderSipHangupcause, DimCustomerDestination, DimProviderDestination
from .forms import CDRForm, DimDateForm, DimCustomerHangupcauseForm, DimCustomerSipHangupcauseForm, DimProviderHangupcauseForm, DimProviderSipHangupcauseForm, DimCustomerDestinationForm, DimProviderDestinationForm


class CDRListView(ListView):
    model = CDR


class CDRCreateView(CreateView):
    model = CDR
    form_class = CDRForm


class CDRDetailView(DetailView):
    model = CDR


class CDRUpdateView(UpdateView):
    model = CDR
    form_class = CDRForm


class DimDateListView(ListView):
    model = DimDate


class DimDateCreateView(CreateView):
    model = DimDate
    form_class = DimDateForm


class DimDateDetailView(DetailView):
    model = DimDate


class DimDateUpdateView(UpdateView):
    model = DimDate
    form_class = DimDateForm


class DimCustomerHangupcauseListView(ListView):
    model = DimCustomerHangupcause


class DimCustomerHangupcauseCreateView(CreateView):
    model = DimCustomerHangupcause
    form_class = DimCustomerHangupcauseForm


class DimCustomerHangupcauseDetailView(DetailView):
    model = DimCustomerHangupcause


class DimCustomerHangupcauseUpdateView(UpdateView):
    model = DimCustomerHangupcause
    form_class = DimCustomerHangupcauseForm


class DimCustomerSipHangupcauseListView(ListView):
    model = DimCustomerSipHangupcause


class DimCustomerSipHangupcauseCreateView(CreateView):
    model = DimCustomerSipHangupcause
    form_class = DimCustomerSipHangupcauseForm


class DimCustomerSipHangupcauseDetailView(DetailView):
    model = DimCustomerSipHangupcause


class DimCustomerSipHangupcauseUpdateView(UpdateView):
    model = DimCustomerSipHangupcause
    form_class = DimCustomerSipHangupcauseForm


class DimProviderHangupcauseListView(ListView):
    model = DimProviderHangupcause


class DimProviderHangupcauseCreateView(CreateView):
    model = DimProviderHangupcause
    form_class = DimProviderHangupcauseForm


class DimProviderHangupcauseDetailView(DetailView):
    model = DimProviderHangupcause


class DimProviderHangupcauseUpdateView(UpdateView):
    model = DimProviderHangupcause
    form_class = DimProviderHangupcauseForm


class DimProviderSipHangupcauseListView(ListView):
    model = DimProviderSipHangupcause


class DimProviderSipHangupcauseCreateView(CreateView):
    model = DimProviderSipHangupcause
    form_class = DimProviderSipHangupcauseForm


class DimProviderSipHangupcauseDetailView(DetailView):
    model = DimProviderSipHangupcause


class DimProviderSipHangupcauseUpdateView(UpdateView):
    model = DimProviderSipHangupcause
    form_class = DimProviderSipHangupcauseForm


class DimCustomerDestinationListView(ListView):
    model = DimCustomerDestination


class DimCustomerDestinationCreateView(CreateView):
    model = DimCustomerDestination
    form_class = DimCustomerDestinationForm


class DimCustomerDestinationDetailView(DetailView):
    model = DimCustomerDestination


class DimCustomerDestinationUpdateView(UpdateView):
    model = DimCustomerDestination
    form_class = DimCustomerDestinationForm


class DimProviderDestinationListView(ListView):
    model = DimProviderDestination


class DimProviderDestinationCreateView(CreateView):
    model = DimProviderDestination
    form_class = DimProviderDestinationForm


class DimProviderDestinationDetailView(DetailView):
    model = DimProviderDestination


class DimProviderDestinationUpdateView(UpdateView):
    model = DimProviderDestination
    form_class = DimProviderDestinationForm

# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import CustomerEndpoint, Codec, ProviderEndpoint
from .forms import CustomerEndpointForm, CodecForm, ProviderEndpointForm


class CustomerEndpointListView(ListView):
    model = CustomerEndpoint


class CustomerEndpointCreateView(CreateView):
    model = CustomerEndpoint
    form_class = CustomerEndpointForm


class CustomerEndpointDetailView(DetailView):
    model = CustomerEndpoint


class CustomerEndpointUpdateView(UpdateView):
    model = CustomerEndpoint
    form_class = CustomerEndpointForm


class CodecListView(ListView):
    model = Codec


class CodecCreateView(CreateView):
    model = Codec
    form_class = CodecForm


class CodecDetailView(DetailView):
    model = Codec


class CodecUpdateView(UpdateView):
    model = Codec
    form_class = CodecForm


class ProviderEndpointListView(ListView):
    model = ProviderEndpoint


class ProviderEndpointCreateView(CreateView):
    model = ProviderEndpoint
    form_class = ProviderEndpointForm


class ProviderEndpointDetailView(DetailView):
    model = ProviderEndpoint


class ProviderEndpointUpdateView(UpdateView):
    model = ProviderEndpoint
    form_class = ProviderEndpointForm

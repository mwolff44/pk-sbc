# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Company, Customer, Provider, CompanyBalanceHistory
from .forms import CompanyForm, CustomerForm, ProviderForm, CompanyBalanceHistoryForm


class CompanyListView(ListView):
    model = Company


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm


class CompanyDetailView(DetailView):
    model = Company


class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm


class CustomerListView(ListView):
    model = Customer


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm


class CustomerDetailView(DetailView):
    model = Customer


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm


class ProviderListView(ListView):
    model = Provider


class ProviderCreateView(CreateView):
    model = Provider
    form_class = ProviderForm


class ProviderDetailView(DetailView):
    model = Provider


class ProviderUpdateView(UpdateView):
    model = Provider
    form_class = ProviderForm


class CompanyBalanceHistoryListView(ListView):
    model = CompanyBalanceHistory


class CompanyBalanceHistoryCreateView(CreateView):
    model = CompanyBalanceHistory
    form_class = CompanyBalanceHistoryForm


class CompanyBalanceHistoryDetailView(DetailView):
    model = CompanyBalanceHistory


class CompanyBalanceHistoryUpdateView(UpdateView):
    model = CompanyBalanceHistory
    form_class = CompanyBalanceHistoryForm

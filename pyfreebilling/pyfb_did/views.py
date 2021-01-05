from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Did, RoutesDid
from .forms import DidForm, RoutesDidForm


class DidListView(ListView):
    model = Did


class DidCreateView(CreateView):
    model = Did
    form_class = DidForm


class DidDetailView(DetailView):
    model = Did


class DidUpdateView(UpdateView):
    model = Did
    form_class = DidForm


class RoutesDidListView(ListView):
    model = RoutesDid


class RoutesDidCreateView(CreateView):
    model = RoutesDid
    form_class = RoutesDidForm


class RoutesDidDetailView(DetailView):
    model = RoutesDid


class RoutesDidUpdateView(UpdateView):
    model = RoutesDid
    form_class = RoutesDidForm


from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Destination, Prefix, Carrier, Region, Country, Type
from .forms import DestinationForm, PrefixForm, CarrierForm, RegionForm, CountryForm, TypeForm


class DestinationListView(ListView):
    model = Destination


class DestinationCreateView(CreateView):
    model = Destination
    form_class = DestinationForm


class DestinationDetailView(DetailView):
    model = Destination


class DestinationUpdateView(UpdateView):
    model = Destination
    form_class = DestinationForm


class PrefixListView(ListView):
    model = Prefix


class PrefixCreateView(CreateView):
    model = Prefix
    form_class = PrefixForm


class PrefixDetailView(DetailView):
    model = Prefix


class PrefixUpdateView(UpdateView):
    model = Prefix
    form_class = PrefixForm


class CarrierListView(ListView):
    model = Carrier


class CarrierCreateView(CreateView):
    model = Carrier
    form_class = CarrierForm


class CarrierDetailView(DetailView):
    model = Carrier


class CarrierUpdateView(UpdateView):
    model = Carrier
    form_class = CarrierForm


class RegionListView(ListView):
    model = Region


class RegionCreateView(CreateView):
    model = Region
    form_class = RegionForm


class RegionDetailView(DetailView):
    model = Region


class RegionUpdateView(UpdateView):
    model = Region
    form_class = RegionForm


class CountryListView(ListView):
    model = Country


class CountryCreateView(CreateView):
    model = Country
    form_class = CountryForm


class CountryDetailView(DetailView):
    model = Country


class CountryUpdateView(UpdateView):
    model = Country
    form_class = CountryForm


class TypeListView(ListView):
    model = Type


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm


class TypeDetailView(DetailView):
    model = Type


class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm


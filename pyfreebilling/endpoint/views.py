from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import UacReg, Trusted
from .forms import UacRegForm, TrustedForm


class UacRegListView(ListView):
    model = UacReg


class UacRegCreateView(CreateView):
    model = UacReg
    form_class = UacRegForm


class UacRegDetailView(DetailView):
    model = UacReg


class UacRegUpdateView(UpdateView):
    model = UacReg
    form_class = UacRegForm


class TrustedListView(ListView):
    model = Trusted


class TrustedCreateView(CreateView):
    model = Trusted
    form_class = TrustedForm


class TrustedDetailView(DetailView):
    model = Trusted


class TrustedUpdateView(UpdateView):
    model = Trusted
    form_class = TrustedForm


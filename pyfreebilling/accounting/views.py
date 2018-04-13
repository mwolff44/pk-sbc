from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Acc, AccCdr, MissedCall
from .forms import AccForm, AccCdrForm, MissedCallForm


class AccListView(ListView):
    model = Acc


class AccCreateView(CreateView):
    model = Acc
    form_class = AccForm


class AccDetailView(DetailView):
    model = Acc


class AccUpdateView(UpdateView):
    model = Acc
    form_class = AccForm


class AccCdrListView(ListView):
    model = AccCdr


class AccCdrCreateView(CreateView):
    model = AccCdr
    form_class = AccCdrForm


class AccCdrDetailView(DetailView):
    model = AccCdr


class AccCdrUpdateView(UpdateView):
    model = AccCdr
    form_class = AccCdrForm


class MissedCallListView(ListView):
    model = MissedCall


class MissedCallCreateView(CreateView):
    model = MissedCall
    form_class = MissedCallForm


class MissedCallDetailView(DetailView):
    model = MissedCall


class MissedCallUpdateView(UpdateView):
    model = MissedCall
    form_class = MissedCallForm


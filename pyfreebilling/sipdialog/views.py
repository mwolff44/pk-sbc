from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Dialog, DialogVar
from .forms import DialogForm, DialogVarForm


class DialogListView(ListView):
    model = Dialog


class DialogCreateView(CreateView):
    model = Dialog
    form_class = DialogForm


class DialogDetailView(DetailView):
    model = Dialog


class DialogUpdateView(UpdateView):
    model = Dialog
    form_class = DialogForm


class DialogVarListView(ListView):
    model = DialogVar


class DialogVarCreateView(CreateView):
    model = DialogVar
    form_class = DialogVarForm


class DialogVarDetailView(DetailView):
    model = DialogVar


class DialogVarUpdateView(UpdateView):
    model = DialogVar
    form_class = DialogVarForm


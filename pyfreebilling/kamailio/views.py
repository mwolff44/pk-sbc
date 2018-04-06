from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable
from .forms import VersionForm, LocationForm, LocationAttrsForm, UserBlackListForm, GlobalBlackListForm, SpeedDialForm, PipeLimitForm, MtreeForm, MtreesForm, HtableForm


class VersionListView(ListView):
    model = Version


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm


class VersionDetailView(DetailView):
    model = Version


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm


class LocationListView(ListView):
    model = Location


class LocationCreateView(CreateView):
    model = Location
    form_class = LocationForm


class LocationDetailView(DetailView):
    model = Location


class LocationUpdateView(UpdateView):
    model = Location
    form_class = LocationForm


class LocationAttrsListView(ListView):
    model = LocationAttrs


class LocationAttrsCreateView(CreateView):
    model = LocationAttrs
    form_class = LocationAttrsForm


class LocationAttrsDetailView(DetailView):
    model = LocationAttrs


class LocationAttrsUpdateView(UpdateView):
    model = LocationAttrs
    form_class = LocationAttrsForm


class UserBlackListListView(ListView):
    model = UserBlackList


class UserBlackListCreateView(CreateView):
    model = UserBlackList
    form_class = UserBlackListForm


class UserBlackListDetailView(DetailView):
    model = UserBlackList


class UserBlackListUpdateView(UpdateView):
    model = UserBlackList
    form_class = UserBlackListForm


class GlobalBlackListListView(ListView):
    model = GlobalBlackList


class GlobalBlackListCreateView(CreateView):
    model = GlobalBlackList
    form_class = GlobalBlackListForm


class GlobalBlackListDetailView(DetailView):
    model = GlobalBlackList


class GlobalBlackListUpdateView(UpdateView):
    model = GlobalBlackList
    form_class = GlobalBlackListForm


class SpeedDialListView(ListView):
    model = SpeedDial


class SpeedDialCreateView(CreateView):
    model = SpeedDial
    form_class = SpeedDialForm


class SpeedDialDetailView(DetailView):
    model = SpeedDial


class SpeedDialUpdateView(UpdateView):
    model = SpeedDial
    form_class = SpeedDialForm


class PipeLimitListView(ListView):
    model = PipeLimit


class PipeLimitCreateView(CreateView):
    model = PipeLimit
    form_class = PipeLimitForm


class PipeLimitDetailView(DetailView):
    model = PipeLimit


class PipeLimitUpdateView(UpdateView):
    model = PipeLimit
    form_class = PipeLimitForm


class MtreeListView(ListView):
    model = Mtree


class MtreeCreateView(CreateView):
    model = Mtree
    form_class = MtreeForm


class MtreeDetailView(DetailView):
    model = Mtree


class MtreeUpdateView(UpdateView):
    model = Mtree
    form_class = MtreeForm


class MtreesListView(ListView):
    model = Mtrees


class MtreesCreateView(CreateView):
    model = Mtrees
    form_class = MtreesForm


class MtreesDetailView(DetailView):
    model = Mtrees


class MtreesUpdateView(UpdateView):
    model = Mtrees
    form_class = MtreesForm


class HtableListView(ListView):
    model = Htable


class HtableCreateView(CreateView):
    model = Htable
    form_class = HtableForm


class HtableDetailView(DetailView):
    model = Htable


class HtableUpdateView(UpdateView):
    model = Htable
    form_class = HtableForm


# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from .models import Dialog, DialogVar, Acc, AccCdr, MissedCall, UacReg, Trusted, Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable, RtpEngine, Statistic
from .forms import DialogForm, DialogVarForm, AccForm, AccCdrForm, MissedCallForm, UacRegForm, TrustedForm, VersionForm, LocationForm, LocationAttrsForm, UserBlackListForm, GlobalBlackListForm, SpeedDialForm, PipeLimitForm, MtreeForm, MtreesForm, HtableForm, RtpEngineForm, StatisticForm


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


class RtpEngineListView(ListView):
    model = RtpEngine


class RtpEngineCreateView(CreateView):
    model = RtpEngine
    form_class = RtpEngineForm


class RtpEngineDetailView(DetailView):
    model = RtpEngine


class RtpEngineUpdateView(UpdateView):
    model = RtpEngine
    form_class = RtpEngineForm


class StatisticListView(ListView):
    model = Statistic


class StatisticCreateView(CreateView):
    model = Statistic
    form_class = StatisticForm


class StatisticDetailView(DetailView):
    model = Statistic


class StatisticUpdateView(UpdateView):
    model = Statistic
    form_class = StatisticForm

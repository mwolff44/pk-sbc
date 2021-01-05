# -*- coding: utf-8 -*-
from django import forms
from .models import Dialog, DialogVar, Acc, AccCdr, MissedCall, UacReg, Trusted, Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable, RtpEngine, Statistic


class DialogForm(forms.ModelForm):
    class Meta:
        model = Dialog
        fields = ['hash_entry', 'hash_id', 'callid', 'from_uri', 'from_tag', 'to_uri', 'to_tag', 'caller_cseq', 'callee_cseq', 'caller_route_set', 'callee_route_set', 'caller_contact', 'callee_contact', 'caller_sock', 'callee_sock', 'state', 'start_time', 'timeout', 'sflags', 'iflags', 'toroute_name', 'req_uri', 'xdata']


class DialogVarForm(forms.ModelForm):
    class Meta:
        model = DialogVar
        fields = ['hash_entry', 'hash_id', 'dialog_key', 'dialog_value']


class AccForm(forms.ModelForm):
    class Meta:
        model = Acc
        fields = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time', 'time_attr', 'time_exten']


class AccCdrForm(forms.ModelForm):
    class Meta:
        model = AccCdr
        fields = ['start_time', 'end_time', 'duration']


class MissedCallForm(forms.ModelForm):
    class Meta:
        model = MissedCall
        fields = ['method', 'from_tag', 'to_tag', 'callid', 'sip_code', 'sip_reason', 'time']


class UacRegForm(forms.ModelForm):
    class Meta:
        model = UacReg
        fields = ['l_uuid', 'l_username', 'l_domain', 'r_username', 'r_domain', 'realm', 'auth_username', 'auth_password', 'auth_ha1', 'auth_proxy', 'expires', 'flags', 'reg_delay', 'socket']


class TrustedForm(forms.ModelForm):
    class Meta:
        model = Trusted
        fields = ['src_ip', 'proto', 'from_pattern', 'ruri_pattern', 'tag', 'priority']


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['table_name', 'table_version']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['ruid', 'username', 'domain', 'contact', 'received', 'path', 'expires', 'q', 'callid', 'cseq', 'last_modified', 'flags', 'cflags', 'user_agent', 'socket', 'methods', 'instance', 'reg_id', 'server_id', 'connection_id', 'keepalive', 'partition']


class LocationAttrsForm(forms.ModelForm):
    class Meta:
        model = LocationAttrs
        fields = ['ruid', 'username', 'domain', 'aname', 'atype', 'avalue', 'last_modified']


class UserBlackListForm(forms.ModelForm):
    class Meta:
        model = UserBlackList
        fields = ['username', 'domain', 'prefix', 'whitelist']


class GlobalBlackListForm(forms.ModelForm):
    class Meta:
        model = GlobalBlackList
        fields = ['prefix', 'whitelist', 'description']


class SpeedDialForm(forms.ModelForm):
    class Meta:
        model = SpeedDial
        fields = ['username', 'domain', 'sd_username', 'sd_domain', 'new_uri', 'fname', 'lname', 'description']


class PipeLimitForm(forms.ModelForm):
    class Meta:
        model = PipeLimit
        fields = ['pipeid', 'algorithm', 'plimit']


class MtreeForm(forms.ModelForm):
    class Meta:
        model = Mtree
        fields = ['tprefix', 'tvalue']


class MtreesForm(forms.ModelForm):
    class Meta:
        model = Mtrees
        fields = ['tname', 'tprefix', 'tvalue']


class HtableForm(forms.ModelForm):
    class Meta:
        model = Htable
        fields = ['key_name', 'key_type', 'value_type', 'key_value', 'expires']


class RtpEngineForm(forms.ModelForm):
    class Meta:
        model = RtpEngine
        fields = ['setid', 'url', 'weight', 'disabled']


class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = ['kamailio_id', 'time_stamp', 'random', 'shm_used_size', 'shm_real_used_size', 'shm_max_used_size', 'shm_free_used_size', 'ul_users', 'ul_contacts']

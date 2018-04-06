from django import forms
from .models import Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['table_name', 'table_version']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['ruid', 'username', 'domain', 'contact', 'received', 'path', 'expires', 'q', 'callid', 'cseq', 'last_modified', 'flags', 'cfags', 'user_agent', 'socket', 'methods', 'instance', 'reg_id', 'server_id', 'connection_id', 'keepalive', 'partition']


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



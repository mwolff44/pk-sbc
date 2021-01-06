# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Domain, Dialog, DialogVar, Acc, AccCdr, MissedCall, UacReg, Trusted, Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable, RtpEngine, Statistic


class DomainAdminForm(forms.ModelForm):

    class Meta:
        model = Domain
        fields = '__all__'


class DomainAdmin(admin.ModelAdmin):
    form = DomainAdminForm
    list_display = ['domain', 'did', 'last_modified']


admin.site.register(Domain, DomainAdmin)


class DialogAdminForm(forms.ModelForm):

    class Meta:
        model = Dialog
        fields = '__all__'


class DialogAdmin(admin.ModelAdmin):
    form = DialogAdminForm
    list_display = [
        'callid',
        'from_uri',
        'to_uri',
        'state',
        'start_time',
        'req_uri'
    ]
    # readonly_fields = ['hash_entry', 'hash_id', 'callid', 'from_uri', 'from_tag', 'to_uri', 'to_tag', 'caller_cseq', 'callee_cseq', 'caller_route_set', 'callee_route_set', 'caller_contact', 'callee_contact', 'caller_sock', 'callee_sock', 'state', 'start_time', 'timeout', 'sflags', 'iflags', 'toroute_name', 'req_uri', 'xdata']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(Dialog, DialogAdmin)


class DialogVarAdminForm(forms.ModelForm):

    class Meta:
        model = DialogVar
        fields = '__all__'


class DialogVarAdmin(admin.ModelAdmin):
    form = DialogVarAdminForm
    list_display = ['hash_entry', 'hash_id', 'dialog_key', 'dialog_value']
    # readonly_fields = ['hash_entry', 'hash_id', 'dialog_key', 'dialog_value']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(DialogVar, DialogVarAdmin)


class AccAdminForm(forms.ModelForm):

    class Meta:
        model = Acc
        fields = '__all__'


class AccAdmin(admin.ModelAdmin):
    form = AccAdminForm
    list_display = [
        'method',
        'from_user',
        'from_domain',
        'ruri_user',
        'ruri_domain',
        'callid',
        'sip_code',
        'sip_reason',
        'time'
    ]
    # readonly_fields = ['src_ip', 'method', 'from_user', 'from_domain', 'ruri_user', 'ruri_domain', 'callid', 'sip_code', 'sip_reason', 'time', 'time_attr', 'time_exten', 'cseq', 'ruri_user', 'ruri_domain', 'from_tag', 'to_tag']
    search_fields = ['^callid']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(Acc, AccAdmin)


class AccCdrAdminForm(forms.ModelForm):

    class Meta:
        model = AccCdr
        fields = '__all__'


class AccCdrAdmin(admin.ModelAdmin):
    form = AccCdrAdminForm
    list_display = [
        'orig_customer',
        'term_customer',
        'direction',
        'caller',
        'callee',
        'called_did',
        'start_time',
        'duration',
        'callid'
    ]
    # readonly_fields = ['company_id', 'direction', 'caller', 'callee', 'start_time', 'end_time', 'duration', 'callid']
    search_fields = ['^caller', '^callee']
    list_filter = ['direction']
    actions = None
    log_change = False
    message_user = False
    show_full_result_count = False
    view_on_site = False

    fieldsets = (
        (_(u'General'), {
            'fields': (('orig_customer', 'term_customer'),
                       ('orig_provider', 'term_provider'),
                       ('start_time', 'duration'),
                       'callee',
                       ('e164_called', 'called_destination'),
                       'caller',
                       ('e164_caller', 'caller_destination'),
                       ('called_did', 'did_destination'),
                       ('direction', 'leg_a_class', 'leg_b_class'))
        }),
        (_(u'Advanced date / duration infos'), {
            'fields': (('answered_time', 'end_time'))
        }),
        (_(u'Financial infos'), {
            'fields': (('o_c_rate_type', 'o_c_rate_id'),
                       ('t_c_rate_type', 't_c_rate_id'),
                       ('o_p_rate_type', 'o_p_rate_id'),
                       ('t_p_rate_type', 't_p_rate_id'))
        }),
        (_(u'Call detailed infos'), {
            'fields': (('sip_rtp_rxstat', 'sip_rtp_txstat'),
                       ('sip_code', 'sip_reason'),
                       ('sip_charge_info', 'sip_user_agent'),
                       'callid',
                       ('kamailio_server', 'media_server'),
                       'processed')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AccCdr, AccCdrAdmin)


class MissedCallAdminForm(forms.ModelForm):

    class Meta:
        model = MissedCall
        fields = '__all__'


class MissedCallAdmin(admin.ModelAdmin):
    form = MissedCallAdminForm
    list_display = [
        'method',
        'from_tag',
        'to_tag',
        'callid',
        'sip_code',
        'sip_reason',
        'time'
    ]
    # readonly_fields = ['src_ip', 'method', 'from_user', 'from_domain', 'ruri_user', 'ruri_domain', 'callid', 'sip_code', 'sip_reason', 'time', 'time_attr', 'time_exten', 'cseq', 'ruri_user', 'ruri_domain', 'from_tag', 'to_tag']
    search_fields = ['^callid']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(MissedCall, MissedCallAdmin)


class UacRegAdminForm(forms.ModelForm):

    class Meta:
        model = UacReg
        fields = '__all__'


class UacRegAdmin(admin.ModelAdmin):
    form = UacRegAdminForm
    readonly_fields=['flags']
    list_display = ['l_uuid', 'l_username', 'l_domain', 'r_username', 'r_domain', 'realm', 'auth_username', 'auth_password', 'auth_ha1', 'auth_proxy', 'expires', 'flags', 'reg_delay', 'socket']
    # readonly_fields = ['l_uuid', 'l_username', 'l_domain', 'r_username', 'r_domain', 'realm', 'auth_username', 'auth_password', 'auth_ha1', 'auth_proxy', 'expires', 'flags', 'reg_delay']


admin.site.register(UacReg, UacRegAdmin)


class TrustedAdminForm(forms.ModelForm):

    class Meta:
        model = Trusted
        fields = '__all__'


class TrustedAdmin(admin.ModelAdmin):
    form = TrustedAdminForm
    list_display = ['src_ip', 'proto', 'from_pattern', 'ruri_pattern', 'tag', 'priority']
    # readonly_fields = ['src_ip', 'proto', 'from_pattern', 'ruri_pattern', 'tag', 'priority']


admin.site.register(Trusted, TrustedAdmin)


class VersionAdminForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


class VersionAdmin(admin.ModelAdmin):
    form = VersionAdminForm
    list_display = ['table_name', 'table_version']
    # readonly_fields = ['table_name', 'table_version']


admin.site.register(Version, VersionAdmin)


class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'


class LocationAdmin(admin.ModelAdmin):
    form = LocationAdminForm
    list_display = [
        'username',
        'domain',
        'received',
        'expires',
        'last_modified',
        'user_agent'
    ]
    # readonly_fields = ['ruid', 'username', 'domain', 'contact', 'received', 'path', 'expires', 'q', 'callid', 'cseq', 'last_modified', 'flags', 'cflags', 'user_agent', 'socket', 'methods', 'instance', 'reg_id', 'server_id', 'connection_id', 'keepalive', 'partition']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(Location, LocationAdmin)


class LocationAttrsAdminForm(forms.ModelForm):

    class Meta:
        model = LocationAttrs
        fields = '__all__'


class LocationAttrsAdmin(admin.ModelAdmin):
    form = LocationAttrsAdminForm
    list_display = ['ruid', 'username', 'domain', 'aname', 'atype', 'avalue', 'last_modified']
    # readonly_fields = ['ruid', 'username', 'domain', 'aname', 'atype', 'avalue', 'last_modified']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(LocationAttrs, LocationAttrsAdmin)


class UserBlackListAdminForm(forms.ModelForm):

    class Meta:
        model = UserBlackList
        fields = '__all__'


class UserBlackListAdmin(admin.ModelAdmin):
    form = UserBlackListAdminForm
    list_display = ['username', 'domain', 'prefix', 'whitelist']
    # readonly_fields = ['username', 'domain', 'prefix', 'whitelist']


admin.site.register(UserBlackList, UserBlackListAdmin)


class GlobalBlackListAdminForm(forms.ModelForm):

    class Meta:
        model = GlobalBlackList
        fields = '__all__'


class GlobalBlackListAdmin(admin.ModelAdmin):
    form = GlobalBlackListAdminForm
    list_display = ['prefix', 'whitelist', 'description']
    # readonly_fields = ['prefix', 'whitelist', 'description']


admin.site.register(GlobalBlackList, GlobalBlackListAdmin)


class SpeedDialAdminForm(forms.ModelForm):

    class Meta:
        model = SpeedDial
        fields = '__all__'


class SpeedDialAdmin(admin.ModelAdmin):
    form = SpeedDialAdminForm
    list_display = ['username', 'domain', 'sd_username', 'sd_domain', 'new_uri', 'fname', 'lname', 'description']
    # readonly_fields = ['username', 'domain', 'sd_username', 'sd_domain', 'new_uri', 'fname', 'lname', 'description']


admin.site.register(SpeedDial, SpeedDialAdmin)


class PipeLimitAdminForm(forms.ModelForm):

    class Meta:
        model = PipeLimit
        fields = '__all__'


class PipeLimitAdmin(admin.ModelAdmin):
    form = PipeLimitAdminForm
    list_display = ['pipeid', 'algorithm', 'plimit']
    # readonly_fields = ['pipeid', 'algorithm', 'plimit']


admin.site.register(PipeLimit, PipeLimitAdmin)


class MtreeAdminForm(forms.ModelForm):

    class Meta:
        model = Mtree
        fields = '__all__'


class MtreeAdmin(admin.ModelAdmin):
    form = MtreeAdminForm
    list_display = ['tprefix', 'tvalue']
    readonly_fields = ['tprefix', 'tvalue']


admin.site.register(Mtree, MtreeAdmin)


class MtreesAdminForm(forms.ModelForm):

    class Meta:
        model = Mtrees
        fields = '__all__'


class MtreesAdmin(admin.ModelAdmin):
    form = MtreesAdminForm
    list_display = ['tname', 'tprefix', 'tvalue']
    readonly_fields = ['tname', 'tprefix', 'tvalue']


admin.site.register(Mtrees, MtreesAdmin)


class HtableAdminForm(forms.ModelForm):

    class Meta:
        model = Htable
        fields = '__all__'


class HtableAdmin(admin.ModelAdmin):
    form = HtableAdminForm
    list_display = ['key_name', 'key_type', 'value_type', 'key_value', 'expires']
    readonly_fields = ['key_name', 'key_type', 'value_type', 'key_value', 'expires']


admin.site.register(Htable, HtableAdmin)


class RtpEngineAdminForm(forms.ModelForm):

    class Meta:
        model = RtpEngine
        fields = '__all__'


class RtpEngineAdmin(admin.ModelAdmin):
    form = RtpEngineAdminForm
    list_display = ['setid', 'url', 'weight', 'disabled', 'stamp']
    # readonly_fields = ['setid', 'url', 'weight', 'disabled', 'stamp']


admin.site.register(RtpEngine, RtpEngineAdmin)


class StatisticAdminForm(forms.ModelForm):

    class Meta:
        model = Statistic
        fields = '__all__'


class StatisticAdmin(admin.ModelAdmin):
    form = StatisticAdminForm
    list_display = ['kamailio_id', 'time_stamp', 'random', 'shm_used_size', 'shm_real_used_size', 'shm_max_used_size', 'shm_free_used_size', 'ul_users', 'ul_contacts']
    # readonly_fields = ['kamailio_id', 'time_stamp', 'random', 'shm_used_size', 'shm_real_used_size', 'shm_max_used_size', 'shm_free_used_size', 'ul_users', 'ul_contacts']

    def get_readonly_fields(self, request, obj=None):
        # make all fields readonly
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.register(Statistic, StatisticAdmin)

from django.contrib import admin
from django import forms
from .models import Version, Location, LocationAttrs, UserBlackList, GlobalBlackList, SpeedDial, PipeLimit, Mtree, Mtrees, Htable

class VersionAdminForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'


class VersionAdmin(admin.ModelAdmin):
    form = VersionAdminForm
    list_display = ['table_name', 'table_version']
    readonly_fields = ['table_name', 'table_version']

admin.site.register(Version, VersionAdmin)


class LocationAdminForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = '__all__'


class LocationAdmin(admin.ModelAdmin):
    form = LocationAdminForm
    list_display = ['ruid', 'username', 'domain', 'contact', 'received', 'path', 'expires', 'q', 'callid', 'cseq', 'last_modified', 'flags', 'cfags', 'user_agent', 'socket', 'methods', 'instance', 'reg_id', 'server_id', 'connection_id', 'keepalive', 'partition']
    readonly_fields = ['ruid', 'username', 'domain', 'contact', 'received', 'path', 'expires', 'q', 'callid', 'cseq', 'last_modified', 'flags', 'cfags', 'user_agent', 'socket', 'methods', 'instance', 'reg_id', 'server_id', 'connection_id', 'keepalive', 'partition']

admin.site.register(Location, LocationAdmin)


class LocationAttrsAdminForm(forms.ModelForm):

    class Meta:
        model = LocationAttrs
        fields = '__all__'


class LocationAttrsAdmin(admin.ModelAdmin):
    form = LocationAttrsAdminForm
    list_display = ['ruid', 'username', 'domain', 'aname', 'atype', 'avalue', 'last_modified']
    readonly_fields = ['ruid', 'username', 'domain', 'aname', 'atype', 'avalue', 'last_modified']

admin.site.register(LocationAttrs, LocationAttrsAdmin)


class UserBlackListAdminForm(forms.ModelForm):

    class Meta:
        model = UserBlackList
        fields = '__all__'


class UserBlackListAdmin(admin.ModelAdmin):
    form = UserBlackListAdminForm
    list_display = ['username', 'domain', 'prefix', 'whitelist']
    readonly_fields = ['username', 'domain', 'prefix', 'whitelist']

admin.site.register(UserBlackList, UserBlackListAdmin)


class GlobalBlackListAdminForm(forms.ModelForm):

    class Meta:
        model = GlobalBlackList
        fields = '__all__'


class GlobalBlackListAdmin(admin.ModelAdmin):
    form = GlobalBlackListAdminForm
    list_display = ['prefix', 'whitelist', 'description']
    readonly_fields = ['prefix', 'whitelist', 'description']

admin.site.register(GlobalBlackList, GlobalBlackListAdmin)


class SpeedDialAdminForm(forms.ModelForm):

    class Meta:
        model = SpeedDial
        fields = '__all__'


class SpeedDialAdmin(admin.ModelAdmin):
    form = SpeedDialAdminForm
    list_display = ['username', 'domain', 'sd_username', 'sd_domain', 'new_uri', 'fname', 'lname', 'description']
    readonly_fields = ['username', 'domain', 'sd_username', 'sd_domain', 'new_uri', 'fname', 'lname', 'description']

admin.site.register(SpeedDial, SpeedDialAdmin)


class PipeLimitAdminForm(forms.ModelForm):

    class Meta:
        model = PipeLimit
        fields = '__all__'


class PipeLimitAdmin(admin.ModelAdmin):
    form = PipeLimitAdminForm
    list_display = ['pipeid', 'algorithm', 'plimit']
    readonly_fields = ['pipeid', 'algorithm', 'plimit']

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



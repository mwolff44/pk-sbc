from django.contrib import admin
from django import forms
from .models import UacReg, Trusted

class UacRegAdminForm(forms.ModelForm):

    class Meta:
        model = UacReg
        fields = '__all__'


class UacRegAdmin(admin.ModelAdmin):
    form = UacRegAdminForm
    list_display = ['l_uuid', 'l_username', 'l_domain', 'r_username', 'r_domain', 'realm', 'auth_username', 'auth_password', 'auth_ha1', 'auth_proxy', 'expires', 'flags', 'reg_delay']
    readonly_fields = ['l_uuid', 'l_username', 'l_domain', 'r_username', 'r_domain', 'realm', 'auth_username', 'auth_password', 'auth_ha1', 'auth_proxy', 'expires', 'flags', 'reg_delay']

admin.site.register(UacReg, UacRegAdmin)


class TrustedAdminForm(forms.ModelForm):

    class Meta:
        model = Trusted
        fields = '__all__'


class TrustedAdmin(admin.ModelAdmin):
    form = TrustedAdminForm
    list_display = ['src_ip', 'proto', 'from_pattern', 'ruri_pattern', 'tag', 'priority']
    readonly_fields = ['src_ip', 'proto', 'from_pattern', 'ruri_pattern', 'tag', 'priority']

admin.site.register(Trusted, TrustedAdmin)



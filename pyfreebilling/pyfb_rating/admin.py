# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from pyfb_company.models import Customer
from pyfb_company.admin import CustomerAdmin

from .models import CallerNumList, ProviderRatecard, CustomerRatecard, CustomerRcAllocation, CustomerPrefixRate, ProviderPrefixRate, CustomerDestinationRate, ProviderDestinationRate, CustomerCountryTypeRate, ProviderCountryTypeRate, CustomerCountryRate, ProviderCountryRate, CustomerRegionTypeRate, ProviderRegionTypeRate, CustomerRegionRate, ProviderRegionRate, CustomerDefaultRate, ProviderDefaultRate

class CallerNumListAdminForm(forms.ModelForm):

    class Meta:
        model = CallerNumList
        fields = '__all__'


class CallerNumListAdmin(admin.ModelAdmin):
    form = CallerNumListAdminForm
    list_display = ['name', 'slug', 'callerid_filter']
    readonly_fields = ['slug',]
    filter_horizontal = ('destination',)
    autocomplete_fields = ['destination']

admin.site.register(CallerNumList, CallerNumListAdmin)


class ProviderPrefixRateInline(admin.TabularInline):
    model = ProviderPrefixRate
    fields = ['prefix', 'destnum_length', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderDestinationRateInline(admin.TabularInline):
    model = ProviderDestinationRate
    fields = ['destination', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderCountryTypeRateInline(admin.TabularInline):
    model = ProviderCountryTypeRate
    fields = ['country', 'type', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderCountryRateInline(admin.TabularInline):
    model = ProviderCountryRate
    fields = ['country', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderRegionTypeRateInline(admin.TabularInline):
    model = ProviderRegionTypeRate
    fields = ['region', 'type', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderRegionRateInline(admin.TabularInline):
    model = ProviderRegionRate
    fields = ['region', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderDefaultRateInline(admin.TabularInline):
    model = ProviderDefaultRate
    fields = ['r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class ProviderRatecardAdminForm(forms.ModelForm):
    # date_validity = DateTimeRangeField(widget=RangeWidget(AdminDateTime())

    class Meta:
        model = ProviderRatecard
        fields = '__all__'


class ProviderRatecardAdmin(admin.ModelAdmin):
    form = ProviderRatecardAdminForm
    list_display = ['id', 'name', 'provider', 'rc_type', 'callerid_list', 'status', 'provider_prefix', 'estimated_quality', 'date_start', 'date_end',]
    readonly_fields = ['id', 'slug', 'status_changed', 'created', 'modified']
    fieldsets = (
        (_(u'Ratecard details'), {
            'fields': (
                ('name', 'provider', 'status'),
                ('rc_type', 'callerid_list'),
                ('provider_prefix', 'estimated_quality'),
                ('date_start', 'date_end'),
            ),
        }),
        (_(u'More -- view description and event dates'), {
            'fields': (
                'description',
                ('created', 'modified'),
                'status_changed',
            ),
            'classes': ('collapse',),
        }),
    )
    list_filter = ['status', 'rc_type']
    search_fields = ['description', '^name']
    inlines = [
        ProviderPrefixRateInline,
        ProviderDestinationRateInline,
        ProviderCountryTypeRateInline,
        ProviderCountryRateInline,
        ProviderRegionTypeRateInline,
        ProviderRegionRateInline,
        ProviderDefaultRateInline,
    ]

admin.site.register(ProviderRatecard, ProviderRatecardAdmin)


class CustomerPrefixRateInline(admin.TabularInline):
    model = CustomerPrefixRate
    fields = ['prefix', 'destnum_length', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerDestinationRateInline(admin.TabularInline):
    model = CustomerDestinationRate
    fields = ['destination', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerCountryTypeRateInline(admin.TabularInline):
    model = CustomerCountryTypeRate
    fields = ['country', 'type', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerCountryRateInline(admin.TabularInline):
    model = CustomerCountryRate
    fields = ['country', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerRegionTypeRateInline(admin.TabularInline):
    model = CustomerRegionTypeRate
    fields = ['region', 'type', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerRegionRateInline(admin.TabularInline):
    model = CustomerRegionRate
    fields = ['region', 'r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerDefaultRateInline(admin.TabularInline):
    model = CustomerDefaultRate
    fields = ['r_rate', 'r_block_min_duration', 'r_minimal_time', 'r_init_block', 'status']
    #formset = CustomerPrefixRateFormSet
    max_num = 40
    extra = 0


class CustomerRcAllocationInline(admin.TabularInline):
    model = CustomerRcAllocation
    fields = ['priority', 'ratecard', 'discount', 'allow_negative_margin', 'tech_prefix', 'description']
    description = _(u'select the Ratecards affected to customer account. Order is important !')
    max_num = 7
    extra = 0
    modal = True


class CustomerRCAdmin(CustomerAdmin):
    inlines = [CustomerRcAllocationInline]

admin.site.unregister(Customer)
admin.site.register(Customer, CustomerRCAdmin)


class CustomerRatecardAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerRatecard
        fields = '__all__'


class CustomerRatecardAdmin(admin.ModelAdmin):
    form = CustomerRatecardAdminForm
    list_display = ['id', 'name', 'rc_type', 'callerid_list', 'status', 'date_start', 'date_end']
    readonly_fields = ['id', 'slug', 'status_changed', 'created', 'modified']
    fieldsets = (
        (_(u'Ratecard details'), {
            'fields': (
                ('name', 'status'),
                ('rc_type', 'callerid_list'),
                ('date_start', 'date_end'),
            ),
        }),
        (_(u'More -- view description and event dates'), {
            'fields': (
                'description',
                ('created', 'modified'),
                'status_changed',
            ),
            'classes': ('collapse',),
        }),
    )
    list_filter = ['status', 'rc_type', 'callerid_list']
    search_fields = ['description', '^name']
    inlines = [
        CustomerPrefixRateInline,
        CustomerDestinationRateInline,
        CustomerCountryTypeRateInline,
        CustomerCountryRateInline,
        CustomerRegionTypeRateInline,
        CustomerRegionRateInline,
        CustomerDefaultRateInline,
    ]

admin.site.register(CustomerRatecard, CustomerRatecardAdmin)


class CustomerRcAllocationAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerRcAllocation
        fields = '__all__'


class CustomerRcAllocationAdmin(admin.ModelAdmin):
    form = CustomerRcAllocationAdminForm
    list_display = ['customer', 'priority', 'ratecard', 'tech_prefix', 'discount', 'allow_negative_margin']
    # readonly_fields = ['tech_prefix', 'priority', 'discount', 'allow_negative_margin', 'description']

admin.site.register(CustomerRcAllocation, CustomerRcAllocationAdmin)


class CustomerPrefixRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerPrefixRate
        fields = '__all__'


class CustomerPrefixRateAdmin(admin.ModelAdmin):
    form = CustomerPrefixRateAdminForm
    list_display = ['prefix', 'destnum_length', 'r_rate', 'status',]
    # readonly_fields = ['prefix', 'destnum_length']

admin.site.register(CustomerPrefixRate, CustomerPrefixRateAdmin)


class ProviderPrefixRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderPrefixRate
        fields = '__all__'


class ProviderPrefixRateAdmin(admin.ModelAdmin):
    form = ProviderPrefixRateAdminForm
    list_display = ['prefix', 'destnum_length', 'r_rate', 'status',]
    # readonly_fields = ['prefix', 'destnum_length']

admin.site.register(ProviderPrefixRate, ProviderPrefixRateAdmin)


class CustomerDestinationRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerDestinationRate
        fields = '__all__'


class CustomerDestinationRateAdmin(admin.ModelAdmin):
    form = CustomerDestinationRateAdminForm


admin.site.register(CustomerDestinationRate, CustomerDestinationRateAdmin)


class ProviderDestinationRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderDestinationRate
        fields = '__all__'


class ProviderDestinationRateAdmin(admin.ModelAdmin):
    form = ProviderDestinationRateAdminForm


admin.site.register(ProviderDestinationRate, ProviderDestinationRateAdmin)


class CustomerCountryTypeRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerCountryTypeRate
        fields = '__all__'


class CustomerCountryTypeRateAdmin(admin.ModelAdmin):
    form = CustomerCountryTypeRateAdminForm


admin.site.register(CustomerCountryTypeRate, CustomerCountryTypeRateAdmin)


class ProviderCountryTypeRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderCountryTypeRate
        fields = '__all__'


class ProviderCountryTypeRateAdmin(admin.ModelAdmin):
    form = ProviderCountryTypeRateAdminForm


admin.site.register(ProviderCountryTypeRate, ProviderCountryTypeRateAdmin)


class CustomerCountryRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerCountryRate
        fields = '__all__'


class CustomerCountryRateAdmin(admin.ModelAdmin):
    form = CustomerCountryRateAdminForm


admin.site.register(CustomerCountryRate, CustomerCountryRateAdmin)


class ProviderCountryRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderCountryRate
        fields = '__all__'


class ProviderCountryRateAdmin(admin.ModelAdmin):
    form = ProviderCountryRateAdminForm


admin.site.register(ProviderCountryRate, ProviderCountryRateAdmin)


class CustomerRegionTypeRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerRegionTypeRate
        fields = '__all__'


class CustomerRegionTypeRateAdmin(admin.ModelAdmin):
    form = CustomerRegionTypeRateAdminForm


admin.site.register(CustomerRegionTypeRate, CustomerRegionTypeRateAdmin)


class ProviderRegionTypeRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderRegionTypeRate
        fields = '__all__'


class ProviderRegionTypeRateAdmin(admin.ModelAdmin):
    form = ProviderRegionTypeRateAdminForm


admin.site.register(ProviderRegionTypeRate, ProviderRegionTypeRateAdmin)


class CustomerRegionRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerRegionRate
        fields = '__all__'


class CustomerRegionRateAdmin(admin.ModelAdmin):
    form = CustomerRegionRateAdminForm


admin.site.register(CustomerRegionRate, CustomerRegionRateAdmin)


class ProviderRegionRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderRegionRate
        fields = '__all__'


class ProviderRegionRateAdmin(admin.ModelAdmin):
    form = ProviderRegionRateAdminForm


admin.site.register(ProviderRegionRate, ProviderRegionRateAdmin)


class CustomerDefaultRateAdminForm(forms.ModelForm):

    class Meta:
        model = CustomerDefaultRate
        fields = '__all__'


class CustomerDefaultRateAdmin(admin.ModelAdmin):
    form = CustomerDefaultRateAdminForm


admin.site.register(CustomerDefaultRate, CustomerDefaultRateAdmin)


class ProviderDefaultRateAdminForm(forms.ModelForm):

    class Meta:
        model = ProviderDefaultRate
        fields = '__all__'


class ProviderDefaultRateAdmin(admin.ModelAdmin):
    form = ProviderDefaultRateAdminForm


admin.site.register(ProviderDefaultRate, ProviderDefaultRateAdmin)

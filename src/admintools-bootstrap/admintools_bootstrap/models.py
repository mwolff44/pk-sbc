
# monkey-pathching django admin

from django.contrib.admin import widgets
from django import forms

class FilteredSelectMultiple(forms.SelectMultiple):
    """
        removing 2 select fields widget
    """
    def __init__(self, verbose_name, is_stacked, attrs=None, choices=[]):
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

widgets.FilteredSelectMultiple = FilteredSelectMultiple

# using jquery ui do display .vDateField
widgets.AdminDateWidget.media = None

# patching admintools menu item

from admin_tools.menu import items

# addming icon argument to base MenuItem class
items.MenuItem.icon = None


import admintools_bootstrap.settings

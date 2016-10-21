# coding: utf-8
# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

# from __future__ import unicode_literals
# from django.template import Library, template


# register = template.Library()
# @register.inclusion_tag('pyfreebilling:components/component.html', takes_context=True)
# def dashboard(context, id, *args, **kwargs):       # The template tag
#     return component_context(
#         context,
#         "LineChartJSONView",                           # The custom view's CSS class name
#         id,
#         "view",
#         "pyfreebill/dashboard",             # Path to the JavaScript class/file for the view
#         kwargs
#     )


# register = Library()


# # Initial code from dezede https://github.com/dezede
# @register.assignment_tag(takes_context=True)
# def get_fieldsets_and_inlines(context):
#     adminform = context['adminform']
#     model_admin = adminform.model_admin
#     adminform = iter(adminform)
#     inlines = iter(context['inline_admin_formsets'])

#     fieldsets_and_inlines = []
#     for choice in getattr(model_admin, 'fieldsets_and_inlines_order', ()):
#         if choice == 'f':
#             fieldsets_and_inlines.append(('f', adminform.next()))
#         elif choice == 'i':
#             fieldsets_and_inlines.append(('i', inlines.next()))

#     for fieldset in adminform:
#         fieldsets_and_inlines.append(('f', fieldset))
#     for inline in inlines:
#         fieldsets_and_inlines.append(('i', inline))

#     return fieldsets_and_inlines

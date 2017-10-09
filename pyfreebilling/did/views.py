# -*- coding: utf-8 -*-
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling. If not, see <http://www.gnu.org/licenses/>

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django import forms

#from simple_import.models import ImportSetting
#from simple_import.views import match_columns
#from simple_import.models import ImportLog


#class ImportForm(forms.ModelForm):
    #class Meta:
        #model = ImportLog
        #fields = ('name', 'import_file', 'import_type')


#@staff_member_required
#def start_import(request):
    #""" View to create a new import record
    #"""
    #if request.method == 'POST':
        #form = ImportForm(request.POST, request.FILES)
        #if form.is_valid():
            #import_log = form.save(commit=False)
            #import_log.user = request.user
            #import_log.import_setting, created = ImportSetting.objects.get_or_create(
                #user=request.user,
                #content_type=ContentType.objects.get(model='did'),
            #)
            #import_log.save()
            #return HttpResponseRedirect(reverse(match_columns,
                                        #kwargs={'import_log_id': import_log.id}))
    #else:
        #form = ImportForm()
    #if not request.user.is_superuser:
        #form.fields["model"].queryset = ContentType.objects.filter(
            #Q(permission__group__user=request.user, permission__codename__startswith="change_") |
            #Q(permission__user=request.user, permission__codename__startswith="change_")).distinct()

    #return render_to_response('admin/did/did/simple_import/import.html',
                              #{'form': form, },
                              #RequestContext(request, {}), )

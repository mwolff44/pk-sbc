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

from django.conf.urls import *
from django.contrib import admin
from django.http import HttpResponseRedirect

admin.autodiscover()

def index(request):
    return HttpResponseRedirect('/extranet/')

urlpatterns = patterns('',
    url(r'^extranet/report/$', 'pyfreebill.views.admin_report_view'),
    url(r'^extranet/status/$', 'pyfreebill.views.admin_status_view'),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include('admin_honeypot.urls')),
    url(r'^extranet/', include(admin.site.urls)),
#    url(r'^extranet/reporting/', include('reporting.urls')),
)

from django.conf.urls import *
from django.contrib import admin
from django.http import HttpResponseRedirect

admin.autodiscover()

def index(request):
    return HttpResponseRedirect('/extranet/')

urlpatterns = patterns('',
    url(r'^extranet/report/$', 'pyfreebill.views.admin_report_view'),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', include('admin_honeypot.urls')),
    url(r'^extranet/', include(admin.site.urls)),
#    url(r'^extranet/reporting/', include('reporting.urls')),
)

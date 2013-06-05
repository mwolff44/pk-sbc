from django.conf.urls import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/report/$', 'pyfreebill.views.admin_report_view'),
    url(r'^grappelli/', include('grappelli.urls')),
#    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/', include('admin_honeypot.urls')),
    url(r'^extranet/', include(admin.site.urls)),
)

from django.conf.urls import *
from django.contrib import admin
#from adminplus.sites import AdminSitePlus

#admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/report/$', 'pyfreebill.admin_views.report'),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

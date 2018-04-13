from django.conf.urls import url, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'acc', api.AccViewSet)
router.register(r'acccdr', api.AccCdrViewSet)
router.register(r'missedcall', api.MissedCallViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Acc
    url(r'^accounting/acc/$', views.AccListView.as_view(), name='accounting_acc_list'),
    url(r'^accounting/acc/create/$', views.AccCreateView.as_view(), name='accounting_acc_create'),
    url(r'^accounting/acc/detail/(?P<pk>\S+)/$', views.AccDetailView.as_view(), name='accounting_acc_detail'),
    url(r'^accounting/acc/update/(?P<pk>\S+)/$', views.AccUpdateView.as_view(), name='accounting_acc_update'),
)

urlpatterns += (
    # urls for AccCdr
    url(r'^accounting/acccdr/$', views.AccCdrListView.as_view(), name='accounting_acccdr_list'),
    url(r'^accounting/acccdr/create/$', views.AccCdrCreateView.as_view(), name='accounting_acccdr_create'),
    url(r'^accounting/acccdr/detail/(?P<pk>\S+)/$', views.AccCdrDetailView.as_view(), name='accounting_acccdr_detail'),
    url(r'^accounting/acccdr/update/(?P<pk>\S+)/$', views.AccCdrUpdateView.as_view(), name='accounting_acccdr_update'),
)

urlpatterns += (
    # urls for MissedCall
    url(r'^accounting/missedcall/$', views.MissedCallListView.as_view(), name='accounting_missedcall_list'),
    url(r'^accounting/missedcall/create/$', views.MissedCallCreateView.as_view(), name='accounting_missedcall_create'),
    url(r'^accounting/missedcall/detail/(?P<pk>\S+)/$', views.MissedCallDetailView.as_view(), name='accounting_missedcall_detail'),
    url(r'^accounting/missedcall/update/(?P<pk>\S+)/$', views.MissedCallUpdateView.as_view(), name='accounting_missedcall_update'),
)


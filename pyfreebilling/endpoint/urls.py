from django.conf.urls import url, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'uacreg', api.UacRegViewSet)
router.register(r'trusted', api.TrustedViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for UacReg
    url(r'^endpoint/uacreg/$', views.UacRegListView.as_view(), name='endpoint_uacreg_list'),
    url(r'^endpoint/uacreg/create/$', views.UacRegCreateView.as_view(), name='endpoint_uacreg_create'),
    url(r'^endpoint/uacreg/detail/(?P<pk>\S+)/$', views.UacRegDetailView.as_view(), name='endpoint_uacreg_detail'),
    url(r'^endpoint/uacreg/update/(?P<pk>\S+)/$', views.UacRegUpdateView.as_view(), name='endpoint_uacreg_update'),
)

urlpatterns += (
    # urls for Trusted
    url(r'^endpoint/trusted/$', views.TrustedListView.as_view(), name='endpoint_trusted_list'),
    url(r'^endpoint/trusted/create/$', views.TrustedCreateView.as_view(), name='endpoint_trusted_create'),
    url(r'^endpoint/trusted/detail/(?P<pk>\S+)/$', views.TrustedDetailView.as_view(), name='endpoint_trusted_detail'),
    url(r'^endpoint/trusted/update/(?P<pk>\S+)/$', views.TrustedUpdateView.as_view(), name='endpoint_trusted_update'),
)


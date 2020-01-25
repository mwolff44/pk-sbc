from django.conf.urls import url, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'destination', api.DestinationViewSet)
router.register(r'prefix', api.PrefixViewSet)
router.register(r'carrier', api.CarrierViewSet)
router.register(r'region', api.RegionViewSet)
router.register(r'country', api.CountryViewSet)
router.register(r'type', api.TypeViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Destination
    url(r'^direction/destination/$', views.DestinationListView.as_view(), name='direction_destination_list'),
    url(r'^direction/destination/create/$', views.DestinationCreateView.as_view(), name='direction_destination_create'),
    url(r'^direction/destination/detail/(?P<slug>\S+)/$', views.DestinationDetailView.as_view(), name='direction_destination_detail'),
    url(r'^direction/destination/update/(?P<slug>\S+)/$', views.DestinationUpdateView.as_view(), name='direction_destination_update'),
)

urlpatterns += (
    # urls for Prefix
    url(r'^direction/prefix/$', views.PrefixListView.as_view(), name='direction_prefix_list'),
    url(r'^direction/prefix/create/$', views.PrefixCreateView.as_view(), name='direction_prefix_create'),
    url(r'^direction/prefix/detail/(?P<slug>\S+)/$', views.PrefixDetailView.as_view(), name='direction_prefix_detail'),
    url(r'^direction/prefix/update/(?P<slug>\S+)/$', views.PrefixUpdateView.as_view(), name='direction_prefix_update'),
)

urlpatterns += (
    # urls for Carrier
    url(r'^direction/carrier/$', views.CarrierListView.as_view(), name='direction_carrier_list'),
    url(r'^direction/carrier/create/$', views.CarrierCreateView.as_view(), name='direction_carrier_create'),
    url(r'^direction/carrier/detail/(?P<slug>\S+)/$', views.CarrierDetailView.as_view(), name='direction_carrier_detail'),
    url(r'^direction/carrier/update/(?P<slug>\S+)/$', views.CarrierUpdateView.as_view(), name='direction_carrier_update'),
)

urlpatterns += (
    # urls for Region
    url(r'^direction/region/$', views.RegionListView.as_view(), name='direction_region_list'),
    url(r'^direction/region/create/$', views.RegionCreateView.as_view(), name='direction_region_create'),
    url(r'^direction/region/detail/(?P<slug>\S+)/$', views.RegionDetailView.as_view(), name='direction_region_detail'),
    url(r'^direction/region/update/(?P<slug>\S+)/$', views.RegionUpdateView.as_view(), name='direction_region_update'),
)

urlpatterns += (
    # urls for Country
    url(r'^direction/country/$', views.CountryListView.as_view(), name='direction_country_list'),
    url(r'^direction/country/create/$', views.CountryCreateView.as_view(), name='direction_country_create'),
    url(r'^direction/country/detail/(?P<pk>\S+)/$', views.CountryDetailView.as_view(), name='direction_country_detail'),
    url(r'^direction/country/update/(?P<pk>\S+)/$', views.CountryUpdateView.as_view(), name='direction_country_update'),
)

urlpatterns += (
    # urls for Type
    url(r'^direction/type/$', views.TypeListView.as_view(), name='direction_type_list'),
    url(r'^direction/type/create/$', views.TypeCreateView.as_view(), name='direction_type_create'),
    url(r'^direction/type/detail/(?P<slug>\S+)/$', views.TypeDetailView.as_view(), name='direction_type_detail'),
    url(r'^direction/type/update/(?P<slug>\S+)/$', views.TypeUpdateView.as_view(), name='direction_type_update'),
)


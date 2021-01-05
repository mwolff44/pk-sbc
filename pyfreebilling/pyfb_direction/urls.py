# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb-direction'

router = routers.DefaultRouter()
router.register(r'carrier', api.CarrierViewSet)
router.register(r'type', api.TypeViewSet)
router.register(r'region', api.RegionViewSet)
router.register(r'country', api.CountryViewSet)
router.register(r'destination', api.DestinationViewSet)
router.register(r'prefix', api.PrefixViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Carrier
    path('pyfb-direction/carrier/', views.CarrierListView.as_view(), name='pyfb-direction_carrier_list'),
    path('pyfb-direction/carrier/create/', views.CarrierCreateView.as_view(), name='pyfb-direction_carrier_create'),
    path('pyfb-direction/carrier/detail/<slug:slug>/', views.CarrierDetailView.as_view(), name='pyfb-direction_carrier_detail'),
    path('pyfb-direction/carrier/update/<slug:slug>/', views.CarrierUpdateView.as_view(), name='pyfb-direction_carrier_update'),
)

urlpatterns += (
    # urls for Type
    path('pyfb-direction/type/', views.TypeListView.as_view(), name='pyfb-direction_type_list'),
    path('pyfb-direction/type/create/', views.TypeCreateView.as_view(), name='pyfb-direction_type_create'),
    path('pyfb-direction/type/detail/<slug:slug>/', views.TypeDetailView.as_view(), name='pyfb-direction_type_detail'),
    path('pyfb-direction/type/update/<slug:slug>/', views.TypeUpdateView.as_view(), name='pyfb-direction_type_update'),
)

urlpatterns += (
    # urls for Region
    path('pyfb-direction/region/', views.RegionListView.as_view(), name='pyfb-direction_region_list'),
    path('pyfb-direction/region/create/', views.RegionCreateView.as_view(), name='pyfb-direction_region_create'),
    path('pyfb-direction/region/detail/<slug:slug>/', views.RegionDetailView.as_view(), name='pyfb-direction_region_detail'),
    path('pyfb-direction/region/update/<slug:slug>/', views.RegionUpdateView.as_view(), name='pyfb-direction_region_update'),
)

urlpatterns += (
    # urls for Country
    path('pyfb-direction/country/', views.CountryListView.as_view(), name='pyfb-direction_country_list'),
    path('pyfb-direction/country/create/', views.CountryCreateView.as_view(), name='pyfb-direction_country_create'),
    path('pyfb-direction/country/detail/<int:pk>/', views.CountryDetailView.as_view(), name='pyfb-direction_country_detail'),
    path('pyfb-direction/country/update/<int:pk>/', views.CountryUpdateView.as_view(), name='pyfb-direction_country_update'),
)

urlpatterns += (
    # urls for Destination
    path('pyfb-direction/destination/', views.DestinationListView.as_view(), name='pyfb-direction_destination_list'),
    path('pyfb-direction/destination/create/', views.DestinationCreateView.as_view(), name='pyfb-direction_destination_create'),
    path('pyfb-direction/destination/detail/<slug:slug>/', views.DestinationDetailView.as_view(), name='pyfb-direction_destination_detail'),
    path('pyfb-direction/destination/update/<slug:slug>/', views.DestinationUpdateView.as_view(), name='pyfb-direction_destination_update'),
)

urlpatterns += (
    # urls for Prefix
    path('pyfb-direction/prefix/', views.PrefixListView.as_view(), name='pyfb-direction_prefix_list'),
    path('pyfb-direction/prefix/create/', views.PrefixCreateView.as_view(), name='pyfb-direction_prefix_create'),
    path('pyfb-direction/prefix/detail/<slug:slug>/', views.PrefixDetailView.as_view(), name='pyfb-direction_prefix_detail'),
    path('pyfb-direction/prefix/update/<slug:slug>/', views.PrefixUpdateView.as_view(), name='pyfb-direction_prefix_update'),
)

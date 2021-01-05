# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb-endpoint'

router = routers.DefaultRouter()
router.register(r'customerendpoint', api.CustomerEndpointViewSet)
router.register(r'codec', api.CodecViewSet)
router.register(r'providerendpoint', api.ProviderEndpointViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for CustomerEndpoint
    path('pyfb_endpoint/customerendpoint/', views.CustomerEndpointListView.as_view(), name='pyfb_endpoint_customerendpoint_list'),
    path('pyfb_endpoint/customerendpoint/create/', views.CustomerEndpointCreateView.as_view(), name='pyfb_endpoint_customerendpoint_create'),
    path('pyfb_endpoint/customerendpoint/detail/<int:pk>/', views.CustomerEndpointDetailView.as_view(), name='pyfb_endpoint_customerendpoint_detail'),
    path('pyfb_endpoint/customerendpoint/update/<int:pk>/', views.CustomerEndpointUpdateView.as_view(), name='pyfb_endpoint_customerendpoint_update'),
)

urlpatterns += (
    # urls for Codec
    path('pyfb_endpoint/codec/', views.CodecListView.as_view(), name='pyfb_endpoint_codec_list'),
    path('pyfb_endpoint/codec/create/', views.CodecCreateView.as_view(), name='pyfb_endpoint_codec_create'),
    path('pyfb_endpoint/codec/detail/<int:pk>/', views.CodecDetailView.as_view(), name='pyfb_endpoint_codec_detail'),
    path('pyfb_endpoint/codec/update/<int:pk>/', views.CodecUpdateView.as_view(), name='pyfb_endpoint_codec_update'),
)

urlpatterns += (
    # urls for ProviderEndpoint
    path('pyfb_endpoint/providerendpoint/', views.ProviderEndpointListView.as_view(), name='pyfb_endpoint_providerendpoint_list'),
    path('pyfb_endpoint/providerendpoint/create/', views.ProviderEndpointCreateView.as_view(), name='pyfb_endpoint_providerendpoint_create'),
    path('pyfb_endpoint/providerendpoint/detail/<int:pk>/', views.ProviderEndpointDetailView.as_view(), name='pyfb_endpoint_providerendpoint_detail'),
    path('pyfb_endpoint/providerendpoint/update/<int:pk>/', views.ProviderEndpointUpdateView.as_view(), name='pyfb_endpoint_providerendpoint_update'),
)

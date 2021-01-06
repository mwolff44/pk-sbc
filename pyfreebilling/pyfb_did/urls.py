# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb_did'

router = routers.DefaultRouter()
router.register(r'did', api.DidViewSet)
router.register(r'routesdid', api.RoutesDidViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Did
    path('pyfb_did/did/', views.DidListView.as_view(), name='pyfb_did_did_list'),
    path('pyfb_did/did/create/', views.DidCreateView.as_view(), name='pyfb_did_did_create'),
    path('pyfb_did/did/detail/<int:pk>/', views.DidDetailView.as_view(), name='pyfb_did_did_detail'),
    path('pyfb_did/did/update/<int:pk>/', views.DidUpdateView.as_view(), name='pyfb_did_did_update'),
)

urlpatterns += (
    # urls for RoutesDid
    path('pyfb_did/routesdid/', views.RoutesDidListView.as_view(), name='pyfb_did_routesdid_list'),
    path('pyfb_did/routesdid/create/', views.RoutesDidCreateView.as_view(), name='pyfb_did_routesdid_create'),
    path('pyfb_did/routesdid/detail/<int:pk>/', views.RoutesDidDetailView.as_view(), name='pyfb_did_routesdid_detail'),
    path('pyfb_did/routesdid/update/<int:pk>/', views.RoutesDidUpdateView.as_view(), name='pyfb_did_routesdid_update'),
)

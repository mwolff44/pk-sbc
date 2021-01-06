# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

app_name = 'pyfb_reporting'

router = routers.DefaultRouter()
router.register(r'cdr', api.CDRViewSet)
router.register(r'dimdate', api.DimDateViewSet)
router.register(r'dimcustomerhangupcause', api.DimCustomerHangupcauseViewSet)
router.register(r'dimcustomersiphangupcause', api.DimCustomerSipHangupcauseViewSet)
router.register(r'dimproviderhangupcause', api.DimProviderHangupcauseViewSet)
router.register(r'dimprovidersiphangupcause', api.DimProviderSipHangupcauseViewSet)
router.register(r'dimcustomerdestination', api.DimCustomerDestinationViewSet)
router.register(r'dimproviderdestination', api.DimProviderDestinationViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for CDR
    path('pyfb_reporting/cdr/', views.CDRListView.as_view(), name='pyfb_reporting_cdr_list'),
    path('pyfb_reporting/cdr/create/', views.CDRCreateView.as_view(), name='pyfb_reporting_cdr_create'),
    path('pyfb_reporting/cdr/detail/<int:pk>/', views.CDRDetailView.as_view(), name='pyfb_reporting_cdr_detail'),
    path('pyfb_reporting/cdr/update/<int:pk>/', views.CDRUpdateView.as_view(), name='pyfb_reporting_cdr_update'),
)

urlpatterns += (
    # urls for DimDate
    path('pyfb_reporting/dimdate/', views.DimDateListView.as_view(), name='pyfb_reporting_dimdate_list'),
    path('pyfb_reporting/dimdate/create/', views.DimDateCreateView.as_view(), name='pyfb_reporting_dimdate_create'),
    path('pyfb_reporting/dimdate/detail/<int:pk>/', views.DimDateDetailView.as_view(), name='pyfb_reporting_dimdate_detail'),
    path('pyfb_reporting/dimdate/update/<int:pk>/', views.DimDateUpdateView.as_view(), name='pyfb_reporting_dimdate_update'),
)

urlpatterns += (
    # urls for DimCustomerHangupcause
    path('pyfb_reporting/dimcustomerhangupcause/', views.DimCustomerHangupcauseListView.as_view(), name='pyfb_reporting_dimcustomerhangupcause_list'),
    path('pyfb_reporting/dimcustomerhangupcause/create/', views.DimCustomerHangupcauseCreateView.as_view(), name='pyfb_reporting_dimcustomerhangupcause_create'),
    path('pyfb_reporting/dimcustomerhangupcause/detail/<int:pk>/', views.DimCustomerHangupcauseDetailView.as_view(), name='pyfb_reporting_dimcustomerhangupcause_detail'),
    path('pyfb_reporting/dimcustomerhangupcause/update/<int:pk>/', views.DimCustomerHangupcauseUpdateView.as_view(), name='pyfb_reporting_dimcustomerhangupcause_update'),
)

urlpatterns += (
    # urls for DimCustomerSipHangupcause
    path('pyfb_reporting/dimcustomersiphangupcause/', views.DimCustomerSipHangupcauseListView.as_view(), name='pyfb_reporting_dimcustomersiphangupcause_list'),
    path('pyfb_reporting/dimcustomersiphangupcause/create/', views.DimCustomerSipHangupcauseCreateView.as_view(), name='pyfb_reporting_dimcustomersiphangupcause_create'),
    path('pyfb_reporting/dimcustomersiphangupcause/detail/<int:pk>/', views.DimCustomerSipHangupcauseDetailView.as_view(), name='pyfb_reporting_dimcustomersiphangupcause_detail'),
    path('pyfb_reporting/dimcustomersiphangupcause/update/<int:pk>/', views.DimCustomerSipHangupcauseUpdateView.as_view(), name='pyfb_reporting_dimcustomersiphangupcause_update'),
)

urlpatterns += (
    # urls for DimProviderHangupcause
    path('pyfb_reporting/dimproviderhangupcause/', views.DimProviderHangupcauseListView.as_view(), name='pyfb_reporting_dimproviderhangupcause_list'),
    path('pyfb_reporting/dimproviderhangupcause/create/', views.DimProviderHangupcauseCreateView.as_view(), name='pyfb_reporting_dimproviderhangupcause_create'),
    path('pyfb_reporting/dimproviderhangupcause/detail/<int:pk>/', views.DimProviderHangupcauseDetailView.as_view(), name='pyfb_reporting_dimproviderhangupcause_detail'),
    path('pyfb_reporting/dimproviderhangupcause/update/<int:pk>/', views.DimProviderHangupcauseUpdateView.as_view(), name='pyfb_reporting_dimproviderhangupcause_update'),
)

urlpatterns += (
    # urls for DimProviderSipHangupcause
    path('pyfb_reporting/dimprovidersiphangupcause/', views.DimProviderSipHangupcauseListView.as_view(), name='pyfb_reporting_dimprovidersiphangupcause_list'),
    path('pyfb_reporting/dimprovidersiphangupcause/create/', views.DimProviderSipHangupcauseCreateView.as_view(), name='pyfb_reporting_dimprovidersiphangupcause_create'),
    path('pyfb_reporting/dimprovidersiphangupcause/detail/<int:pk>/', views.DimProviderSipHangupcauseDetailView.as_view(), name='pyfb_reporting_dimprovidersiphangupcause_detail'),
    path('pyfb_reporting/dimprovidersiphangupcause/update/<int:pk>/', views.DimProviderSipHangupcauseUpdateView.as_view(), name='pyfb_reporting_dimprovidersiphangupcause_update'),
)

urlpatterns += (
    # urls for DimCustomerDestination
    path('pyfb_reporting/dimcustomerdestination/', views.DimCustomerDestinationListView.as_view(), name='pyfb_reporting_dimcustomerdestination_list'),
    path('pyfb_reporting/dimcustomerdestination/create/', views.DimCustomerDestinationCreateView.as_view(), name='pyfb_reporting_dimcustomerdestination_create'),
    path('pyfb_reporting/dimcustomerdestination/detail/<int:pk>/', views.DimCustomerDestinationDetailView.as_view(), name='pyfb_reporting_dimcustomerdestination_detail'),
    path('pyfb_reporting/dimcustomerdestination/update/<int:pk>/', views.DimCustomerDestinationUpdateView.as_view(), name='pyfb_reporting_dimcustomerdestination_update'),
)

urlpatterns += (
    # urls for DimProviderDestination
    path('pyfb_reporting/dimproviderdestination/', views.DimProviderDestinationListView.as_view(), name='pyfb_reporting_dimproviderdestination_list'),
    path('pyfb_reporting/dimproviderdestination/create/', views.DimProviderDestinationCreateView.as_view(), name='pyfb_reporting_dimproviderdestination_create'),
    path('pyfb_reporting/dimproviderdestination/detail/<int:pk>/', views.DimProviderDestinationDetailView.as_view(), name='pyfb_reporting_dimproviderdestination_detail'),
    path('pyfb_reporting/dimproviderdestination/update/<int:pk>/', views.DimProviderDestinationUpdateView.as_view(), name='pyfb_reporting_dimproviderdestination_update'),
)


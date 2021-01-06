# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb-company'

router = routers.DefaultRouter()
router.register(r'company', api.CompanyViewSet)
router.register(r'customer', api.CustomerViewSet)
router.register(r'provider', api.ProviderViewSet)
router.register(r'companybalancehistory', api.CompanyBalanceHistoryViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Company
    path('pyfb_company/company/', views.CompanyListView.as_view(), name='pyfb_company_company_list'),
    path('pyfb_company/company/create/', views.CompanyCreateView.as_view(), name='pyfb_company_company_create'),
    path('pyfb_company/company/detail/<slug:slug>/', views.CompanyDetailView.as_view(), name='pyfb_company_company_detail'),
    path('pyfb_company/company/update/<slug:slug>/', views.CompanyUpdateView.as_view(), name='pyfb_company_company_update'),
)

urlpatterns += (
    # urls for Customer
    path('pyfb_company/customer/', views.CustomerListView.as_view(), name='pyfb_company_customer_list'),
    path('pyfb_company/customer/create/', views.CustomerCreateView.as_view(), name='pyfb_company_customer_create'),
    path('pyfb_company/customer/detail/<int:pk>/', views.CustomerDetailView.as_view(), name='pyfb_company_customer_detail'),
    path('pyfb_company/customer/update/<int:pk>/', views.CustomerUpdateView.as_view(), name='pyfb_company_customer_update'),
)

urlpatterns += (
    # urls for Provider
    path('pyfb_company/provider/', views.ProviderListView.as_view(), name='pyfb_company_provider_list'),
    path('pyfb_company/provider/create/', views.ProviderCreateView.as_view(), name='pyfb_company_provider_create'),
    path('pyfb_company/provider/detail/<int:pk>/', views.ProviderDetailView.as_view(), name='pyfb_company_provider_detail'),
    path('pyfb_company/provider/update/<int:pk>/', views.ProviderUpdateView.as_view(), name='pyfb_company_provider_update'),
)

urlpatterns += (
    # urls for CompanyBalanceHistory
    path('pyfb_company/companybalancehistory/', views.CompanyBalanceHistoryListView.as_view(), name='pyfb_company_companybalancehistory_list'),
    path('pyfb_company/companybalancehistory/create/', views.CompanyBalanceHistoryCreateView.as_view(), name='pyfb_company_companybalancehistory_create'),
    path('pyfb_company/companybalancehistory/detail/<int:pk>/', views.CompanyBalanceHistoryDetailView.as_view(), name='pyfb_company_companybalancehistory_detail'),
    path('pyfb_company/companybalancehistory/update/<int:pk>/', views.CompanyBalanceHistoryUpdateView.as_view(), name='pyfb_company_companybalancehistory_update'),
)

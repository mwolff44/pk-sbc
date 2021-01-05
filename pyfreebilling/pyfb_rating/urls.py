# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb_rating'

router = routers.DefaultRouter()
router.register(r'customerrcallocation', api.CustomerRcAllocationViewSet)
router.register(r'callernumlist', api.CallerNumListViewSet)
router.register(r'providerratecard', api.ProviderRatecardViewSet)
router.register(r'customerratecard', api.CustomerRatecardViewSet)
router.register(r'customerprefixrate', api.CustomerPrefixRateViewSet)
router.register(r'providerprefixrate', api.ProviderPrefixRateViewSet)
router.register(r'customerdestinationrate', api.CustomerDestinationRateViewSet)
router.register(r'providerdestinationrate', api.ProviderDestinationRateViewSet)
router.register(r'customercountrytyperate', api.CustomerCountryTypeRateViewSet)
router.register(r'providercountrytyperate', api.ProviderCountryTypeRateViewSet)
router.register(r'customercountryrate', api.CustomerCountryRateViewSet)
router.register(r'providercountryrate', api.ProviderCountryRateViewSet)
router.register(r'customerregiontyperate', api.CustomerRegionTypeRateViewSet)
router.register(r'providerregiontyperate', api.ProviderRegionTypeRateViewSet)
router.register(r'customerregionrate', api.CustomerRegionRateViewSet)
router.register(r'providerregionrate', api.ProviderRegionRateViewSet)
router.register(r'customerdefaultrate', api.CustomerDefaultRateViewSet)
router.register(r'providerdefaultrate', api.ProviderDefaultRateViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for CustomerRcAllocation
    path('pyfb_rating/customerrcallocation/', views.CustomerRcAllocationListView.as_view(), name='pyfb_rating_customerrcallocation_list'),
    path('pyfb_rating/customerrcallocation/create/', views.CustomerRcAllocationCreateView.as_view(), name='pyfb_rating_customerrcallocation_create'),
    path('pyfb_rating/customerrcallocation/detail/<int:pk>/', views.CustomerRcAllocationDetailView.as_view(), name='pyfb_rating_customerrcallocation_detail'),
    path('pyfb_rating/customerrcallocation/update/<int:pk>/', views.CustomerRcAllocationUpdateView.as_view(), name='pyfb_rating_customerrcallocation_update'),
)

urlpatterns += (
    # urls for CallerNumList
    path('rate/callernumlist/', views.CallerNumListListView.as_view(), name='pyfb_rating_callernumlist_list'),
    path('rate/callernumlist/create/', views.CallerNumListCreateView.as_view(), name='pyfb_rating_callernumlist_create'),
    path('rate/callernumlist/detail/<slug:slug>/', views.CallerNumListDetailView.as_view(), name='pyfb_rating_callernumlist_detail'),
    path('rate/callernumlist/update/<slug:slug>/', views.CallerNumListUpdateView.as_view(), name='pyfb_rating_callernumlist_update'),
)

urlpatterns += (
    # urls for ProviderRatecard
    path('rate/providerratecard/', views.ProviderRatecardListView.as_view(), name='pyfb_rating_providerratecard_list'),
    path('rate/providerratecard/create/', views.ProviderRatecardCreateView.as_view(), name='pyfb_rating_providerratecard_create'),
    path('rate/providerratecard/detail/<slug:slug>/', views.ProviderRatecardDetailView.as_view(), name='pyfb_rating_providerratecard_detail'),
    path('rate/providerratecard/update/<slug:slug>/', views.ProviderRatecardUpdateView.as_view(), name='pyfb_rating_providerratecard_update'),
)

urlpatterns += (
    # urls for CustomerRatecard
    path('rate/customerratecard/', views.CustomerRatecardListView.as_view(), name='pyfb_rating_customerratecard_list'),
    path('rate/customerratecard/create/', views.CustomerRatecardCreateView.as_view(), name='pyfb_rating_customerratecard_create'),
    path('rate/customerratecard/detail/<slug:slug>/', views.CustomerRatecardDetailView.as_view(), name='pyfb_rating_customerratecard_detail'),
    path('rate/customerratecard/update/<slug:slug>/', views.CustomerRatecardUpdateView.as_view(), name='pyfb_rating_customerratecard_update'),
)

urlpatterns += (
    # urls for CustomerPrefixRate
    path('rate/customerprefixrate/', views.CustomerPrefixRateListView.as_view(), name='pyfb_rating_customerprefixrate_list'),
    path('rate/customerprefixrate/create/', views.CustomerPrefixRateCreateView.as_view(), name='pyfb_rating_customerprefixrate_create'),
    path('rate/customerprefixrate/detail/<int:pk>/', views.CustomerPrefixRateDetailView.as_view(), name='pyfb_rating_customerprefixrate_detail'),
    path('rate/customerprefixrate/update/<int:pk>/', views.CustomerPrefixRateUpdateView.as_view(), name='pyfb_rating_customerprefixrate_update'),
)

urlpatterns += (
    # urls for ProviderPrefixRate
    path('rate/providerprefixrate/', views.ProviderPrefixRateListView.as_view(), name='pyfb_rating_providerprefixrate_list'),
    path('rate/providerprefixrate/create/', views.ProviderPrefixRateCreateView.as_view(), name='pyfb_rating_providerprefixrate_create'),
    path('rate/providerprefixrate/detail/<int:pk>/', views.ProviderPrefixRateDetailView.as_view(), name='pyfb_rating_providerprefixrate_detail'),
    path('rate/providerprefixrate/update/<int:pk>/', views.ProviderPrefixRateUpdateView.as_view(), name='pyfb_rating_providerprefixrate_update'),
)

urlpatterns += (
    # urls for CustomerDestinationRate
    path('rate/customerdestinationrate/', views.CustomerDestinationRateListView.as_view(), name='pyfb_rating_customerdestinationrate_list'),
    path('rate/customerdestinationrate/create/', views.CustomerDestinationRateCreateView.as_view(), name='pyfb_rating_customerdestinationrate_create'),
    path('rate/customerdestinationrate/detail/<int:pk>/', views.CustomerDestinationRateDetailView.as_view(), name='pyfb_rating_customerdestinationrate_detail'),
    path('rate/customerdestinationrate/update/<int:pk>/', views.CustomerDestinationRateUpdateView.as_view(), name='pyfb_rating_customerdestinationrate_update'),
)

urlpatterns += (
    # urls for ProviderDestinationRate
    path('rate/providerdestinationrate/', views.ProviderDestinationRateListView.as_view(), name='pyfb_rating_providerdestinationrate_list'),
    path('rate/providerdestinationrate/create/', views.ProviderDestinationRateCreateView.as_view(), name='pyfb_rating_providerdestinationrate_create'),
    path('rate/providerdestinationrate/detail/<int:pk>/', views.ProviderDestinationRateDetailView.as_view(), name='pyfb_rating_providerdestinationrate_detail'),
    path('rate/providerdestinationrate/update/<int:pk>/', views.ProviderDestinationRateUpdateView.as_view(), name='pyfb_rating_providerdestinationrate_update'),
)

urlpatterns += (
    # urls for CustomerCountryTypeRate
    path('rate/customercountrytyperate/', views.CustomerCountryTypeRateListView.as_view(), name='pyfb_rating_customercountrytyperate_list'),
    path('rate/customercountrytyperate/create/', views.CustomerCountryTypeRateCreateView.as_view(), name='pyfb_rating_customercountrytyperate_create'),
    path('rate/customercountrytyperate/detail/<int:pk>/', views.CustomerCountryTypeRateDetailView.as_view(), name='pyfb_rating_customercountrytyperate_detail'),
    path('rate/customercountrytyperate/update/<int:pk>/', views.CustomerCountryTypeRateUpdateView.as_view(), name='pyfb_rating_customercountrytyperate_update'),
)

urlpatterns += (
    # urls for ProviderCountryTypeRate
    path('rate/providercountrytyperate/', views.ProviderCountryTypeRateListView.as_view(), name='pyfb_rating_providercountrytyperate_list'),
    path('rate/providercountrytyperate/create/', views.ProviderCountryTypeRateCreateView.as_view(), name='pyfb_rating_providercountrytyperate_create'),
    path('rate/providercountrytyperate/detail/<int:pk>/', views.ProviderCountryTypeRateDetailView.as_view(), name='pyfb_rating_providercountrytyperate_detail'),
    path('rate/providercountrytyperate/update/<int:pk>/', views.ProviderCountryTypeRateUpdateView.as_view(), name='pyfb_rating_providercountrytyperate_update'),
)

urlpatterns += (
    # urls for CustomerCountryRate
    path('rate/customercountryrate/', views.CustomerCountryRateListView.as_view(), name='pyfb_rating_customercountryrate_list'),
    path('rate/customercountryrate/create/', views.CustomerCountryRateCreateView.as_view(), name='pyfb_rating_customercountryrate_create'),
    path('rate/customercountryrate/detail/<int:pk>/', views.CustomerCountryRateDetailView.as_view(), name='pyfb_rating_customercountryrate_detail'),
    path('rate/customercountryrate/update/<int:pk>/', views.CustomerCountryRateUpdateView.as_view(), name='pyfb_rating_customercountryrate_update'),
)

urlpatterns += (
    # urls for ProviderCountryRate
    path('rate/providercountryrate/', views.ProviderCountryRateListView.as_view(), name='pyfb_rating_providercountryrate_list'),
    path('rate/providercountryrate/create/', views.ProviderCountryRateCreateView.as_view(), name='pyfb_rating_providercountryrate_create'),
    path('rate/providercountryrate/detail/<int:pk>/', views.ProviderCountryRateDetailView.as_view(), name='pyfb_rating_providercountryrate_detail'),
    path('rate/providercountryrate/update/<int:pk>/', views.ProviderCountryRateUpdateView.as_view(), name='pyfb_rating_providercountryrate_update'),
)

urlpatterns += (
    # urls for CustomerRegionTypeRate
    path('rate/customerregiontyperate/', views.CustomerRegionTypeRateListView.as_view(), name='pyfb_rating_customerregiontyperate_list'),
    path('rate/customerregiontyperate/create/', views.CustomerRegionTypeRateCreateView.as_view(), name='pyfb_rating_customerregiontyperate_create'),
    path('rate/customerregiontyperate/detail/<int:pk>/', views.CustomerRegionTypeRateDetailView.as_view(), name='pyfb_rating_customerregiontyperate_detail'),
    path('rate/customerregiontyperate/update/<int:pk>/', views.CustomerRegionTypeRateUpdateView.as_view(), name='pyfb_rating_customerregiontyperate_update'),
)

urlpatterns += (
    # urls for ProviderRegionTypeRate
    path('rate/providerregiontyperate/', views.ProviderRegionTypeRateListView.as_view(), name='pyfb_rating_providerregiontyperate_list'),
    path('rate/providerregiontyperate/create/', views.ProviderRegionTypeRateCreateView.as_view(), name='pyfb_rating_providerregiontyperate_create'),
    path('rate/providerregiontyperate/detail/<int:pk>/', views.ProviderRegionTypeRateDetailView.as_view(), name='pyfb_rating_providerregiontyperate_detail'),
    path('rate/providerregiontyperate/update/<int:pk>/', views.ProviderRegionTypeRateUpdateView.as_view(), name='pyfb_rating_providerregiontyperate_update'),
)

urlpatterns += (
    # urls for CustomerRegionRate
    path('rate/customerregionrate/', views.CustomerRegionRateListView.as_view(), name='pyfb_rating_customerregionrate_list'),
    path('rate/customerregionrate/create/', views.CustomerRegionRateCreateView.as_view(), name='pyfb_rating_customerregionrate_create'),
    path('rate/customerregionrate/detail/<int:pk>/', views.CustomerRegionRateDetailView.as_view(), name='pyfb_rating_customerregionrate_detail'),
    path('rate/customerregionrate/update/<int:pk>/', views.CustomerRegionRateUpdateView.as_view(), name='pyfb_rating_customerregionrate_update'),
)

urlpatterns += (
    # urls for ProviderRegionRate
    path('rate/providerregionrate/', views.ProviderRegionRateListView.as_view(), name='pyfb_rating_providerregionrate_list'),
    path('rate/providerregionrate/create/', views.ProviderRegionRateCreateView.as_view(), name='pyfb_rating_providerregionrate_create'),
    path('rate/providerregionrate/detail/<int:pk>/', views.ProviderRegionRateDetailView.as_view(), name='pyfb_rating_providerregionrate_detail'),
    path('rate/providerregionrate/update/<int:pk>/', views.ProviderRegionRateUpdateView.as_view(), name='pyfb_rating_providerregionrate_update'),
)

urlpatterns += (
    # urls for CustomerDefaultRate
    path('rate/customerdefaultrate/', views.CustomerDefaultRateListView.as_view(), name='pyfb_rating_customerdefaultrate_list'),
    path('rate/customerdefaultrate/create/', views.CustomerDefaultRateCreateView.as_view(), name='pyfb_rating_customerdefaultrate_create'),
    path('rate/customerdefaultrate/detail/<int:pk>/', views.CustomerDefaultRateDetailView.as_view(), name='pyfb_rating_customerdefaultrate_detail'),
    path('rate/customerdefaultrate/update/<int:pk>/', views.CustomerDefaultRateUpdateView.as_view(), name='pyfb_rating_customerdefaultrate_update'),
)

urlpatterns += (
    # urls for ProviderDefaultRate
    path('rate/providerdefaultrate/', views.ProviderDefaultRateListView.as_view(), name='pyfb_rating_providerdefaultrate_list'),
    path('rate/providerdefaultrate/create/', views.ProviderDefaultRateCreateView.as_view(), name='pyfb_rating_providerdefaultrate_create'),
    path('rate/providerdefaultrate/detail/<int:pk>/', views.ProviderDefaultRateDetailView.as_view(), name='pyfb_rating_providerdefaultrate_detail'),
    path('rate/providerdefaultrate/update/<int:pk>/', views.ProviderDefaultRateUpdateView.as_view(), name='pyfb_rating_providerdefaultrate_update'),
)

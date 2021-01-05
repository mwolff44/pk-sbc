# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb_routing'

router = routers.DefaultRouter()
router.register(r'customerroutinggroup', api.CustomerRoutingGroupViewSet)
router.register(r'routinggroup', api.RoutingGroupViewSet)
router.register(r'prefixrule', api.PrefixRuleViewSet)
router.register(r'destinationrule', api.DestinationRuleViewSet)
router.register(r'countrytyperule', api.CountryTypeRuleViewSet)
router.register(r'countryrule', api.CountryRuleViewSet)
router.register(r'regiontyperule', api.RegionTypeRuleViewSet)
router.register(r'regionrule', api.RegionRuleViewSet)
router.register(r'defaultrule', api.DefaultRuleViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for CustomerRoutingGroup
    path('pyfb_routing/customerroutinggroup/', views.CustomerRoutingGroupListView.as_view(), name='pyfb_routing_customerroutinggroup_list'),
    path('pyfb_routing/customerroutinggroup/create/', views.CustomerRoutingGroupCreateView.as_view(), name='pyfb_routing_customerroutinggroup_create'),
    path('pyfb_routing/customerroutinggroup/detail/<int:pk>/', views.CustomerRoutingGroupDetailView.as_view(), name='pyfb_routing_customerroutinggroup_detail'),
    path('pyfb_routing/customerroutinggroup/update/<int:pk>/', views.CustomerRoutingGroupUpdateView.as_view(), name='pyfb_routing_customerroutinggroup_update'),
)

urlpatterns += (
    # urls for RoutingGroup
    path('pyfb_routing/routinggroup/', views.RoutingGroupListView.as_view(), name='pyfb_routing_routinggroup_list'),
    path('pyfb_routing/routinggroup/create/', views.RoutingGroupCreateView.as_view(), name='pyfb_routing_routinggroup_create'),
    path('pyfb_routing/routinggroup/detail/<slug:slug>/', views.RoutingGroupDetailView.as_view(), name='pyfb_routing_routinggroup_detail'),
    path('pyfb_routing/routinggroup/update/<slug:slug>/', views.RoutingGroupUpdateView.as_view(), name='pyfb_routing_routinggroup_update'),
)

urlpatterns += (
    # urls for PrefixRule
    path('pyfb_routing/prefixrule/', views.PrefixRuleListView.as_view(), name='pyfb_routing_prefixrule_list'),
    path('pyfb_routing/prefixrule/create/', views.PrefixRuleCreateView.as_view(), name='pyfb_routing_prefixrule_create'),
    path('pyfb_routing/prefixrule/detail/<int:pk>/', views.PrefixRuleDetailView.as_view(), name='pyfb_routing_prefixrule_detail'),
    path('pyfb_routing/prefixrule/update/<int:pk>/', views.PrefixRuleUpdateView.as_view(), name='pyfb_routing_prefixrule_update'),
)

urlpatterns += (
    # urls for DestinationRule
    path('pyfb_routing/destinationrule/', views.DestinationRuleListView.as_view(), name='pyfb_routing_destinationrule_list'),
    path('pyfb_routing/destinationrule/create/', views.DestinationRuleCreateView.as_view(), name='pyfb_routing_destinationrule_create'),
    path('pyfb_routing/destinationrule/detail/<int:pk>/', views.DestinationRuleDetailView.as_view(), name='pyfb_routing_destinationrule_detail'),
    path('pyfb_routing/destinationrule/update/<int:pk>/', views.DestinationRuleUpdateView.as_view(), name='pyfb_routing_destinationrule_update'),
)

urlpatterns += (
    # urls for CountryTypeRule
    path('pyfb_routing/countrytyperule/', views.CountryTypeRuleListView.as_view(), name='pyfb_routing_countrytyperule_list'),
    path('pyfb_routing/countrytyperule/create/', views.CountryTypeRuleCreateView.as_view(), name='pyfb_routing_countrytyperule_create'),
    path('pyfb_routing/countrytyperule/detail/<int:pk>/', views.CountryTypeRuleDetailView.as_view(), name='pyfb_routing_countrytyperule_detail'),
    path('pyfb_routing/countrytyperule/update/<int:pk>/', views.CountryTypeRuleUpdateView.as_view(), name='pyfb_routing_countrytyperule_update'),
)

urlpatterns += (
    # urls for CountryRule
    path('pyfb_routing/countryrule/', views.CountryRuleListView.as_view(), name='pyfb_routing_countryrule_list'),
    path('pyfb_routing/countryrule/create/', views.CountryRuleCreateView.as_view(), name='pyfb_routing_countryrule_create'),
    path('pyfb_routing/countryrule/detail/<int:pk>/', views.CountryRuleDetailView.as_view(), name='pyfb_routing_countryrule_detail'),
    path('pyfb_routing/countryrule/update/<int:pk>/', views.CountryRuleUpdateView.as_view(), name='pyfb_routing_countryrule_update'),
)

urlpatterns += (
    # urls for RegionTypeRule
    path('pyfb_routing/regiontyperule/', views.RegionTypeRuleListView.as_view(), name='pyfb_routing_regiontyperule_list'),
    path('pyfb_routing/regiontyperule/create/', views.RegionTypeRuleCreateView.as_view(), name='pyfb_routing_regiontyperule_create'),
    path('pyfb_routing/regiontyperule/detail/<int:pk>/', views.RegionTypeRuleDetailView.as_view(), name='pyfb_routing_regiontyperule_detail'),
    path('pyfb_routing/regiontyperule/update/<int:pk>/', views.RegionTypeRuleUpdateView.as_view(), name='pyfb_routing_regiontyperule_update'),
)

urlpatterns += (
    # urls for RegionRule
    path('pyfb_routing/regionrule/', views.RegionRuleListView.as_view(), name='pyfb_routing_regionrule_list'),
    path('pyfb_routing/regionrule/create/', views.RegionRuleCreateView.as_view(), name='pyfb_routing_regionrule_create'),
    path('pyfb_routing/regionrule/detail/<int:pk>/', views.RegionRuleDetailView.as_view(), name='pyfb_routing_regionrule_detail'),
    path('pyfb_routing/regionrule/update/<int:pk>/', views.RegionRuleUpdateView.as_view(), name='pyfb_routing_regionrule_update'),
)

urlpatterns += (
    # urls for DefaultRule
    path('pyfb_routing/defaultrule/', views.DefaultRuleListView.as_view(), name='pyfb_routing_defaultrule_list'),
    path('pyfb_routing/defaultrule/create/', views.DefaultRuleCreateView.as_view(), name='pyfb_routing_defaultrule_create'),
    path('pyfb_routing/defaultrule/detail/<int:pk>/', views.DefaultRuleDetailView.as_view(), name='pyfb_routing_defaultrule_detail'),
    path('pyfb_routing/defaultrule/update/<int:pk>/', views.DefaultRuleUpdateView.as_view(), name='pyfb_routing_defaultrule_update'),
)

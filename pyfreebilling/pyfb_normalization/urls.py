# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


app_name = 'pyfb_normalization'

router = routers.DefaultRouter()
router.register(r'callmappingrule', api.CallMappingRuleViewSet)
router.register(r'normalizationgrp', api.NormalizationGrpViewSet)
router.register(r'normalizationrule', api.NormalizationRuleViewSet)
router.register(r'normalizationrulegrp', api.NormalizationRuleGrpViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for CallMappingRule
    path('pyfb_normalization/callmappingrule/', views.CallMappingRuleListView.as_view(), name='pyfb_normalization_callmappingrule_list'),
    path('pyfb_normalization/callmappingrule/create/', views.CallMappingRuleCreateView.as_view(), name='pyfb_normalization_callmappingrule_create'),
    path('pyfb_normalization/callmappingrule/detail/<int:pk>/', views.CallMappingRuleDetailView.as_view(), name='pyfb_normalization_callmappingrule_detail'),
    path('pyfb_normalization/callmappingrule/update/<int:pk>/', views.CallMappingRuleUpdateView.as_view(), name='pyfb_normalization_callmappingrule_update'),
)

urlpatterns += (
    # urls for NormalizationGrp
    path('pyfb_normalization/normalizationgrp/', views.NormalizationGrpListView.as_view(), name='pyfb_normalization_normalizationgrp_list'),
    path('pyfb_normalization/normalizationgrp/create/', views.NormalizationGrpCreateView.as_view(), name='pyfb_normalization_normalizationgrp_create'),
    path('pyfb_normalization/normalizationgrp/detail/<int:pk>/', views.NormalizationGrpDetailView.as_view(), name='pyfb_normalization_normalizationgrp_detail'),
    path('pyfb_normalization/normalizationgrp/update/<int:pk>/', views.NormalizationGrpUpdateView.as_view(), name='pyfb_normalization_normalizationgrp_update'),
)

urlpatterns += (
    # urls for NormalizationRule
    path('pyfb_normalization/normalizationrule/', views.NormalizationRuleListView.as_view(), name='pyfb_normalization_normalizationrule_list'),
    path('pyfb_normalization/normalizationrule/create/', views.NormalizationRuleCreateView.as_view(), name='pyfb_normalization_normalizationrule_create'),
    path('pyfb_normalization/normalizationrule/detail/<int:pk>/', views.NormalizationRuleDetailView.as_view(), name='pyfb_normalization_normalizationrule_detail'),
    path('pyfb_normalization/normalizationrule/update/<int:pk>/', views.NormalizationRuleUpdateView.as_view(), name='pyfb_normalization_normalizationrule_update'),
)

urlpatterns += (
    # urls for NormalizationRuleGrp
    path('pyfb_normalization/normalizationrulegrp/', views.NormalizationRuleGrpListView.as_view(), name='pyfb_normalization_normalizationrulegrp_list'),
    path('pyfb_normalization/normalizationrulegrp/create/', views.NormalizationRuleGrpCreateView.as_view(), name='pyfb_normalization_normalizationrulegrp_create'),
    path('pyfb_normalization/normalizationrulegrp/detail/<int:pk>/', views.NormalizationRuleGrpDetailView.as_view(), name='pyfb_normalization_normalizationrulegrp_detail'),
    path('pyfb_normalization/normalizationrulegrp/update/<int:pk>/', views.NormalizationRuleGrpUpdateView.as_view(), name='pyfb_normalization_normalizationrulegrp_update'),
)

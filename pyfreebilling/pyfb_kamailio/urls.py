# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

app_name = 'pyfb_kamailio'

router = routers.DefaultRouter()
router.register(r'dialog', api.DialogViewSet)
router.register(r'dialogvar', api.DialogVarViewSet)
router.register(r'acc', api.AccViewSet)
router.register(r'acccdr', api.AccCdrViewSet)
router.register(r'missedcall', api.MissedCallViewSet)
router.register(r'uacreg', api.UacRegViewSet)
router.register(r'trusted', api.TrustedViewSet)
router.register(r'version', api.VersionViewSet)
router.register(r'location', api.LocationViewSet)
router.register(r'locationattrs', api.LocationAttrsViewSet)
router.register(r'userblacklist', api.UserBlackListViewSet)
router.register(r'globalblacklist', api.GlobalBlackListViewSet)
router.register(r'speeddial', api.SpeedDialViewSet)
router.register(r'pipelimit', api.PipeLimitViewSet)
router.register(r'mtree', api.MtreeViewSet)
router.register(r'mtrees', api.MtreesViewSet)
router.register(r'htable', api.HtableViewSet)
router.register(r'rtpengine', api.RtpEngineViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    path('api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Dialog
    path('pyfb_kamailio/dialog/', views.DialogListView.as_view(), name='pyfb_kamailio_dialog_list'),
    path('pyfb_kamailio/dialog/create/', views.DialogCreateView.as_view(), name='pyfb_kamailio_dialog_create'),
    path('pyfb_kamailio/dialog/detail/<int:pk>/', views.DialogDetailView.as_view(), name='pyfb_kamailio_dialog_detail'),
    path('pyfb_kamailio/dialog/update/<int:pk>/', views.DialogUpdateView.as_view(), name='pyfb_kamailio_dialog_update'),
)

urlpatterns += (
    # urls for DialogVar
    path('pyfb_kamailio/dialogvar/', views.DialogVarListView.as_view(), name='pyfb_kamailio_dialogvar_list'),
    path('pyfb_kamailio/dialogvar/create/', views.DialogVarCreateView.as_view(), name='pyfb_kamailio_dialogvar_create'),
    path('pyfb_kamailio/dialogvar/detail/<int:pk>/', views.DialogVarDetailView.as_view(), name='pyfb_kamailio_dialogvar_detail'),
    path('pyfb_kamailio/dialogvar/update/<int:pk>/', views.DialogVarUpdateView.as_view(), name='pyfb_kamailio_dialogvar_update'),
)

urlpatterns += (
    # urls for Acc
    path('pyfb_kamailio/acc/', views.AccListView.as_view(), name='pyfb_kamailio_acc_list'),
    path('pyfb_kamailio/acc/create/', views.AccCreateView.as_view(), name='pyfb_kamailio_acc_create'),
    path('pyfb_kamailio/acc/detail/<int:pk>/', views.AccDetailView.as_view(), name='pyfb_kamailio_acc_detail'),
    path('pyfb_kamailio/acc/update/<int:pk>/', views.AccUpdateView.as_view(), name='pyfb_kamailio_acc_update'),
)

urlpatterns += (
    # urls for AccCdr
    path('pyfb_kamailio/acccdr/', views.AccCdrListView.as_view(), name='pyfb_kamailio_acccdr_list'),
    path('pyfb_kamailio/acccdr/create/', views.AccCdrCreateView.as_view(), name='pyfb_kamailio_acccdr_create'),
    path('pyfb_kamailio/acccdr/detail/<int:pk>/', views.AccCdrDetailView.as_view(), name='pyfb_kamailio_acccdr_detail'),
    path('pyfb_kamailio/acccdr/update/<int:pk>/', views.AccCdrUpdateView.as_view(), name='pyfb_kamailio_acccdr_update'),
)

urlpatterns += (
    # urls for MissedCall
    path('pyfb_kamailio/missedcall/', views.MissedCallListView.as_view(), name='pyfb_kamailio_missedcall_list'),
    path('pyfb_kamailio/missedcall/create/', views.MissedCallCreateView.as_view(), name='pyfb_kamailio_missedcall_create'),
    path('pyfb_kamailio/missedcall/detail/<int:pk>/', views.MissedCallDetailView.as_view(), name='pyfb_kamailio_missedcall_detail'),
    path('pyfb_kamailio/missedcall/update/<int:pk>/', views.MissedCallUpdateView.as_view(), name='pyfb_kamailio_missedcall_update'),
)

urlpatterns += (
    # urls for UacReg
    path('pyfb_kamailio/uacreg/', views.UacRegListView.as_view(), name='pyfb_kamailio_uacreg_list'),
    path('pyfb_kamailio/uacreg/create/', views.UacRegCreateView.as_view(), name='pyfb_kamailio_uacreg_create'),
    path('pyfb_kamailio/uacreg/detail/<int:pk>/', views.UacRegDetailView.as_view(), name='pyfb_kamailio_uacreg_detail'),
    path('pyfb_kamailio/uacreg/update/<int:pk>/', views.UacRegUpdateView.as_view(), name='pyfb_kamailio_uacreg_update'),
)

urlpatterns += (
    # urls for Trusted
    path('pyfb_kamailio/trusted/', views.TrustedListView.as_view(), name='pyfb_kamailio_trusted_list'),
    path('pyfb_kamailio/trusted/create/', views.TrustedCreateView.as_view(), name='pyfb_kamailio_trusted_create'),
    path('pyfb_kamailio/trusted/detail/<int:pk>/', views.TrustedDetailView.as_view(), name='pyfb_kamailio_trusted_detail'),
    path('pyfb_kamailio/trusted/update/<int:pk>/', views.TrustedUpdateView.as_view(), name='pyfb_kamailio_trusted_update'),
)

urlpatterns += (
    # urls for Version
    path('pyfb_kamailio/version/', views.VersionListView.as_view(), name='pyfb_kamailio_version_list'),
    path('pyfb_kamailio/version/create/', views.VersionCreateView.as_view(), name='pyfb_kamailio_version_create'),
    path('pyfb_kamailio/version/detail/<int:pk>/', views.VersionDetailView.as_view(), name='pyfb_kamailio_version_detail'),
    path('pyfb_kamailio/version/update/<int:pk>/', views.VersionUpdateView.as_view(), name='pyfb_kamailio_version_update'),
)

urlpatterns += (
    # urls for Location
    path('pyfb_kamailio/location/', views.LocationListView.as_view(), name='pyfb_kamailio_location_list'),
    path('pyfb_kamailio/location/create/', views.LocationCreateView.as_view(), name='pyfb_kamailio_location_create'),
    path('pyfb_kamailio/location/detail/<int:pk>/', views.LocationDetailView.as_view(), name='pyfb_kamailio_location_detail'),
    path('pyfb_kamailio/location/update/<int:pk>/', views.LocationUpdateView.as_view(), name='pyfb_kamailio_location_update'),
)

urlpatterns += (
    # urls for LocationAttrs
    path('pyfb_kamailio/locationattrs/', views.LocationAttrsListView.as_view(), name='pyfb_kamailio_locationattrs_list'),
    path('pyfb_kamailio/locationattrs/create/', views.LocationAttrsCreateView.as_view(), name='pyfb_kamailio_locationattrs_create'),
    path('pyfb_kamailio/locationattrs/detail/<int:pk>/', views.LocationAttrsDetailView.as_view(), name='pyfb_kamailio_locationattrs_detail'),
    path('pyfb_kamailio/locationattrs/update/<int:pk>/', views.LocationAttrsUpdateView.as_view(), name='pyfb_kamailio_locationattrs_update'),
)

urlpatterns += (
    # urls for UserBlackList
    path('pyfb_kamailio/userblacklist/', views.UserBlackListListView.as_view(), name='pyfb_kamailio_userblacklist_list'),
    path('pyfb_kamailio/userblacklist/create/', views.UserBlackListCreateView.as_view(), name='pyfb_kamailio_userblacklist_create'),
    path('pyfb_kamailio/userblacklist/detail/<int:pk>/', views.UserBlackListDetailView.as_view(), name='pyfb_kamailio_userblacklist_detail'),
    path('pyfb_kamailio/userblacklist/update/<int:pk>/', views.UserBlackListUpdateView.as_view(), name='pyfb_kamailio_userblacklist_update'),
)

urlpatterns += (
    # urls for GlobalBlackList
    path('pyfb_kamailio/globalblacklist/', views.GlobalBlackListListView.as_view(), name='pyfb_kamailio_globalblacklist_list'),
    path('pyfb_kamailio/globalblacklist/create/', views.GlobalBlackListCreateView.as_view(), name='pyfb_kamailio_globalblacklist_create'),
    path('pyfb_kamailio/globalblacklist/detail/<int:pk>/', views.GlobalBlackListDetailView.as_view(), name='pyfb_kamailio_globalblacklist_detail'),
    path('pyfb_kamailio/globalblacklist/update/<int:pk>/', views.GlobalBlackListUpdateView.as_view(), name='pyfb_kamailio_globalblacklist_update'),
)

urlpatterns += (
    # urls for SpeedDial
    path('pyfb_kamailio/speeddial/', views.SpeedDialListView.as_view(), name='pyfb_kamailio_speeddial_list'),
    path('pyfb_kamailio/speeddial/create/', views.SpeedDialCreateView.as_view(), name='pyfb_kamailio_speeddial_create'),
    path('pyfb_kamailio/speeddial/detail/<int:pk>/', views.SpeedDialDetailView.as_view(), name='pyfb_kamailio_speeddial_detail'),
    path('pyfb_kamailio/speeddial/update/<int:pk>/', views.SpeedDialUpdateView.as_view(), name='pyfb_kamailio_speeddial_update'),
)

urlpatterns += (
    # urls for PipeLimit
    path('pyfb_kamailio/pipelimit/', views.PipeLimitListView.as_view(), name='pyfb_kamailio_pipelimit_list'),
    path('pyfb_kamailio/pipelimit/create/', views.PipeLimitCreateView.as_view(), name='pyfb_kamailio_pipelimit_create'),
    path('pyfb_kamailio/pipelimit/detail/<int:pk>/', views.PipeLimitDetailView.as_view(), name='pyfb_kamailio_pipelimit_detail'),
    path('pyfb_kamailio/pipelimit/update/<int:pk>/', views.PipeLimitUpdateView.as_view(), name='pyfb_kamailio_pipelimit_update'),
)

urlpatterns += (
    # urls for Mtree
    path('pyfb_kamailio/mtree/', views.MtreeListView.as_view(), name='pyfb_kamailio_mtree_list'),
    path('pyfb_kamailio/mtree/create/', views.MtreeCreateView.as_view(), name='pyfb_kamailio_mtree_create'),
    path('pyfb_kamailio/mtree/detail/<int:pk>/', views.MtreeDetailView.as_view(), name='pyfb_kamailio_mtree_detail'),
    path('pyfb_kamailio/mtree/update/<int:pk>/', views.MtreeUpdateView.as_view(), name='pyfb_kamailio_mtree_update'),
)

urlpatterns += (
    # urls for Mtrees
    path('pyfb_kamailio/mtrees/', views.MtreesListView.as_view(), name='pyfb_kamailio_mtrees_list'),
    path('pyfb_kamailio/mtrees/create/', views.MtreesCreateView.as_view(), name='pyfb_kamailio_mtrees_create'),
    path('pyfb_kamailio/mtrees/detail/<int:pk>/', views.MtreesDetailView.as_view(), name='pyfb_kamailio_mtrees_detail'),
    path('pyfb_kamailio/mtrees/update/<int:pk>/', views.MtreesUpdateView.as_view(), name='pyfb_kamailio_mtrees_update'),
)

urlpatterns += (
    # urls for Htable
    path('pyfb_kamailio/htable/', views.HtableListView.as_view(), name='pyfb_kamailio_htable_list'),
    path('pyfb_kamailio/htable/create/', views.HtableCreateView.as_view(), name='pyfb_kamailio_htable_create'),
    path('pyfb_kamailio/htable/detail/<int:pk>/', views.HtableDetailView.as_view(), name='pyfb_kamailio_htable_detail'),
    path('pyfb_kamailio/htable/update/<int:pk>/', views.HtableUpdateView.as_view(), name='pyfb_kamailio_htable_update'),
)

urlpatterns += (
    # urls for RtpEngine
    path('pyfb_kamailio/rtpengine/', views.RtpEngineListView.as_view(), name='pyfb_kamailio_rtpengine_list'),
    path('pyfb_kamailio/rtpengine/create/', views.RtpEngineCreateView.as_view(), name='pyfb_kamailio_rtpengine_create'),
    path('pyfb_kamailio/rtpengine/detail/<int:pk>/', views.RtpEngineDetailView.as_view(), name='pyfb_kamailio_rtpengine_detail'),
    path('pyfb_kamailio/rtpengine/update/<int:pk>/', views.RtpEngineUpdateView.as_view(), name='pyfb_kamailio_rtpengine_update'),
)

urlpatterns += (
    # urls for Statistic
    path('pyfb_kamailio/statistic/', views.StatisticListView.as_view(), name='pyfb_kamailio_statistic_list'),
    path('pyfb_kamailio/statistic/create/', views.StatisticCreateView.as_view(), name='pyfb_kamailio_statistic_create'),
    path('pyfb_kamailio/statistic/detail/<int:pk>/', views.StatisticDetailView.as_view(), name='pyfb_kamailio_statistic_detail'),
    path('pyfb_kamailio/statistic/update/<int:pk>/', views.StatisticUpdateView.as_view(), name='pyfb_kamailio_statistic_update'),
)

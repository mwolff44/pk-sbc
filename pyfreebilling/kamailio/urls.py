from django.conf.urls import url, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
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


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Version
    url(r'^kamailio/version/$', views.VersionListView.as_view(), name='kamailio_version_list'),
    url(r'^kamailio/version/create/$', views.VersionCreateView.as_view(), name='kamailio_version_create'),
    url(r'^kamailio/version/detail/(?P<pk>\S+)/$', views.VersionDetailView.as_view(), name='kamailio_version_detail'),
    url(r'^kamailio/version/update/(?P<pk>\S+)/$', views.VersionUpdateView.as_view(), name='kamailio_version_update'),
)

urlpatterns += (
    # urls for Location
    url(r'^kamailio/location/$', views.LocationListView.as_view(), name='kamailio_location_list'),
    url(r'^kamailio/location/create/$', views.LocationCreateView.as_view(), name='kamailio_location_create'),
    url(r'^kamailio/location/detail/(?P<pk>\S+)/$', views.LocationDetailView.as_view(), name='kamailio_location_detail'),
    url(r'^kamailio/location/update/(?P<pk>\S+)/$', views.LocationUpdateView.as_view(), name='kamailio_location_update'),
)

urlpatterns += (
    # urls for LocationAttrs
    url(r'^kamailio/locationattrs/$', views.LocationAttrsListView.as_view(), name='kamailio_locationattrs_list'),
    url(r'^kamailio/locationattrs/create/$', views.LocationAttrsCreateView.as_view(), name='kamailio_locationattrs_create'),
    url(r'^kamailio/locationattrs/detail/(?P<pk>\S+)/$', views.LocationAttrsDetailView.as_view(), name='kamailio_locationattrs_detail'),
    url(r'^kamailio/locationattrs/update/(?P<pk>\S+)/$', views.LocationAttrsUpdateView.as_view(), name='kamailio_locationattrs_update'),
)

urlpatterns += (
    # urls for UserBlackList
    url(r'^kamailio/userblacklist/$', views.UserBlackListListView.as_view(), name='kamailio_userblacklist_list'),
    url(r'^kamailio/userblacklist/create/$', views.UserBlackListCreateView.as_view(), name='kamailio_userblacklist_create'),
    url(r'^kamailio/userblacklist/detail/(?P<pk>\S+)/$', views.UserBlackListDetailView.as_view(), name='kamailio_userblacklist_detail'),
    url(r'^kamailio/userblacklist/update/(?P<pk>\S+)/$', views.UserBlackListUpdateView.as_view(), name='kamailio_userblacklist_update'),
)

urlpatterns += (
    # urls for GlobalBlackList
    url(r'^kamailio/globalblacklist/$', views.GlobalBlackListListView.as_view(), name='kamailio_globalblacklist_list'),
    url(r'^kamailio/globalblacklist/create/$', views.GlobalBlackListCreateView.as_view(), name='kamailio_globalblacklist_create'),
    url(r'^kamailio/globalblacklist/detail/(?P<pk>\S+)/$', views.GlobalBlackListDetailView.as_view(), name='kamailio_globalblacklist_detail'),
    url(r'^kamailio/globalblacklist/update/(?P<pk>\S+)/$', views.GlobalBlackListUpdateView.as_view(), name='kamailio_globalblacklist_update'),
)

urlpatterns += (
    # urls for SpeedDial
    url(r'^kamailio/speeddial/$', views.SpeedDialListView.as_view(), name='kamailio_speeddial_list'),
    url(r'^kamailio/speeddial/create/$', views.SpeedDialCreateView.as_view(), name='kamailio_speeddial_create'),
    url(r'^kamailio/speeddial/detail/(?P<pk>\S+)/$', views.SpeedDialDetailView.as_view(), name='kamailio_speeddial_detail'),
    url(r'^kamailio/speeddial/update/(?P<pk>\S+)/$', views.SpeedDialUpdateView.as_view(), name='kamailio_speeddial_update'),
)

urlpatterns += (
    # urls for PipeLimit
    url(r'^kamailio/pipelimit/$', views.PipeLimitListView.as_view(), name='kamailio_pipelimit_list'),
    url(r'^kamailio/pipelimit/create/$', views.PipeLimitCreateView.as_view(), name='kamailio_pipelimit_create'),
    url(r'^kamailio/pipelimit/detail/(?P<pk>\S+)/$', views.PipeLimitDetailView.as_view(), name='kamailio_pipelimit_detail'),
    url(r'^kamailio/pipelimit/update/(?P<pk>\S+)/$', views.PipeLimitUpdateView.as_view(), name='kamailio_pipelimit_update'),
)

urlpatterns += (
    # urls for Mtree
    url(r'^kamailio/mtree/$', views.MtreeListView.as_view(), name='kamailio_mtree_list'),
    url(r'^kamailio/mtree/create/$', views.MtreeCreateView.as_view(), name='kamailio_mtree_create'),
    url(r'^kamailio/mtree/detail/(?P<pk>\S+)/$', views.MtreeDetailView.as_view(), name='kamailio_mtree_detail'),
    url(r'^kamailio/mtree/update/(?P<pk>\S+)/$', views.MtreeUpdateView.as_view(), name='kamailio_mtree_update'),
)

urlpatterns += (
    # urls for Mtrees
    url(r'^kamailio/mtrees/$', views.MtreesListView.as_view(), name='kamailio_mtrees_list'),
    url(r'^kamailio/mtrees/create/$', views.MtreesCreateView.as_view(), name='kamailio_mtrees_create'),
    url(r'^kamailio/mtrees/detail/(?P<pk>\S+)/$', views.MtreesDetailView.as_view(), name='kamailio_mtrees_detail'),
    url(r'^kamailio/mtrees/update/(?P<pk>\S+)/$', views.MtreesUpdateView.as_view(), name='kamailio_mtrees_update'),
)

urlpatterns += (
    # urls for Htable
    url(r'^kamailio/htable/$', views.HtableListView.as_view(), name='kamailio_htable_list'),
    url(r'^kamailio/htable/create/$', views.HtableCreateView.as_view(), name='kamailio_htable_create'),
    url(r'^kamailio/htable/detail/(?P<pk>\S+)/$', views.HtableDetailView.as_view(), name='kamailio_htable_detail'),
    url(r'^kamailio/htable/update/(?P<pk>\S+)/$', views.HtableUpdateView.as_view(), name='kamailio_htable_update'),
)


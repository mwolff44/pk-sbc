from django.conf.urls import url, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register(r'dialog', api.DialogViewSet)
router.register(r'dialogvar', api.DialogVarViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
)

urlpatterns += (
    # urls for Dialog
    url(r'^sipdialog/dialog/$', views.DialogListView.as_view(), name='sipdialog_dialog_list'),
    url(r'^sipdialog/dialog/create/$', views.DialogCreateView.as_view(), name='sipdialog_dialog_create'),
    url(r'^sipdialog/dialog/detail/(?P<pk>\S+)/$', views.DialogDetailView.as_view(), name='sipdialog_dialog_detail'),
    url(r'^sipdialog/dialog/update/(?P<pk>\S+)/$', views.DialogUpdateView.as_view(), name='sipdialog_dialog_update'),
)

urlpatterns += (
    # urls for DialogVar
    url(r'^sipdialog/dialogvar/$', views.DialogVarListView.as_view(), name='sipdialog_dialogvar_list'),
    url(r'^sipdialog/dialogvar/create/$', views.DialogVarCreateView.as_view(), name='sipdialog_dialogvar_create'),
    url(r'^sipdialog/dialogvar/detail/(?P<pk>\S+)/$', views.DialogVarDetailView.as_view(), name='sipdialog_dialogvar_detail'),
    url(r'^sipdialog/dialogvar/update/(?P<pk>\S+)/$', views.DialogVarUpdateView.as_view(), name='sipdialog_dialogvar_update'),
)


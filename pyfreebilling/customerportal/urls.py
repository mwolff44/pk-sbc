# -*- coding: utf-8 -*-
# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.HomePageCustView.as_view(),
        name='home'
    ),
    url(
        regex=r'^sip_account/$',
        view=views.SipAccountCustView.as_view(),
        name='sip_account'
    ),
    # url(
    #     regex=r'^sip_account/add$',
    #     view=views.SipAccountCustAddView.as_view(),
    #     name='add_sip_account'
    # ),
    # url(
    #     regex=r'^sip_account/dactivate$',
    #     view=views.SipAccountCustDeactivateView.as_view(),
    #     name='deactivate_sip_account'
    # ),
    url(
        regex=r'^balance/$',
        view=views.BalanceHistoryCustView.as_view(),
        name='balance_history'
    ),
    url(
        regex=r'^stats/$',
        view=views.CdrReportCustView.as_view(),
        name='stats'
    ),
    url(
        regex=r'^reports/$',
        view=views.ListExportCustView.as_view(),
        name='list_export'
    ),
    url(
        regex=r'^rates_export/(?P<ratecard>\d+)/$',
        view=views.rates_csv_view,
        name='rates_download'
    ),
    url(
        regex=r'^rates/(?P<ratecard>\d+)/$',
        view=views.RatesFilteredTableView.as_view(),
        name='list_rates'
    ),
    url(
        regex=r'^cdr_export/(?P<month>\d{1})/(?P<day>\d{1})/$',
        view=views.csv_view,
        name='report'
    ),
    url(
        regex=r'^cdr_report/$',
        view=views.CdrReportCustView.as_view(),
        name='cdr_report'
    ),
    url(
        regex=r'^accounts/login/$',
        view=auth_views.login,
        kwargs={'template_name': 'customer/login.html'},
        name='login'
    ),
    url(
        regex=r'^accounts/logout/$',
        view=auth_views.logout_then_login,
        name='logout_then_login'
    ),
    url(
        regex=r'^accounts/profile/$',
        view=views.HomePageCustView.as_view(),
        name='user_profile'
    ),
    url(
        regex=r'^register/$',
        view=views.CreateUserView.as_view(),
        name='create_user'
    ),
]

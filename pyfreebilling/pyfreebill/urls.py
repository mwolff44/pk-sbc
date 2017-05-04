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

from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(
        r'^extranet/', include([
            url(
                regex=r'^report/$',
                view=views.admin_report_view,
                name='status'
            ),
            url(
                regex=r'^cdrform/$',
                view=views.live_report_view,
                name='cdr_report'
            ),
            url(
                regex=r'^status/$',
                view=views.admin_status_view,
                name='version'
            ),
            url(
                regex=r'^list_models/$',
                view=views.admin_listmodels_view
            ),
            url(
                regex=r'^customers_stats/$',
                view=views.customers_stats_view,
                name='customers_stats'
            ),
            url(
                regex=r'^destination_customers_stats/$',
                view=views.destination_customers_stats_view,
                name='dest_customers_stats'
            ),
            url(
                regex=r'^providers_stats/$',
                view=views.providers_stats_view,
                name='providers_stats'
            ),
            url(
                regex=r'^destination_providers_stats/$',
                view=views.destination_providers_stats_view,
                name='dest_providers_stats'
            ),
            url(
                regex=r'^FsDirectoryUpdate/',
                view=views.FsDirectoryUpdateView,
                name='fs_directory_update'
            ),
            url(
                regex=r'^FsSofiaUpdate/',
                view=views.FsSofiaUpdateView,
                name='fs_sofia_update'
            ),
        ])),
    url(
        regex=r'^chart_stats_general_json/$',
        view=views.chart_stats_general_json,
        name='chart_stats_general_json'),
]

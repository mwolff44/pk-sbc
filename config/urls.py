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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
# from django.views.generic.base import TemplateView
from django.views import defaults as default_views
from django.utils.translation import ugettext_lazy as _


admin.autodiscover()


urlpatterns = [
    # PyFreeBilling Admin
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(
        settings.ADMIN_URL,
        include(admin.site.urls)
    ),

    # Honeypot
    url(
        settings.HONEYPOT_URL,
        include('admin_honeypot.urls',
                namespace='admin_honeypot')
    ),

    # user management
    # url(r'^accounts/', include('allauth.urls')),

    # Currencies management
    url(
        r'^currencies/',
        include('currencies.urls')
    ),

    # Pyfreebilling applications
    url(
        r'^',
        include('pyfreebilling.customerportal.urls',
                namespace='customerportal')
    ),
    url(
        r'^',
        include('pyfreebilling.did.urls',
                namespace='did')
    ),
    url(
        r'^',
        include('pyfreebilling.pyfreebill.urls',
                namespace='pyfreebill')
    ),
    url(
        r'^',
        include('pyfreebilling.switch.urls',
                namespace='switch')
    ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$',
            default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

# urlpatterns += patterns(
#     '',
#     url(r'^extranet/report/$',
#         'pyfreebill.views.admin_report_view'),
#     url(r'^extranet/FsServer/$',
#         'switch.views.fs_status_view'),
#     url(r'^extranet/FsServerRegistry/$',
#         'switch.views.fs_registry_view'),
#     url(r'^extranet/FsServerBCalls/$',
#         'switch.views.fs_bcalls_view'),
#     url(r'^extranet/cdrform/$',
#         'pyfreebill.views.live_report_view'),
#     url(r'^extranet/status/$',
#         'pyfreebill.views.admin_status_view'),
#     url(r'^extranet/list_models/$',
#         'pyfreebill.views.admin_listmodels_view'),
#     url(r'^extranet/customers_stats/$',
#         'pyfreebill.views.customers_stats_view',
#         name='customers_stats'),
#     url(r'^extranet/destination_customers_stats/$',
#         'pyfreebill.views.destination_customers_stats_view',
#         name='dest_customers_stats'),
#     url(r'^extranet/providers_stats/$',
#         'pyfreebill.views.providers_stats_view',
#         name='providers_stats'),
#     url(r'^extranet/destination_providers_stats/$',
#         'pyfreebill.views.destination_providers_stats_view',
#         name='dest_providers_stats'),
#     url(r'^extranet/ServerStatus/$',
#         'switch.views.server_status_view'),
#     url(r'^extranet/did/wizard_import/$',
#         'did.views.start_import',),
#     url(r'^i18n/',
#         include('django.conf.urls.i18n')),
#     url(r'^extranet/simple_import/',
#         include('simple_import.urls')),
#     url(r'^extranet/FsDirectoryUpdate/',
#         'pyfreebill.views.FsDirectoryUpdateView',
#         name='fs_directory_update'),
#     url(r'^extranet/FsSofiaUpdate/',
#         'pyfreebill.views.FsSofiaUpdateView',
#         name='fs_sofia_update'),
#     url(regex=r'^chart_stats_general_json/$',
#         view=chart_stats_general_json,
#         name='chart_stats_general_json'),
# )

admin.site.site_header = settings.ADMIN_SITE_NAME
admin.site.site_title = settings.ADMIN_SITE_DESCRIPTION
admin.site.index_title = settings.ADMIN_SITE_TITLE

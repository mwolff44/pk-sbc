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


# # Custom menu
# def perms_func(request, item):
#         if not request.user.is_superuser and item['name'].startswith('Statistics'):
#                 return False
#         return True


# admin_site.register_top_menu_item(_(u'1_Customers'),
#                                   icon_class="icon-user",
#                                   children=[{'name': _(u'Customers list'),
#                                              'admin_url': '/extranet/pyfreebill/company/?customer_enabled__exact=1',
#                                              'order': 1,
#                                              'title_icon': 'icon-list'},
#                                             {'name': _(u'SIP accounts'),
#                                              'admin_url': '/extranet/pyfreebill/customerdirectory/',
#                                              'order': 2,
#                                              'separator': True,
#                                              'title_icon': 'icon-check'},
#                                             {'name': _(u'Ratecards'),
#                                              'admin_url': '/extranet/pyfreebill/ratecard/',
#                                              'order': 3,
#                                              'separator': True,
#                                              'title_icon': 'icon-money'},
#                                             {'name': _(u'Rates'),
#                                              'admin_url': '/extranet/pyfreebill/customerrates/',
#                                              'order': 4,
#                                              'title_icon': 'icon-money'},
#                                             {'name': _(u'Destination number normalization'),
#                                              'admin_url': '/extranet/pyfreebill/customernormalizationrules/',
#                                              'order': 4,
#                                              'separator': True,
#                                              'title_icon': 'icon-medkit'},
#                                             {'name': _(u'CallerID normalization'),
#                                              'admin_url': '/extranet/pyfreebill/customercidnormalizationrules/',
#                                              'order': 5,
#                                              'title_icon': 'icon-medkit'},
#                                             {'name': _(u'Customer statistics'),
#                                              'admin_url': '/extranet/customers_stats/',
#                                              'order': 6,
#                                              'separator': True,
#                                              'title_icon': 'icon-dashboard'},
#                                             {'name': _(u'Destination statistics'),
#                                              'admin_url': '/extranet/destination_customers_stats/',
#                                              'order': 6,
#                                              'title_icon': 'icon-dashboard'}, ],
#                                   perms=perms_func)

# admin_site.register_top_menu_item(_(u'2_Providers'),
#                                   icon_class="icon-group",
#                                   children=[{'name': _(u'Providers list'),
#                                              'admin_url': '/extranet/pyfreebill/company/?supplier_enabled__exact=1',
#                                              'order': 1,
#                                              'title_icon': 'icon-list'},
#                                             {'name': _(u'Provider gateways'),
#                                              'admin_url': '/extranet/pyfreebill/sofiagateway/',
#                                              'order': 2,
#                                              'separator': True,
#                                              'title_icon': 'icon-check'},
#                                             {'name': _(u'Ratecards'),
#                                              'admin_url': '/extranet/pyfreebill/providertariff/',
#                                              'order': 3,
#                                              'separator': True,
#                                              'title_icon': 'icon-money'},
#                                             {'name': _(u'Rates'),
#                                              'admin_url': '/extranet/pyfreebill/providerrates/',
#                                              'order': 4,
#                                              'title_icon': 'icon-money'},
#                                             {'name': _(u'Destination number normalization'),
#                                              'admin_url': '/extranet/pyfreebill/carriernormalizationrules/',
#                                              'order': 5,
#                                              'separator': True,
#                                              'title_icon': 'icon-medkit'},
#                                             {'name': _(u'CallerID normalization'),
#                                              'admin_url': '/extranet/pyfreebill/carriercidnormalizationrules/',
#                                              'order': 6,
#                                              'title_icon': 'icon-medkit'},
#                                             {'name': _(u'Provider statistics'),
#                                              'admin_url': '/extranet/providers_stats/',
#                                              'order': 7,
#                                              'separator': True,
#                                              'title_icon': 'icon-dashboard'},
#                                             {'name': _(u'Destination statistics'),
#                                              'admin_url': '/extranet/destination_providers_stats/',
#                                              'order': 8,
#                                              'title_icon': 'icon-dashboard'}, ],
#                                   perms=perms_func)

# admin_site.register_top_menu_item(_(u'3_DID'),
#                                   icon_class="icon-headphones",
#                                   children=[{'name': 'DID list',
#                                              'admin_url': '/extranet/did/did',
#                                              'order': 1,
#                                              'title_icon': 'icon-list'},
#                                             {'name': 'Customer rates',
#                                              'admin_url': '/extranet/did/customerratesdid',
#                                              'order': 2,
#                                              'separator': True,
#                                              'title_icon': 'icon-money'},
#                                             {'name': 'Provider rates',
#                                              'admin_url': '/extranet/did/providerratesdid',
#                                              'order': 3,
#                                              'title_icon': 'icon-money'},
#                                             {'name': 'Bulk import',
#                                              'admin_url': '/extranet/did/wizard_import/',
#                                              'order': 4,
#                                              'separator': True,
#                                              'title_icon': 'icon-download-alt'},
#                                             {'name': 'Statistics',
#                                              'admin_url': '/extranet/pyfreebill/cdr/',
#                                              'order': 5,
#                                              'separator': True,
#                                              'title_icon': 'icon-dashboard'}, ],
#                                   perms=perms_func)

# admin_site.register_top_menu_item(_(u'4_Routing'),
#                                   icon_class="icon-exchange",
#                                   children=[{'name': _(u'LCR'),
#                                              'admin_url': '/extranet/pyfreebill/lcrgroup/',
#                                              'order': 1,
#                                              'title_icon': 'icon-random'},
#                                             {'name': _(u'Destination Number Normalization'),
#                                              'admin_url': '/extranet/pyfreebill/destinationnumberrules/',
#                                              'order': 2,
#                                              'separator': True,
#                                              'title_icon': 'icon-medkit'},
#                                             {'name': _(u'CallerID prefix management'),
#                                              'admin_url': '/extranet/pyfreebill/calleridprefixlist/',
#                                              'order': 3,
#                                              'separator': True,
#                                              'title_icon': 'icon-list'}, ],
#                                   perms=perms_func)

# admin_site.register_top_menu_item(_(u'5_Switches'),
#                                   icon_class="icon-cogs",
#                                   children=[{'name': _(u'Customer accounts'),
#                                              'admin_url': '/extranet/pyfreebill/customerdirectory/',
#                                              'order': 1,
#                                              'title_icon': 'icon-list'},
#                                             {'name': _(u'Provider gateways'),
#                                              'admin_url': '/extranet/pyfreebill/sofiagateway/',
#                                              'order': 2,
#                                              'title_icon': 'icon-list'},
#                                             {'name': _(u'Freeswitch status'),
#                                              'admin_url': '/extranet/FsServer/',
#                                              'order': 3,
#                                              'separator': True,
#                                              'title_icon': 'icon-user-md'},
#                                             {'name': _(u'Registration status'),
#                                              'admin_url': '/extranet/FsServerRegistry/',
#                                              'order': 4,
#                                              'title_icon': 'icon-user-md'},
#                                             {'name': _(u'Bridged Calls'),
#                                              'admin_url': '/extranet/FsServerBCalls/',
#                                              'order': 5,
#                                              'title_icon': 'icon-user-md'},
#                                             {'name': _(u'Freeswitch list'),
#                                              'admin_url': '/extranet/switch/voipswitch/',
#                                              'order': 6,
#                                              'title_icon': 'icon-list'},
#                                             {'name': _(u'Sofia profiles'),
#                                              'admin_url': '/extranet/pyfreebill/sipprofile/',
#                                              'order': 7,
#                                              'separator': True,
#                                              'title_icon': 'icon-cogs'}, ],
#                                   perms=perms_func)

# admin_site.register_top_menu_item(_(u'6_Finance'),
#                                   icon_class="icon-money",
#                                   children=[{'name': _(u'Add payment'),
#                                              'admin_url': '/extranet/pyfreebill/companybalancehistory/add/',
#                                              'order': 1,
#                                              'title_icon': 'icon-download-alt'},
#                                             {'name': _(u'History'),
#                                              'admin_url': '/extranet/pyfreebill/companybalancehistory/',
#                                              'order': 2,
#                                              'title_icon': 'icon-money'},
#                                              {'name': _(u'Currency Management'),
#                                              'admin_url': '/extranet/currencies/currency/',
#                                              'order': 3,
#                                              'separator': True,
#                                              'title_icon': 'icon-money'}, ],
#                                   perms=perms_func)

# admin_site.register_top_menu_item(_(u'7_Report'),
#                                   icon_class="icon-dashboard",
#                                   children=[{'name': _(u'CDR'),
#                                              'admin_url': '/extranet/cdrform/',
#                                              'order': 1,
#                                              'title_icon': 'icon-phone'},
#                                             {'name': _(u'Server status'),
#                                              'admin_url': '/extranet/ServerStatus/',
#                                              'order': 2,
#                                              'separator': True,
#                                              'title_icon': 'icon-dashboard'},
#                                              {'name': _(u'FreeSwitch status'),
#                                              'admin_url': '/extranet/FsServer/',
#                                              'order': 3,
#                                              'separator': True,
#                                              'title_icon': 'icon-dashboard'}, ],
#                                   perms=perms_func)


# admin_site.register_top_menu_item(_(u'8_Admin'),
#                                   icon_class="icon-wrench",
#                                   children=[{'name': _(u'Users'),
#                                              'admin_url': '/extranet/auth/user/',
#                                              'order': 1,
#                                              'title_icon': 'icon-user'},
#                                             {'name': _(u'Access logs'),
#                                              'admin_url': '/extranet/axes/accesslog/',
#                                              'order': 2,
#                                              'separator': True,
#                                              'title_icon': 'icon-key'},
#                                             {'name': _(u'Access attempts'),
#                                              'admin_url': '/extranet/axes/accessattempt/',
#                                              'order': 3,
#                                              'title_icon': 'icon-warning-sign'},
#                                              {'name': _(u'Honeypot logs'),
#                                              'admin_url': '/extranet/admin_honeypot/loginattempt/',
#                                              'order': 4,
#                                              'separator': True,
#                                              'title_icon': 'icon-warning-sign'},
#                                             {'name': _(u'Admin logs'),
#                                              'admin_url': '/extranet/admin/logentry/',
#                                              'order': 5,
#                                              'separator': True,
#                                              'title_icon': 'icon-exclamation-sign'},
#                                             {'name': _(u'Recurring task logs'),
#                                              'admin_url': '/extranet/chroniker/log/',
#                                              'order': 6,
#                                              'title_icon': 'icon-puzzle-piece'},
#                                              {'name': _(u'Import logs'),
#                                              'admin_url': '/extranet/simple_import/importlog/',
#                                              'order': 7,
#                                              'title_icon': 'icon-download-alt'},
#                                             {'name': _(u'Version'),
#                                              'admin_url': '/extranet/status/',
#                                              'order': 8,
#                                              'separator': True,
#                                              'title_icon': 'icon-pushpin'}, ],
#                                   perms=perms_func)


urlpatterns = [
    # url(r'^$',
    #     TemplateView.as_view(template_name='pages/home.html'),
    #     name='home'),
    # url(r'^about/$',
    #     TemplateView.as_view(template_name='pages/about.html'),
    #     name='about'),

    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
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

    # Simple import module
    url(
        r'^extranet/simple_import/',
        include('simple_import.urls')
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

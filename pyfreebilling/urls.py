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

from django.conf.urls import patterns, include, url, handler404, handler500
from django.contrib import admin
from django.http import request
from django.views.generic.base import TemplateView

from yawdadmin import admin_site

from pyfreebilling.settings import DEBUG

from pyfreebill.views import chart_stats_general_json, FsDirectoryUpdateView, FsSofiaUpdateView


from customerportal.urls import urlpatterns as customerportal_url
from customerportal.views import Template404View, Template500View


admin.autodiscover()
admin_site._registry.update(admin.site._registry)


handler404 = Template404View.as_view()
handler500 = Template500View.as_view()

# Custom menu
def perms_func(request, item):
        if not request.user.is_superuser and item['name'].startswith('Statistics'):
                return False
        return True


admin_site.register_top_menu_item('1_Customers',
                                  icon_class="icon-user",
                                  children=[{'name': 'Customers list',
                                             'admin_url': '/extranet/pyfreebill/company/?customer_enabled__exact=1',
                                             'order': 1,
                                             'title_icon': 'icon-list'},
                                            {'name': 'SIP accounts',
                                             'admin_url': '/extranet/pyfreebill/customerdirectory/',
                                             'order': 2,
                                             'separator': True,
                                             'title_icon': 'icon-check'},
                                            {'name': 'Ratecards',
                                             'admin_url': '/extranet/pyfreebill/ratecard/',
                                             'order': 3,
                                             'separator': True,
                                             'title_icon': 'icon-money'},
                                            {'name': 'Rates',
                                             'admin_url': '/extranet/pyfreebill/customerrates/',
                                             'order': 4,
                                             'title_icon': 'icon-money'},
                                            {'name': 'Destination number normalization',
                                             'admin_url': '/extranet/pyfreebill/customernormalizationrules/',
                                             'order': 4,
                                             'separator': True,
                                             'title_icon': 'icon-medkit'},
                                            {'name': 'CallerID normalization',
                                             'admin_url': '/extranet/pyfreebill/customercidnormalizationrules/',
                                             'order': 5,
                                             'title_icon': 'icon-medkit'},
                                            {'name': 'Customer statistics',
                                             'admin_url': '/extranet/customers_stats/',
                                             'order': 6,
                                             'separator': True,
                                             'title_icon': 'icon-dashboard'},
                                             {'name': 'Destination statistics',
                                             'admin_url': '/extranet/destination_customers_stats/',
                                             'order': 6,
                                             'title_icon': 'icon-dashboard'}, ],
                                  perms=perms_func)

admin_site.register_top_menu_item('2_Providers',
                                  icon_class="icon-group",
                                  children=[{'name': 'Providers list',
                                             'admin_url': '/extranet/pyfreebill/company/?supplier_enabled__exact=1',
                                             'order': 1,
                                             'title_icon': 'icon-list'},
                                            {'name': 'Provider gateways',
                                             'admin_url': '/extranet/pyfreebill/sofiagateway/',
                                             'order': 2,
                                             'separator': True,
                                             'title_icon': 'icon-check'},
                                            {'name': 'Ratecards',
                                             'admin_url': '/extranet/pyfreebill/providertariff/',
                                             'order': 3,
                                             'separator': True,
                                             'title_icon': 'icon-money'},
                                            {'name': 'Rates',
                                             'admin_url': '/extranet/pyfreebill/providerrates/',
                                             'order': 4,
                                             'title_icon': 'icon-money'},
                                            {'name': 'Destination number normalization',
                                             'admin_url': '/extranet/pyfreebill/carriernormalizationrules/',
                                             'order': 5,
                                             'separator': True,
                                             'title_icon': 'icon-medkit'},
                                            {'name': 'CallerID normalization',
                                             'admin_url': '/extranet/pyfreebill/carriercidnormalizationrules/',
                                             'order': 6,
                                             'title_icon': 'icon-medkit'},
                                            {'name': 'Provider statistics',
                                             'admin_url': '/extranet/providers_stats/',
                                             'order': 7,
                                             'separator': True,
                                             'title_icon': 'icon-dashboard'},
                                             {'name': 'Destination statistics',
                                             'admin_url': '/extranet/destination_providers_stats/',
                                             'order': 8,
                                             'title_icon': 'icon-dashboard'}, ],
                                  perms=perms_func)

admin_site.register_top_menu_item('3_DID',
                                  icon_class="icon-headphones",
                                  children=[{'name': 'DID list',
                                             'admin_url': '/extranet/did/did',
                                             'order': 1,
                                             'title_icon': 'icon-list'},
                                            {'name': 'Customer rates',
                                             'admin_url': '/extranet/did/customerratesdid',
                                             'order': 2,
                                             'separator': True,
                                             'title_icon': 'icon-money'},
                                            {'name': 'Provider rates',
                                             'admin_url': '/extranet/did/providerratesdid',
                                             'order': 3,
                                             'title_icon': 'icon-money'},
                                            {'name': 'Bulk import',
                                             'admin_url': '/extranet/did/wizard_import/',
                                             'order': 4,
                                             'separator': True,
                                             'title_icon': 'icon-download-alt'},
                                            {'name': 'Statistics',
                                             'admin_url': '/extranet/pyfreebill/cdr/',
                                             'order': 5,
                                             'separator': True,
                                             'title_icon': 'icon-dashboard'}, ],
                                  perms=perms_func)

admin_site.register_top_menu_item('4_Routing',
                                  icon_class="icon-exchange",
                                  children=[{'name': 'LCR',
                                             'admin_url': '/extranet/pyfreebill/lcrgroup/',
                                             'order': 1,
                                             'title_icon': 'icon-random'},
                                            {'name': 'Destination Number Normalization',
                                             'admin_url': '/extranet/pyfreebill/destinationnumberrules/',
                                             'order': 2,
                                             'separator': True,
                                             'title_icon': 'icon-medkit'},
                                            {'name': 'CallerID prefix management',
                                             'admin_url': '/extranet/pyfreebill/calleridprefixlist/',
                                             'order': 3,
                                             'separator': True,
                                             'title_icon': 'icon-list'}, ],
                                  perms=perms_func)

admin_site.register_top_menu_item('5_Switches',
                                  icon_class="icon-cogs",
                                  children=[{'name': 'Customer accounts',
                                             'admin_url': '/extranet/pyfreebill/customerdirectory/',
                                             'order': 1,
                                             'title_icon': 'icon-list'},
                                            {'name': 'Provider gateways',
                                             'admin_url': '/extranet/pyfreebill/sofiagateway/',
                                             'order': 2,
                                             'title_icon': 'icon-list'},
                                            {'name': 'Freeswitch status',
                                             'admin_url': '/extranet/FsServer/',
                                             'order': 3,
                                             'separator': True,
                                             'title_icon': 'icon-user-md'},
                                            {'name': 'Registration status',
                                             'admin_url': '/extranet/FsServerRegistry/',
                                             'order': 4,
                                             'title_icon': 'icon-user-md'},
                                            {'name': 'Bridged Calls',
                                             'admin_url': '/extranet/FsServerBCalls/',
                                             'order': 5,
                                             'title_icon': 'icon-user-md'},
                                            {'name': 'Freeswitch list',
                                             'admin_url': '/extranet/switch/voipswitch/',
                                             'order': 6,
                                             'title_icon': 'icon-list'},
                                            {'name': 'Sofia profiles',
                                             'admin_url': '/extranet/pyfreebill/sipprofile/',
                                             'order': 7,
                                             'separator': True,
                                             'title_icon': 'icon-cogs'}, ],
                                  perms=perms_func)

admin_site.register_top_menu_item('6_Finance',
                                  icon_class="icon-money",
                                  children=[{'name': 'Add payment',
                                             'admin_url': '/extranet/pyfreebill/companybalancehistory/add/',
                                             'order': 1,
                                             'title_icon': 'icon-download-alt'},
                                            {'name': 'History',
                                             'admin_url': '/extranet/pyfreebill/companybalancehistory/',
                                             'order': 2,
                                             'title_icon': 'icon-money'},
                                             {'name': 'Currency Management',
                                             'admin_url': '/extranet/currencies/currency/',
                                             'order': 3,
                                             'separator': True,
                                             'title_icon': 'icon-money'}, ],
                                  perms=perms_func)

admin_site.register_top_menu_item('7_Report',
                                  icon_class="icon-dashboard",
                                  children=[{'name': 'CDR',
                                             'admin_url': '/extranet/cdrform/',
                                             'order': 1,
                                             'title_icon': 'icon-phone'},
                                            {'name': 'Server status',
                                             'admin_url': '/extranet/ServerStatus/',
                                             'order': 2,
                                             'separator': True,
                                             'title_icon': 'icon-dashboard'},
                                             {'name': 'FreeSwitch status',
                                             'admin_url': '/extranet/FsServer/',
                                             'order': 3,
                                             'separator': True,
                                             'title_icon': 'icon-dashboard'}, ],
                                  perms=perms_func)


admin_site.register_top_menu_item('8_Admin',
                                  icon_class="icon-wrench",
                                  children=[{'name': 'Users',
                                             'admin_url': '/extranet/auth/user/',
                                             'order': 1,
                                             'title_icon': 'icon-user'},
                                            {'name': 'Access logs',
                                             'admin_url': '/extranet/axes/accesslog/',
                                             'order': 2,
                                             'separator': True,
                                             'title_icon': 'icon-key'},
                                            {'name': 'Access attempts',
                                             'admin_url': '/extranet/axes/accessattempt/',
                                             'order': 3,
                                             'title_icon': 'icon-warning-sign'},
                                             {'name': 'Honeypot logs',
                                             'admin_url': '/extranet/admin_honeypot/loginattempt/',
                                             'order': 4,
                                             'separator': True,
                                             'title_icon': 'icon-warning-sign'},
                                             {'name': 'Visitors stats',
                                             'admin_url': '/extranet/request/request/overview/',
                                             'order': 5,
                                             'separator': True,
                                             'title_icon': 'icon-exclamation-sign'},
                                            {'name': 'Admin logs',
                                             'admin_url': '/extranet/admin/logentry/',
                                             'order': 6,
                                             'separator': True,
                                             'title_icon': 'icon-exclamation-sign'},
                                            {'name': 'Recurring task logs',
                                             'admin_url': '/extranet/chroniker/log/',
                                             'order': 7,
                                             'title_icon': 'icon-puzzle-piece'},
                                             {'name': 'Import logs',
                                             'admin_url': '/extranet/simple_import/importlog/',
                                             'order': 8,
                                             'title_icon': 'icon-download-alt'},
                                            {'name': 'Database size',
                                             'admin_url': '/extranet/database_size/table/',
                                             'order': 9,
                                             'separator': True,
                                             'title_icon': 'icon-pushpin'},
                                            {'name': 'Version',
                                             'admin_url': '/extranet/status/',
                                             'order': 10,
                                             'separator': True,
                                             'title_icon': 'icon-pushpin'}, ],
                                  perms=perms_func)


# Modules
urlpatterns = customerportal_url

if DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', TemplateView.as_view(template_name="customer/500.html")),
        (r'^404/$', TemplateView.as_view(template_name="customer/404.html")),
    )

urlpatterns += patterns('',
                       url(r'^extranet/report/$',
                           'pyfreebill.views.admin_report_view'),
                       url(r'^extranet/FsServer/$',
                           'switch.views.fs_status_view'),
                       url(r'^extranet/FsServerRegistry/$',
                           'switch.views.fs_registry_view'),
                       url(r'^extranet/FsServerBCalls/$',
                           'switch.views.fs_bcalls_view'),
                       url(r'^extranet/cdrform/$',
                           'pyfreebill.views.live_report_view'),
                       url(r'^extranet/status/$',
                           'pyfreebill.views.admin_status_view'),
                       url(r'^extranet/list_models/$',
                           'pyfreebill.views.admin_listmodels_view'),
                       url(r'^extranet/customers_stats/$',
                           'pyfreebill.views.customers_stats_view', name='customers_stats'),
                       url(r'^extranet/destination_customers_stats/$',
                           'pyfreebill.views.destination_customers_stats_view', name='dest_customers_stats'),
                       url(r'^extranet/providers_stats/$',
                           'pyfreebill.views.providers_stats_view', name='providers_stats'),
                       url(r'^extranet/destination_providers_stats/$',
                           'pyfreebill.views.destination_providers_stats_view', name='dest_providers_stats'),
                       url(r'^extranet/ServerStatus/$',
                           'switch.views.server_status_view'),
                       url(r'^extranet/did/wizard_import/$',
                           'did.views.start_import',),
                       url(r'^i18n/', include('django.conf.urls.i18n')),
                       url(r'^admin/',
                           include('admin_honeypot.urls')),
                       url(r'^extranet/simple_import/',
                           include('simple_import.urls')),
                       url(r'^extranet/FsDirectoryUpdate/',
                           'pyfreebill.views.FsDirectoryUpdateView',
                           name='fs_directory_update'),
                       url(r'^extranet/FsSofiaUpdate/',
                           'pyfreebill.views.FsSofiaUpdateView',
                           name='fs_sofia_update'),
                       url(r'^extranet/',
                           include(admin_site.urls)),
                       url(regex=r'^chart_stats_general_json/$',
                           view=chart_stats_general_json,
                           name='chart_stats_general_json'),
                       url(r'^extranet/',
                           include("massadmin.urls")), )

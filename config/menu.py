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

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for pyfreebilling admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.MenuItem(_('Companies'), reverse('admin:pyfreebill_company_changelist'),
                children=[
                    items.MenuItem(_('Customers'), '/extranet/pyfreebill/company/?customer_enabled__exact=1',
                        children=[
                            items.MenuItem(_('List'), '/extranet/pyfreebill/company/?customer_enabled__exact=1',
                                children=[
                                    items.MenuItem(_('All'), '/extranet/pyfreebill/company/?customer_enabled__exact=1'),
                                    items.MenuItem(_('Prepaid Account'), '/extranet/pyfreebill/company/?customer_enabled__exact=1&prepaid__exact=1'),
                                    items.MenuItem(_('Postpaid account'), '/extranet/pyfreebill/company/?customer_enabled__exact=1&prepaid__exact=0'),
                                    items.MenuItem(_('Add new customer'), '/extranet/pyfreebill/company/add/'),
                                ]
                            ),
                            items.MenuItem(_('Balance history'), '/extranet/pyfreebill/companybalancehistory/'),
                            items.MenuItem(_('Add payment'), '/extranet/pyfreebill/companybalancehistory/add/'),
                            items.MenuItem(_('Customer management'),
                                children=[
                                    items.MenuItem(_('Customer SIP accounts'), '/extranet/customerdirectory/customerdirectory/'),
                                    items.MenuItem(_('DIDs management'), reverse('admin:did_did_changelist'),
                                        children=[
                                            items.MenuItem(_('DIDs list'), reverse('admin:did_did_changelist')),
                                            items.MenuItem(_('DIDs routing'), reverse('admin:did_routesdid_changelist')),
                                        ]
                                    ),
                                    # items.MenuItem(_('Destination number normalization rules'), '/extranet/pyfreebill/customernormalizationrules/'),
                                    # items.MenuItem(_('CallerID Normalization Rules'), '/extranet/pyfreebill/customercidnormalizationrules/'),
                                ]
                            ),
                            items.MenuItem(_('Customer statistics'),
                                children=[
                                    items.MenuItem(_('Statistics'), reverse('admin:pyfreebill_salesummary_changelist')),
                                    items.MenuItem(_('Destinations statistics'), reverse('pyfreebill:dest_customers_stats')),
                                ]
                            ),
                        ]
                    ),
                    items.MenuItem(_('Providers'), '/extranet/pyfreebill/company/?supplier_enabled__exact=1',
                        children=[
                            items.MenuItem(_('List'), '/extranet/pyfreebill/company/?supplier_enabled__exact=1',
                                children=[
                                    items.MenuItem(_('All'), '/extranet/pyfreebill/company/?supplier_enabled__exact=1'),
                                    items.MenuItem(_('Add new provider'), '/extranet/pyfreebill/company/add/'),
                                ]
                            ),
                            items.MenuItem(_('provider management'),
                                children=[
                                    items.MenuItem(_('Provider gateways'), reverse('admin:pyfreebill_sofiagateway_changelist')),
                                    items.MenuItem(_('CalleeID Normalization Rules'), reverse('admin:pyfreebill_carriernormalizationrules_changelist')),
                                    items.MenuItem(_('CallerID Normalization Rules'), reverse('admin:pyfreebill_carriercidnormalizationrules_changelist')),
                                ]
                            ),
                            items.MenuItem(_('Provider statistics'),
                                children=[
                                    items.MenuItem(_('Statistics'), reverse('admin:pyfreebill_costsummary_changelist')),
                                    items.MenuItem(_('Destinations statistics'), reverse('pyfreebill:dest_providers_stats')),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            items.MenuItem(_('Rates'),
                children=[
                    items.MenuItem(_('Sell rates'),
                        children=[
                            items.MenuItem(_('Ratecards'), reverse('admin:pyfreebill_ratecard_changelist')),
                            items.MenuItem(_('CallerID prefix list for filtering'), reverse('admin:pyfreebill_calleridprefixlist_changelist')),
                            items.MenuItem(_('Rates'), reverse('admin:pyfreebill_customerrates_changelist')),
                            items.MenuItem(_('Customer - ratecard association'), reverse('admin:pyfreebill_customerratecards_changelist')),
                        ]
                    ),
                    items.MenuItem(_('Provider rates'),
                        children=[
                            items.MenuItem(_('Provider tariffs'), reverse('admin:pyfreebill_providertariff_changelist')),
                            items.MenuItem(_('Provider rates'), reverse('admin:pyfreebill_providerrates_changelist')),
                        ]
                    ),
                ]
            ),
            items.MenuItem(_('Routing'),
                children=[
                    items.MenuItem(_('LCRs'), reverse('admin:pyfreebill_lcrgroup_changelist')),
                    items.MenuItem(_('DIDs management'), reverse('admin:did_did_changelist')),
                    items.MenuItem(_('Route mapping rules'), reverse('admin:normalizationrule_callmappingrule_changelist')),
                    items.MenuItem(_('Number normalization management'),
                        children=[
                            items.MenuItem(_('Number normalization groups'), reverse('admin:normalizationrule_normalizationgroup_changelist')),
                            items.MenuItem(_('Number normalization rules'), reverse('admin:normalizationrule_normalizationrule_changelist')),
                        ]
                    ),
                ]
            ),
            items.MenuItem(_('Finance'),
                children=[
                    items.MenuItem(_('Add payment'), reverse('admin:pyfreebill_companybalancehistory_add')),
                    items.MenuItem(_('History'), reverse('admin:pyfreebill_companybalancehistory_changelist')),
                ]
            ),
            items.MenuItem(_('Stats and reports'),
                children=[
                    items.MenuItem(_('CDRs'), '/extranet/cdrform/',
                        children=[
                            items.MenuItem(_('CDRs view'), '/extranet/cdr/cdr/'),
                            items.MenuItem(_('Successfull CDRs'), '/extranet/cdr/cdr/?effective_duration__gt=0'),
                            items.MenuItem(_('Failed CDRs'), '/extranet/cdr/cdr/?effective_duration__exact=0'),
                            # items.MenuItem(_('Hangup Cause'), '/extranet/pyfreebill/hangupcause/'),
                        ]
                    ),
                    items.MenuItem(_('Customer statistics'),
                        children=[
                            items.MenuItem(_('Statistics'), reverse('admin:pyfreebill_salesummary_changelist')),
                            items.MenuItem(_('Destinations statistics'), reverse('pyfreebill:dest_customers_stats')),
                        ]
                    ),
                    items.MenuItem(_('Provider statistics'),
                        children=[
                            items.MenuItem(_('Statistics'), reverse('admin:pyfreebill_costsummary_changelist')),
                            items.MenuItem(_('Destinations statistics'), reverse('pyfreebill:dest_providers_stats')),
                        ]
                    ),
                    items.MenuItem(_('Server status'), reverse('switch:ServerStatus')),
                ]
            ),
            items.MenuItem(_('Admin'),
                children=[
                    items.MenuItem(_('Users'), reverse('admin:auth_user_changelist'),
                        children=[
                            items.MenuItem(_('Users list'), reverse('admin:auth_user_changelist')),
                            items.MenuItem(_('Groups list'), reverse('admin:auth_group_changelist')),
                        ]
                    ),
                    items.MenuItem(_('Destinations and prefix management'),
                        children=[
                            items.MenuItem(_('Prefix'), reverse('admin:direction_prefix_changelist')),
                            items.MenuItem(_('Destinations'), reverse('admin:direction_destination_changelist')),
                            items.MenuItem(_('Countries'), reverse('admin:direction_country_changelist')),
                            items.MenuItem(_('Regions'), reverse('admin:direction_region_changelist')),
                            items.MenuItem(_('Carriers'), reverse('admin:direction_carrier_changelist')),
                            items.MenuItem(_('Type of destination'), reverse('admin:direction_type_changelist')),
                        ]
                    ),
                    items.MenuItem(_('Configuration'),
                        children=[
                            items.MenuItem(_('VoIP switches'), reverse('admin:switch_voipswitch_changelist')),
                            items.MenuItem(_('FS SIP profiles'), reverse('admin:pyfreebill_sipprofile_changelist')),
                            items.MenuItem(_('SIP domains'), reverse('admin:switch_domain_changelist')),
                            #if settings.PFB_URGENCY:
                            #    items.MenuItem(_('PDAU'), reverse('admin:urgencyfr_pdau_changelist')),
                        ]
                    ),
                    items.MenuItem(_('Logs'),
                        children=[
                            items.MenuItem(_('Access logs'), reverse('admin:axes_accesslog_changelist')),
                            items.MenuItem(_('Access attemps'), reverse('admin:axes_accessattempt_changelist')),
                            items.MenuItem(_('Honeypot access attemps'), reverse('admin:admin_honeypot_loginattempt_changelist')),
                            items.MenuItem(_('Recurring tasks logs'), reverse('admin:chroniker_log_changelist')),
                        ]
                    ),
                    items.MenuItem(_('PyFreeBilling version'), '/extranet/status/'),
                    items.MenuItem(_('PyFreeBilling license'), '/extranet/license/'),
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)

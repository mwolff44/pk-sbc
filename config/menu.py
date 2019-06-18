from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from admin_tools.menu import items, Menu
from admin_tools.utils import get_admin_site_name


class CustomMenu(Menu):
    """
    Custom Menu for pyfreebilling admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('PyFB'), reverse('admin:index')),
            items.MenuItem(_('Companies'), reverse('admin:pyfb_company_company_changelist'),
                children=[
                    items.MenuItem(_('Customers'), reverse('admin:pyfb_company_customer_changelist'),
                        children=[
                            items.MenuItem(_('List'), reverse('admin:pyfb_company_customer_changelist')),
                            items.MenuItem(_('Add new customer'), reverse('admin:pyfb_company_customer_add')),
                            items.MenuItem(_('Customer endpoints'), reverse('admin:pyfb_endpoint_customerendpoint_changelist'),
                            #         items.MenuItem(_('DIDs management'), reverse('admin:did_did_changelist'),
                            #             children=[
                            #                 items.MenuItem(_('DIDs list'), reverse('admin:did_did_changelist')),
                            #                 items.MenuItem(_('DIDs routing'), reverse('admin:did_routesdid_changelist')),
                            #             ]
                            #         ),
                            #         # items.MenuItem(_('Destination number normalization rules'), '/extranet/pyfreebill/customernormalizationrules/'),
                            #         # items.MenuItem(_('CallerID Normalization Rules'), '/extranet/pyfreebill/customercidnormalizationrules/'),
                            #     ]
                            # ),
                            ),
                        ]
                    ),
                    items.MenuItem(_('Providers'), reverse('admin:pyfb_company_provider_changelist'),
                        children=[
                            items.MenuItem(_('List'), reverse('admin:pyfb_company_provider_changelist')),
                            items.MenuItem(_('Add new provider'), reverse('admin:pyfb_company_provider_add')),
                            items.MenuItem(_('Provider gateways'), reverse('admin:pyfb_endpoint_providerendpoint_changelist')),
                        ]
                    ),
                ]
            ),
            items.MenuItem(_('Rates'),
                children=[
                    items.MenuItem(_('Customer ratecards'), reverse('admin:pyfb_rating_customerratecard_changelist')),
                    items.MenuItem(_('Provider ratecards'), reverse('admin:pyfb_rating_providerratecard_changelist')),
                    items.MenuItem(_('Customer ratecard allocation'), reverse('admin:pyfb_rating_customerrcallocation_changelist')),
                    # items.MenuItem(_('CallerID prefix list for filtering'), reverse('admin:pyfreebill_calleridprefixlist_changelist')),
                ]
            ),
            items.MenuItem(_('Routing'),
                children=[
                    items.MenuItem(_('Routing rules'), reverse('admin:pyfb_routing_routinggroup_changelist')),
                    items.MenuItem(_('Route mapping rules'), reverse('admin:pyfb_normalization_callmappingrule_changelist')),
                    items.MenuItem(_('Customer routing group allocation'), reverse('admin:pyfb_routing_customerroutinggroup_changelist')),
                ]
            ),
            items.MenuItem(_('DIDs'), reverse('admin:pyfb_did_did_changelist')),
            items.MenuItem(_('Finance'),
                children=[
                    items.MenuItem(_('Add payment'), reverse('admin:pyfb_company_companybalancehistory_add')),
                    items.MenuItem(_('History'), reverse('admin:pyfb_company_companybalancehistory_changelist')),
                ]
            ),
            items.MenuItem(_('Stats and reports'),
                children=[
                    items.MenuItem(_('CDRs'), '/extranet/cdrform/',
                        children=[
                            items.MenuItem(_('Call Detail Report'), reverse('admin:pyfb_reporting_cdr_changelist')),
                            items.MenuItem(_('CDRs view'), reverse('admin:pyfb_kamailio_acccdr_changelist')),
                            items.MenuItem(_('Successfull CDRs'), reverse('admin:pyfb_kamailio_acc_changelist')),
                            items.MenuItem(_('Failed CDRs'), reverse('admin:pyfb_kamailio_missedcall_changelist')),
                            # items.MenuItem(_('Hangup Cause'), '/extranet/pyfreebill/hangupcause/'),
                        ]
                    ),
                    # items.MenuItem(_('Customer statistics'),
                    #     children=[
                    #         items.MenuItem(_('Statistics'), reverse('admin:pyfreebill_salesummary_changelist')),
                    #         items.MenuItem(_('Destinations statistics'), reverse('pyfreebill:dest_customers_stats')),
                    #     ]
                    # ),
                    # items.MenuItem(_('Provider statistics'),
                    #     children=[
                    #         items.MenuItem(_('Statistics'), reverse('admin:pyfreebill_costsummary_changelist')),
                    #         items.MenuItem(_('Destinations statistics'), reverse('pyfreebill:dest_providers_stats')),
                    #     ]
                    # ),
                    # items.MenuItem(_('Server status'), reverse('switch:ServerStatus')),
                ]
            ),
            items.MenuItem(_('Admin'),
                children=[
                    items.MenuItem(_('Users'), reverse('admin:users_user_changelist'),
                        children=[
                            items.MenuItem(_('Users list'), reverse('admin:users_user_changelist')),
                            items.MenuItem(_('Groups list'), reverse('admin:auth_group_changelist')),
                        ]
                    ),
                    items.MenuItem(_('Destinations and prefix management'),
                        children=[
                            items.MenuItem(_('Prefix'), reverse('admin:pyfb_direction_prefix_changelist')),
                            items.MenuItem(_('Destinations'), reverse('admin:pyfb_direction_destination_changelist')),
                            items.MenuItem(_('Countries'), reverse('admin:pyfb_direction_country_changelist')),
                            items.MenuItem(_('Regions'), reverse('admin:pyfb_direction_region_changelist')),
                            items.MenuItem(_('Carriers'), reverse('admin:pyfb_direction_carrier_changelist')),
                            items.MenuItem(_('Type of destination'), reverse('admin:pyfb_direction_type_changelist')),
                        ]
                    ),
                    items.MenuItem(_('Configuration'),
                        children=[
                            items.MenuItem(_('Domain management'), reverse('admin:pyfb_kamailio_domain_changelist')),
                            items.MenuItem(_('RTP proxies'), reverse('admin:pyfb_kamailio_rtpengine_changelist')),
                            items.MenuItem(_('CallerID prefix list for filtering'), reverse('admin:pyfb_rating_callernumlist_changelist')),
                            items.MenuItem(_('Codecs'), reverse('admin:pyfb_endpoint_codec_changelist')),
                            items.MenuItem(_('Number normalization management'),
                                children=[
                                    items.MenuItem(_('Number normalization groups'), reverse('admin:pyfb_normalization_normalizationgrp_changelist')),
                                    items.MenuItem(_('Number normalization rules'), reverse('admin:pyfb_normalization_normalizationrule_changelist')),
                                ]
                            ),
                            #if settings.PFB_URGENCY:
                            #    items.MenuItem(_('PDAU'), reverse('admin:urgencyfr_pdau_changelist')),
                        ]
                    ),
                    # items.MenuItem(_('Logs'),
                    #     children=[
                    #         items.MenuItem(_('Access logs'), reverse('admin:axes_accesslog_changelist')),
                    #         items.MenuItem(_('Access attemps'), reverse('admin:axes_accessattempt_changelist')),
                    #         items.MenuItem(_('Honeypot access attemps'), reverse('admin:admin_honeypot_loginattempt_changelist')),
                    #         items.MenuItem(_('Recurring tasks logs'), reverse('admin:chroniker_log_changelist')),
                    #     ]
                    # ),
                    # items.MenuItem(_('PyFreeBilling version'), '/extranet/status/'),
                    # items.MenuItem(_('PyFreeBilling license'), '/extranet/license/'),
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)

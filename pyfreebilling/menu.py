"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'pyfreebilling.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for pyfreebilling admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            items.MenuItem(_('Companies'),
                children=[
                    items.MenuItem(_('Companies'),
                        children=[
                            items.MenuItem(_('List'), '/extranet/pyfreebill/company/'),
                            items.MenuItem(_('Balance history'), '/extranet/pyfreebill/companybalancehistory/'),
                            items.MenuItem(_('Customer SIP accounts'), '/extranet/pyfreebill/customerdirectory/'),
                            items.MenuItem(_('Provider gateways'), '/extranet/pyfreebill/sofiagateway/'),
                        ]
                    ),
                    items.MenuItem(_('Contacts'), '/extranet/pyfreebill/person/'),
                    items.MenuItem(_('Groups'), '/extranet/pyfreebill/group/'),
                ]
            ),
            items.MenuItem(_('Rates'),
                children=[
                    items.MenuItem(_('Sell rates'),
                        children=[
                            items.MenuItem(_('Ratecards'), '/extranet/pyfreebill/ratecard/'),
                            items.MenuItem(_('Customer ratecards'), '/extranet/pyfreebill/customerratecards/'),
                            items.MenuItem(_('Rates'), '/extranet/pyfreebill/customerrates/'),
                        ]
                    ),
                    items.MenuItem(_('LCRs'), '/extranet/pyfreebill/lcrgroup/'),
                    items.MenuItem(_('Provider rates'),
                        children=[
                            items.MenuItem(_('Provider tariffs'), '/extranet/pyfreebill/providertariff/'),
                            items.MenuItem(_('Provider rates'), '/extranet/pyfreebill/providerrates/'),
                        ]
                    ),
                ]
            ),
            items.MenuItem(_('Reports'),
                children=[
                    items.MenuItem(_('CDRs'), '/extranet/pyfreebill/cdr/',
                        children=[
                            items.MenuItem(_('CDRs view'), '/extranet/pyfreebill/cdr/'),
                            items.MenuItem(_('Hangup Cause'), '/extranet/pyfreebill/hangupcause/'),
                        ]
                    ),
                    items.MenuItem(_('Reports'), '/extranet/report/'),
                ]
            ),
            items.MenuItem(_('Admin'),
                children=[
                    items.MenuItem(_('Users'), '/extranet/auth/',
                        children=[
                            items.MenuItem(_('Groups'), '/extranet/auth/group/'),
                            items.MenuItem(_('Users'), '/extranet/auth/user/'),
                            items.MenuItem(_('Rates'), '/extranet/pyfreebill/customerrates/'),
                        ]
                    ),
                    items.MenuItem(_('VoIP switches'),
                        children=[
                            items.MenuItem(_('VoIP switches'), '/extranet/pyfreebill/voipswitch/'),
                            items.MenuItem(_('SIP profiles'), '/extranet/pyfreebill/sipprofile/'),
                            items.MenuItem(_('ACL'), '/extranet/pyfreebill/acllists/'),
                        ]
                    ),
                    items.MenuItem(_('Logs'),
                        children=[
                            items.MenuItem(_('Access logs'), '/extranet/axes/accesslog/'),
                            items.MenuItem(_('Access attemps'), '/extranet/axes/accessattempt/'),
                        ]
                    ),
                ]
            ),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)

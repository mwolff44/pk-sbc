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
                            items.MenuItem(_('List'), '/admin/pyfreebill/company/'),
                            items.MenuItem(_('Balance history'), '/admin/pyfreebill/companybalancehistory/'),
                            items.MenuItem(_('Customer SIP accounts'), '/admin/pyfreebill/customerdirectory/'),
                            items.MenuItem(_('Provider gateways'), '/admin/pyfreebill/sofiagateway/'),
                        ]
                    ),
                    items.MenuItem(_('Contacts'), '/admin/pyfreebill/person/'),
                    items.MenuItem(_('Groups'), '/admin/pyfreebill/group/'),
                ]
            ),
            items.MenuItem(_('Rates'),
                children=[
                    items.MenuItem(_('Sell rates'),
                        children=[
                            items.MenuItem(_('Ratecards'), '/admin/pyfreebill/ratecard/'),
                            items.MenuItem(_('Customer ratecards'), '/admin/pyfreebill/customerratecards/'),
                            items.MenuItem(_('Rates'), '/admin/pyfreebill/customerrates/'),
                        ]
                    ),
                    items.MenuItem(_('LCRs'), '/admin/pyfreebill/lcrgroup/'),
                    items.MenuItem(_('Provider rates'),
                        children=[
                            items.MenuItem(_('Provider tariffs'), '/admin/pyfreebill/providertariff/'),
                            items.MenuItem(_('Provider rates'), '/admin/pyfreebill/providerrates/'),
                        ]
                    ),
                ]
            ),
            items.MenuItem(_('CDRs'), '/admin/pyfreebill/cdr/'),
           # items.AppList(
           #     _('Applications'),
           #     exclude=('django.contrib.*',)
           # ),
            items.MenuItem(_('Admin'),
                children=[
                    items.MenuItem(_('Users'), '/admin/auth/',
                        children=[
                            items.MenuItem(_('Groups'), '/admin/auth/group/'),
                            items.MenuItem(_('Users'), '/admin/auth/user/'),
                            items.MenuItem(_('Rates'), '/admin/pyfreebill/customerrates/'),
                        ]
                    ),
                    items.MenuItem(_('VoIP switches'),
                        children=[
                            items.MenuItem(_('VoIP switches'), '/admin/pyfreebill/voipswitch/'),
                            items.MenuItem(_('SIP profiles'), '/admin/pyfreebill/sipprofile/'),
                            items.MenuItem(_('ACL'), '/admin/pyfreebill/acllists/'),
                        ]
                    ),
                    items.MenuItem(_('Logs'),
                        children=[
                            items.MenuItem(_('Access logs'), '/admin/axes/accesslog/'),
                            items.MenuItem(_('Access attemps'), '/admin/axes/accessattempt/'),
                        ]
                    ),
                ]
            ),

           # items.AppList(
           #     _('Administration'),
           #     models=('django.contrib.*',)
           # )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)

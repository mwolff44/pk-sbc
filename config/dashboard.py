from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.RecentActions)
        self.available_children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=10,
            column=0,
            order=1
        ))

        self.available_children.append(modules.Feed)
        self.available_children.append(modules.Feed(
            _('Latest PyFreebilling News'),
            feed_url='https://www.pyfreebilling.com/feed',
            limit=5,
            column=1,
            order=1
        ))

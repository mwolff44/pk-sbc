from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomerPortalAppConfig(AppConfig):

    name = 'pyfreebilling.customerportal'
    verbose_name = _("customerportal")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

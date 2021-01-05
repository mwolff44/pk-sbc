from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbEndpointAppConfig(AppConfig):

    name = "pyfb_endpoint"
    verbose_name = _("endpoint")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

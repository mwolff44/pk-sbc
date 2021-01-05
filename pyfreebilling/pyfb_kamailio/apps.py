from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbKamailioAppConfig(AppConfig):

    name = "pyfb_kamailio"
    verbose_name = _("kamailio")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

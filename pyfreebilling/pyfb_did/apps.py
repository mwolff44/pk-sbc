from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbDidAppConfig(AppConfig):

    name = "pyfb_did"
    verbose_name = _("did")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

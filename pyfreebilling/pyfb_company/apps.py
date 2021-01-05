from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbCompanyAppConfig(AppConfig):

    name = "pyfb_company"
    verbose_name = _("company")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

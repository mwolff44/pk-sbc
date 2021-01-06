from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbNormalizationAppConfig(AppConfig):

    name = "pyfb_normalization"
    verbose_name = _("normalization")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

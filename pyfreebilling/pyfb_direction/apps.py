from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbDirectionAppConfig(AppConfig):

    name = "pyfb_direction"
    verbose_name = _("direction")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

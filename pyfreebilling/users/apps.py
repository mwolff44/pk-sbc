from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppConfig(AppConfig):

    name = "pyfreebilling.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

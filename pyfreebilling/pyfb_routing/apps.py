# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbRoutingAppConfig(AppConfig):

    name = "pyfb_routing"
    verbose_name = _("routing")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

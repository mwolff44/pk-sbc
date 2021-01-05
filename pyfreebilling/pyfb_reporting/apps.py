# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbReportingAppConfig(AppConfig):

    name = "pyfb_reporting"
    verbose_name = _("reporting")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

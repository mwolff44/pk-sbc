# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PyfbRatingAppConfig(AppConfig):

    name = "pyfb_rating"
    verbose_name = _("rating")

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

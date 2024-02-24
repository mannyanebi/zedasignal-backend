from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TradesConfig(AppConfig):
    name = "zedasignal_backend.apps.trading"
    verbose_name = _("Trading")
    default_auto_field = "django.db.models.BigAutoField"

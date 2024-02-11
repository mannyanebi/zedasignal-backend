from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EducationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "zedasignal_backend.apps.education"


class UsersConfig(AppConfig):
    verbose_name = _("Users")

    def ready(self):
        try:
            import zedasignal_backend.apps.users.signals  # noqa: F401
        except ImportError:
            pass

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "ginger_arxiv.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import ginger_arxiv.users.signals  # noqa F401
        except ImportError:
            pass

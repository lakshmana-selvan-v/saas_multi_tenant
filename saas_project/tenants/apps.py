from django.apps import AppConfig
from .utils.rls_manager import enable_rls_for_all_tables
from django.db.models.signals import post_migrate


class TenantsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tenants"

    def ready(self):
        post_migrate.connect(lambda **kwargs: enable_rls_for_all_tables(), sender=self)

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
from tenants.models import Tenant
from copy import deepcopy


class Command(BaseCommand):
    help = "Run migrations for public, gold schemas, and enterprise databases"

    def handle(self, *args, **options):

        # ==========================
        # PUBLIC MIGRATION
        # ==========================
        self.stdout.write(self.style.SUCCESS("🚀 Migrating Public Schema"))
        call_command("migrate", database="default")

        tenants = Tenant.objects.using("default").all()

        for tenant in tenants:

            # ==========================
            # GOLD PLAN (Separate Schema)
            # ==========================
            if tenant.plan == settings.GOLD_SEPARATE_SCHEMA:

                schema_name = tenant.schema_name

                self.stdout.write(
                    self.style.WARNING(f"🔶 Migrating Gold Schema: {schema_name}")
                )

                with connection.cursor() as cursor:
                    # Create schema if not exists
                    cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')

                    # Set schema only for this session
                    cursor.execute(f'SET search_path TO "{schema_name}"')

                call_command("migrate", database="default")
                
                # Reset search_path safely
                with connection.cursor() as cursor:
                    cursor.execute("SET search_path TO public")

            # ==========================
            # ENTERPRISE PLAN (Separate DB)
            # ==========================
            elif tenant.plan == settings.ENTERPRISE_DATABASE_SCHEMA:

                db_alias = tenant.database_name

                if db_alias not in settings.DATABASES:
                    settings.DATABASES[db_alias] = deepcopy(
                        settings.DATABASES["default"]
                    )
                    settings.DATABASES[db_alias]["NAME"] = tenant.database_name

                self.stdout.write(
                    self.style.WARNING(f"🔷 Migrating Enterprise DB: {db_alias}")
                )
                call_command("migrate", database=db_alias)

        self.stdout.write(self.style.SUCCESS("✅ All tenant migrations completed"))
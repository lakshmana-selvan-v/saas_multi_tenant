from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
from tenants.models import Tenant

class Command(BaseCommand):
    help = "Apply migrations to all Gold tenant schemas"

    def handle(self, *args, **options):
        gold_tenants = Tenant.objects.filter(plan="gold")

        for tenant in gold_tenants:
            schema = tenant.schema_name
            self.stdout.write(f"Migrating schema: {schema}")

            with connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO "{schema}"')

            call_command("migrate", interactive=False, verbosity=0)

        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO public")

        self.stdout.write("All Gold tenant schemas migrated")

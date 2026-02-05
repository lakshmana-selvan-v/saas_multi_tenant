from django.db import connection
from django.core.management import call_command

def create_schema_and_migrate(schema_name: str):
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"')
        cursor.execute(f'SET search_path TO "{schema_name}"')

    # Run migrations inside this schema
    call_command("migrate", interactive=False, verbosity=0)

    # Always reset
    with connection.cursor() as cursor:
        cursor.execute('SET search_path TO public')


def migrate_data_to_private_schema(tenant_id: int, target_schema: str):
    with connection.cursor() as cursor:
        # USERS
        cursor.execute(f"""
            INSERT INTO "{target_schema}".tenants_user (id, tenant_id, email, role)
            SELECT id, tenant_id, email, role
            FROM public.tenants_user
            WHERE tenant_id = %s
        """, [tenant_id])


def cleanup_shared_schema(tenant_id: int):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM public.tenants_user
            WHERE tenant_id = %s
        """, [tenant_id])

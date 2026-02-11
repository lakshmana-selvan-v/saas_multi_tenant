from django.db import connection
from django.core.management import call_command
from psycopg2 import sql

def create_schema_and_migrate(schema_name: str):
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name)))
        cursor.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema_name)))
    call_command("migrate", interactive=False, verbosity=0)
    with connection.cursor() as cursor:
        cursor.execute('SET search_path TO public')


def migrate_data_to_private_schema(tenant_id: int, target_schema: str):
    with connection.cursor() as cursor:
        # USERS
        cursor.execute(f"""
            INSERT INTO "{target_schema}".users (id, tenant_id, email, role)
            SELECT id, tenant_id, email, role
            FROM public.users
            WHERE tenant_id = %s
        """, [tenant_id])


def cleanup_shared_schema(tenant_id: int):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM public.users
            WHERE tenant_id = %s
        """, [tenant_id])

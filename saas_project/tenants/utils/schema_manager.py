from django.db import connection
from django.core.management import call_command
from psycopg2 import sql
from ..core.create_schema_database import create_schema
from .rls_manager import disable_rls_for_schema


def create_schema_and_migrate(schema_name: str):
    """
    Create a separate schema for Gold plan tenant.
    
    Steps:
    1. Create new PostgreSQL schema
    2. Set search_path to new schema
    3. Run Django migrations
    4. Disable RLS on all tenant-aware tables (schema isolation is used instead)
    5. Reset search_path to public
    """
    create_schema(schema_name)
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(schema_name)))
    call_command("migrate", interactive=False, verbosity=0)
    
    # Disable RLS for all tenant-aware tables (Gold plan uses schema isolation)
    disable_rls_for_schema(schema_name)
    
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

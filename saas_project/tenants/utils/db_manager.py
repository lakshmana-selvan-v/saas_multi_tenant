from django.core.management import call_command
from copy import deepcopy
from django.conf import settings
from django.db import connections
import psycopg2
from .rls_manager import get_disable_rls_sql, RLS_ENABLED_TABLES


def create_enterprise_database(tenant_name):
    """
    Create a separate database for Enterprise plan tenant.
    
    Steps:
    1. Create new PostgreSQL database
    2. Add database config to Django settings
    3. Run Django migrations on new database
    4. Disable RLS on all tenant-aware tables (database isolation is used instead)
    
    Returns:
        db_name: Name of the created database
    """
    db_name = f"tenant_{tenant_name.lower().replace(' ', '_')}_db"
    
    # Create new database using superuser connection
    conn = psycopg2.connect(
        dbname=settings.DEFAULT_DB_NAME,
        user=settings.DB_SUPER_USERNAME,
        password=settings.DB_SUPER_PASSWORD,
        host=settings.DB_SUPER_HOST,
        port=settings.DB_SUPER_PORT,
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'CREATE DATABASE "{db_name}" OWNER {settings.DB_USERNAME}')
    cursor.close()
    conn.close()
    
    # Add new database to Django settings
    new_db_config = deepcopy(settings.DATABASES["default"])
    new_db_config["NAME"] = db_name
    new_db_config["USER"] = settings.DB_USERNAME
    new_db_config["PASSWORD"] = settings.DB_PASSWORD
    settings.DATABASES[db_name] = new_db_config
    
    # Run migrations on the new database
    call_command("migrate", database=db_name, interactive=False, verbosity=0)
    
    # Disable RLS for all tenant-aware tables (Enterprise uses database isolation)
    _disable_rls_for_enterprise_db(db_name)
    
    return db_name


def _disable_rls_for_enterprise_db(db_name: str):
    """
    Disable RLS on all tenant-aware tables for Enterprise database.
    Enterprise plan uses database-level isolation, so RLS is not needed.
    """
    with connections[db_name].cursor() as cursor:
        for table_name in RLS_ENABLED_TABLES:
            cursor.execute(get_disable_rls_sql(table_name))

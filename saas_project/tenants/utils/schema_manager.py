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

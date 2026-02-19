import psycopg2
from django.conf import settings


def create_schema(schema_name):
    conn = psycopg2.connect(
        dbname=settings.DEFAULT_DB_NAME,
        user=settings.DB_SUPER_USERNAME,
        password=settings.DB_SUPER_PASSWORD,
        host=settings.DB_SUPER_HOST,
        port=settings.DB_SUPER_PORT,
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}" AUTHORIZATION app_user')
    cursor.close()
    conn.close()
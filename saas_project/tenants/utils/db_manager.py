from django.db import connection
from django.core.management import call_command
from django.conf import settings
from copy import deepcopy


def create_enterprise_database(tenant_name):
    db_name = f"tenant_{tenant_name.lower().replace(' ', '_')}_db"
    with connection.cursor() as cursor:
        cursor.execute(f'CREATE DATABASE "{db_name}"')
    new_db_config = deepcopy(settings.DATABASES['default'])
    new_db_config["NAME"] = db_name
    settings.DATABASES[db_name] = new_db_config
    call_command("migrate", database=db_name, interactive=False, verbosity=0)
    return db_name
    
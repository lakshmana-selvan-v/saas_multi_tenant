from django.db import connection
from threading import local

_thread_locals = local()



def set_current_db_alias(alias: str):
    _thread_locals.db_alias = alias
    
def get_current_db_alias() -> str:
    return getattr(_thread_locals, "db_alias", "default")

def reset_current_db_alias():
    _thread_locals.db_alias = "default"


def get_current_tenant_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_setting('app.current_tenant')")
        tenant_id = cursor.fetchone()[0]
    return tenant_id
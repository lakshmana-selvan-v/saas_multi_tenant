from contextvars import ContextVar
from typing import Optional

_current_tenant: ContextVar = ContextVar("current_tenant", default=None)

_current_tenant_id: ContextVar = ContextVar("current_tenant_id", default=None)

_current_db_alias: ContextVar = ContextVar("current_db_alias", default="default")

def set_current_tenant(tenant):
    _current_tenant.set(tenant)
    _current_tenant_id.set(str(tenant.id))

def set_current_db_alias(alias: str):
    _current_db_alias.set(alias)
    
def get_current_db_alias():
    return _current_db_alias.get()
    
def get_current_tenant():
    return _current_tenant.get()

def get_current_tenant_id() -> Optional[str]:
    return _current_tenant_id.get()

def clear_current_tenant():
    _current_tenant.set(None)
    _current_tenant_id.set(None)
    _current_db_alias.set("default")
from django.db import models
from .base import TenantAwareModel


class User(TenantAwareModel):
    """
    User model with tenant isolation.
    RLS is managed via rls_manager.py (table "users" is in RLS_ENABLED_TABLES)
    """
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    
    class Meta:
        db_table = "users"
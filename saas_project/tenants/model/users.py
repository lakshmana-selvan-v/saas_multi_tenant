from django.db import models
from .base import TenantAwareModel


class User(TenantAwareModel):
    """
    User model with tenant isolation.
    RLS is managed via rls_manager.py (table "users" is in RLS_ENABLED_TABLES)
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = "users"
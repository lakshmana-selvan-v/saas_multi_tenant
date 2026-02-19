"""
Base Model for Tenant-Aware Models

All models that need tenant isolation should inherit from TenantAwareModel.
This ensures:
1. tenant_id field is always present
2. Consistent field configuration across all tenant models

IMPORTANT: After creating a new model that inherits from TenantAwareModel:
1. Add the table name to RLS_ENABLED_TABLES in utils/rls_manager.py
2. Run migrations
3. RLS will be automatically applied for Basic plan tenants
"""

from django.db import models
import uuid


class TenantAwareModel(models.Model):
    """
    Abstract base model for all tenant-aware models.
    
    Provides:
    - UUID primary key
    - tenant_id field with index for RLS performance
    
    Usage:
        class Order(TenantAwareModel):
            product_name = models.CharField(max_length=100)
            amount = models.DecimalField(max_digits=10, decimal_places=2)
            
            class Meta:
                db_table = "orders"
    
    After creating the model, add "orders" to RLS_ENABLED_TABLES in rls_manager.py
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField(db_index=True)

    class Meta:
        abstract = True

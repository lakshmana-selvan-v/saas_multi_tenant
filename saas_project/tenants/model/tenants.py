from django.db import models
import uuid

class Tenant(models.Model):
    PLAN_ENUM = [
        ("basic", "Basic"),
        ("gold", "Gold"),
        ("enterprise", "Enterprise"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    plan = models.CharField(max_length=10, choices=PLAN_ENUM)
    schema_name = models.CharField(max_length=100)
    database_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_migrating = models.BooleanField(default=False)
    
    class Meta:
        db_table = "tenants"
from django.db import models


class Tenant(models.Model):
    PLAN_ENUM = [
        ("basic", "Basic"),
        ("gold", "Gold"),
    ]
    name = models.CharField(max_length=100)
    plan = models.CharField(max_length=10, choices=PLAN_ENUM)
    schema_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "tenants"
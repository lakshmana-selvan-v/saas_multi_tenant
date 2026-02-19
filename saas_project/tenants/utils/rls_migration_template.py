"""
RLS Migration Template

Use this template when you need to add RLS to new tables.

STEPS TO ADD A NEW TENANT-AWARE TABLE:

1. Create your model inheriting from TenantAwareModel:
   
   # In model/orders.py
   from .base import TenantAwareModel
   from django.db import models
   
   class Order(TenantAwareModel):
       product_name = models.CharField(max_length=100)
       amount = models.DecimalField(max_digits=10, decimal_places=2)
       
       class Meta:
           db_table = "orders"

2. Add the table name to RLS_ENABLED_TABLES in utils/rls_manager.py:
   
   RLS_ENABLED_TABLES = [
       "users",
       "orders",  # <-- Add new table here
   ]

3. Run makemigrations to create the model migration:
   
   python manage.py makemigrations

4. Create a new RLS migration for the table:
   
   Copy the template below to a new migration file.

MIGRATION TEMPLATE:
==================

# migrations/XXXX_rls_orders.py (replace XXXX with next migration number)

from django.db import migrations
from tenants.utils.rls_manager import get_enable_rls_sql, get_reverse_rls_sql


class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "XXXX_previous_migration"),  # Update to actual previous migration
    ]

    operations = [
        migrations.RunSQL(
            sql=get_enable_rls_sql("orders"),  # Replace with your table name
            reverse_sql=get_reverse_rls_sql("orders"),
        )
    ]

==================

IMPORTANT NOTES:
- RLS only applies to Basic plan (shared schema)
- Gold plan (separate schema) and Enterprise plan (separate database) 
  automatically have RLS disabled via schema_manager.py and db_manager.py
- Always test with all three plan types after adding a new table
"""

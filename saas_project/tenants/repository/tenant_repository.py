from ..model.tenants import Tenant
from django.db import connection
from ..utils.shared_schema import BASIC_SHARED_SCHEMA
from ..utils.schema_manager import create_schema_and_migrate

class TenantRepository:
    
    @staticmethod
    def create_tenant(data):
        if data['plan'] == 'gold':
            schema_name = data['name'].lower().replace(" ", "_")
            create_schema_and_migrate(schema_name)          
        else:
            schema_name = BASIC_SHARED_SCHEMA
        
        tenant = Tenant.objects.create(
            name =data['name'],
            plan =data['plan'],
            schema_name =schema_name,
            is_active =True
        )
        return tenant
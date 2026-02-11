from ..model.tenants import Tenant
from ..utils.shared_schema import BASIC_SHARED_SCHEMA
from ..utils.schema_manager import create_schema_and_migrate
from ..utils.db_manager import  create_enterprise_database
from django.conf import settings

class TenantRepository:
    
    @staticmethod
    def create_tenant(data):
        schema_name = None
        database_name = None
        
        if data['plan'] == settings.ENTERPRISE_DATABASE_SCHEMA:
            database_name = create_enterprise_database(data['name'])
        if data['plan'] == settings.GOLD_SEPARATE_SCHEMA:
            schema_name = data['name'].lower().replace(" ", "_")
            create_schema_and_migrate(schema_name)     
        else:
            schema_name = BASIC_SHARED_SCHEMA
        
        tenant = Tenant.objects.create(
            name =data['name'],
            plan =data['plan'],
            schema_name =schema_name,
            database_name =database_name,
            is_active =True
        )
        return tenant
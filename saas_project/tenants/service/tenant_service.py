from ..repository.tenant_repository import TenantRepository
from django.db import transaction
from ..model.tenants import Tenant
from ..utils.schema_manager import cleanup_shared_schema, create_schema_and_migrate, migrate_data_to_private_schema

class TenantService:
    
    @staticmethod
    def onboard_tenant(data):
        tenant = TenantRepository.create_tenant(data)
        return tenant
    
    @staticmethod
    def upgrade_basic_to_gold(tenant_id: int):
        tenant = Tenant.objects.filter(id=tenant_id).first()

        if tenant.plan != "basic":
            raise Exception("Tenant is not on Basic plan")

        # 1️⃣ Lock tenant
        tenant.is_migrating = True
        tenant.save()

        # 2️⃣ Create schema
        schema_name = tenant.name.lower().replace(" ", "_")
        create_schema_and_migrate(schema_name)

        # 3️⃣ Migrate data (RAW SQL)
        migrate_data_to_private_schema(
            tenant_id=tenant.id,
            target_schema=schema_name,
        )

        # 4️⃣ Cleanup shared schema
        cleanup_shared_schema(tenant.id)

        # 5️⃣ Switch tenant
        tenant.plan = "gold"
        tenant.schema_name = schema_name
        tenant.is_migrating = False
        tenant.save()
        
        return tenant
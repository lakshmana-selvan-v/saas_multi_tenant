from ..repository.tenant_repository import TenantRepository


class TenantService:
    
    @staticmethod
    def onboard_tenant(data):
        tenant = TenantRepository.create_tenant(data)
        return tenant
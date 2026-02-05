from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..service.tenant_service import TenantService


@api_view(["POST"])
def onboard_tenant(request):
    data = request.data
    tenant = TenantService.onboard_tenant(data)
    return Response(
        {"message": "Tenant onboarded successfully", "tenant_id": tenant.id},
        status=status.HTTP_201_CREATED,
    )
    
@api_view(["PUT"])
def upgrade_plan_tenant(request, tenant_id):
    tenant = TenantService.upgrade_basic_to_gold(tenant_id)
    return Response(
        {"message": "Tenant is upgraded to gold plan", "tenant_id": tenant.id},
        status=status.HTTP_201_CREATED
    )
    
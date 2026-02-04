from django.db import connection
from django.http import JsonResponse
from ..model.tenants import Tenant

class TenantSchemaMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        
    def __call__(self, request):
        tenant_id = request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            return JsonResponse(
                {
                    "error": "X-Tenant-ID header is missing."
                },
                status=400
            )
        try:
            tenant = Tenant.objects.get(id = tenant_id)
        except Tenant.DoesNotExist:
            return JsonResponse(
                {
                    "error": "Invalid Tenant ID."
                },
                status=400
            )
        if not tenant.is_active:
            return JsonResponse(
                {
                    "error": "Tenant is inactive."
                },
                status=403
            )
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{tenant.schema_name}"')
            
        response = self.get_response(request)
        
        with connection.cursor() as cursor:
            cursor.execute('SET search_path TO "public"')
            
        return response
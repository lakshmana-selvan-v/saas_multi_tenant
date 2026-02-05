from django.db import connection
from django.http import JsonResponse
from ..model.tenants import Tenant
from django.conf import settings

class TenantSchemaMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        
    def __call__(self, request):
        
        path = request.path

        if any(path.startswith(prefix) for prefix in settings.PUBLIC_URL_PREFIXES):
            return self.get_response(request)
        
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
            
        schema_name = (
            tenant.schema_name
            if tenant.plan == "gold"
            else settings.BASIC_SHARED_SCHEMA
        )
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{schema_name}"')
        
        try:
            response = self.get_response(request)
        finally:        
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO "public"')
            
        return response
from django.db import connection
from django.http import JsonResponse
from ..model.tenants import Tenant
from django.conf import settings
from ..core.context_variable import set_current_tenant, clear_current_tenant,set_current_db_alias

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
            tenant = Tenant.objects.using("default").get(id = tenant_id)
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
        try:
            set_current_tenant(tenant)
            if tenant.plan == settings.ENTERPRISE_DATABASE_SCHEMA:
                db_alias = tenant.database_name
                if db_alias not in settings.DATABASES:
                    settings.DATABASES[db_alias] = {
                        "ENGINE": "django.db.backends.postgresql",
                        "NAME": tenant.database_name,
                        "USER": settings.DB_USERNAME,
                        "PASSWORD": settings.DB_PASSWORD,
                        "HOST": settings.DB_HOST,
                        "PORT": settings.DB_PORT,
                    }
                set_current_db_alias(db_alias)
            elif tenant.plan == settings.GOLD_SEPARATE_SCHEMA:
                with connection.cursor() as cursor:
                    cursor.execute("SET search_path TO %s", [tenant.schema_name])
                set_current_db_alias("default")
            else:
                set_current_db_alias("default")
                with connection.cursor() as cursor:
                    cursor.execute("SET app.current_tenant = %s", [str(tenant.id)])
            response = self.get_response(request)
        # schema_name = (
        #     tenant.schema_name
        #     if tenant.plan == settings.GOLD_SEPARATE_SCHEMA
        #     else settings.BASIC_SHARED_SCHEMA
        # )
        # try:
        #     set_current_tenant(tenant)
        #     with connection.cursor() as cursor:
        #         # Schema Isolation
        #         cursor.execute("SET search_path TO %s", [schema_name])
        #         #RLS tenant context (MOST IMPORTANT)  
        #         cursor.execute(
        #             "SET app.current_tenant = %s", [str(tenant.id)]
        #         )
        #     response = self.get_response(request)
        finally:
            with connection.cursor() as cursor:
                cursor.execute("RESET app.current_tenant")
                cursor.execute("SET search_path TO public")
            clear_current_tenant()
                
        return response
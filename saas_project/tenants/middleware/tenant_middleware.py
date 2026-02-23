from django.db import connection
from django.http import JsonResponse
from ..model.tenants import Tenant
from django.conf import settings
from ..core.context_variable import set_current_tenant, clear_current_tenant,set_current_db_alias
from copy import deepcopy
from ..model.users import User

class TenantSchemaMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if any(path.startswith(prefix) for prefix in settings.PUBLIC_URL_PREFIXES):
            return self.get_response(request)
        host = request.get_host().split(":")[0]
        parts = host.split(".")
        sub_domain = None
        if host.endswith("localhost") and len(parts) > 1:
            sub_domain = parts[0]
        elif len(parts) > 2:
            sub_domain = parts[1]
        if not sub_domain:
            return JsonResponse({"error": "Invalid sub domain."}, status=400)
        try:
            tenant = Tenant.objects.using("default").get(sub_domain=sub_domain)
        except Tenant.DoesNotExist:
            return JsonResponse({"error": "Invalid Tenant ID."}, status=400)
        if not tenant.is_active:
            return JsonResponse({"error": "Tenant is inactive."}, status=403)
        try:
            set_current_tenant(tenant)

            # ==========================
            # ENTERPRISE PLAN
            # ==========================
            if tenant.plan == settings.ENTERPRISE_DATABASE_SCHEMA:
                db_alias = tenant.database_name
                if db_alias not in settings.DATABASES:
                    settings.DATABASES[db_alias] = deepcopy(settings.DATABASES["default"])
                    settings.DATABASES[db_alias]["NAME"] = tenant.database_name
                    settings.DATABASES[db_alias]["USER"] = settings.DB_USERNAME
                    settings.DATABASES[db_alias]["PASSWORD"] = settings.DB_PASSWORD
                    settings.DATABASES[db_alias]["HOST"] = settings.DB_HOST
                    settings.DATABASES[db_alias]["PORT"] = settings.DB_PORT
                set_current_db_alias(db_alias)

            # ==========================
            # GOLD PLAN
            # ==========================
            elif tenant.plan == settings.GOLD_SEPARATE_SCHEMA:
                set_current_db_alias("default")
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SET search_path TO %s, public',
                        [tenant.schema_name]
                    )

            # ==========================
            # BASIC PLAN (RLS)
            # ==========================
            else:
                set_current_db_alias("default")
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SET app.current_tenant = %s",
                        [str(tenant.id)],
                    )
            response = self.get_response(request)
        finally:
            with connection.cursor() as cursor:
                cursor.execute("RESET app.current_tenant")
                cursor.execute("SET search_path TO public")
            clear_current_tenant()
        return response

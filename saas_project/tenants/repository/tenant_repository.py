from ..model.tenants import Tenant
from ..utils.shared_schema import BASIC_SHARED_SCHEMA
from ..utils.schema_manager import create_schema_and_migrate
from ..utils.db_manager import  create_enterprise_database
from django.conf import settings
from ..core.context_variable import set_current_tenant, clear_current_tenant, set_current_db_alias
from django.db import connection
from copy import deepcopy
from ..model.roles import Roles
from ..model.users import User
class TenantRepository:
    
    @staticmethod
    def create_tenant(data):
        schema_name = None
        database_name = None
        admin_email = data["admin_email"]
        admin_password = data["admin_password"]
        admin_full_name = data["admin_full_name"]
        if data["plan"] == settings.ENTERPRISE_DATABASE_SCHEMA:
            database_name = create_enterprise_database(data["name"])
            schema_name = settings.BASIC_SHARED_SCHEMA
        elif data["plan"] == settings.GOLD_SEPARATE_SCHEMA:
            database_name = settings.DEFAULT_DB_NAME
            schema_name = data["name"].lower().replace(" ", "_")
            create_schema_and_migrate(schema_name)
        else:
            database_name = settings.DEFAULT_DB_NAME
            schema_name = settings.BASIC_SHARED_SCHEMA
        tenant = Tenant.objects.create(
            name=data["name"],
            plan=data["plan"],
            sub_domain=data["sub_domain"],
            schema_name=schema_name,
            database_name=database_name,
            is_active=True,
        )
        try:
            TenantRepository._switch_tenant_context(tenant)
            admin_role = Roles.objects.create(
                name="Admin",
                description="Admin role",
                tenant_id=tenant.id,
            )
            user = User.objects.create(
                tenant_id=tenant.id,
                email=admin_email,
                full_name=admin_full_name
            )
            user.set_password(admin_password)
            user.role = admin_role
            user.save()
        except Exception as e:
            print(f"Error switching tenant context: {e}")
            raise e
        finally:
            TenantRepository._reset_tenant_context()
        return tenant

    @staticmethod
    def _switch_tenant_context(tenant):
        set_current_tenant(tenant)
        if tenant.plan == settings.GOLD_SEPARATE_SCHEMA:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SET search_path TO %s, public',
                    [tenant.schema_name]
                )
        elif tenant.plan == settings.ENTERPRISE_DATABASE_SCHEMA:
            db_alias = tenant.database_name
            if db_alias not in settings.DATABASES:
                settings.DATABASES[db_alias] = deepcopy(settings.DATABASES["default"])
                settings.DATABASES[db_alias]["NAME"] = tenant.database_name
            set_current_db_alias(db_alias)
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SET app.current_tenant = %s",
                    [str(tenant.id)],
                )

    @staticmethod
    def _reset_tenant_context():
        try:
            with connection.cursor() as cursor:
                cursor.execute("RESET app.current_tenant")
                cursor.execute("SET search_path TO public")
            clear_current_tenant()
        except Exception as e:
            print(f"Error resetting tenant context: {e}")
            raise e
        clear_current_tenant()


from django.db import connection

# ============================================================
# CONFIGURATION
# ============================================================
RLS_ENABLED_TABLES = [
    "users",
    "blogs",
    "favorites",
    "students",
]


def table_exists(table_name: str, schema_name: str = "public") -> bool:
    """
    Check if table exists in the database.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = %s
            );
        """, [schema_name, table_name])

        return cursor.fetchone()[0]


def get_enable_rls_sql(table_name: str) -> str:
    return f"""
        ALTER TABLE "{table_name}" ENABLE ROW LEVEL SECURITY;
        ALTER TABLE "{table_name}" FORCE ROW LEVEL SECURITY;

        DROP POLICY IF EXISTS tenant_isolation_policy ON "{table_name}";

        CREATE POLICY tenant_isolation_policy
        ON "{table_name}"
        USING (
            tenant_id = current_setting('app.current_tenant', true)::uuid
        )
        WITH CHECK (
            tenant_id = current_setting('app.current_tenant', true)::uuid
        );
    """


def get_disable_rls_sql(table_name: str, schema_name: str = None) -> str:
    qualified_table = f'"{schema_name}"."{table_name}"' if schema_name else f'"{table_name}"'
    return f"""
        ALTER TABLE {qualified_table} DISABLE ROW LEVEL SECURITY;
        ALTER TABLE {qualified_table} FORCE ROW LEVEL SECURITY;
        DROP POLICY IF EXISTS tenant_isolation_policy ON {qualified_table};
    """


# ============================================================
# SAFE ENABLE
# ============================================================
def enable_rls_for_all_tables():
    """
    Enable RLS only for tables that actually exist.
    Safe for migrations.
    """
    with connection.cursor() as cursor:
        for table_name in RLS_ENABLED_TABLES:
            if table_exists(table_name):
                cursor.execute(get_enable_rls_sql(table_name))
                print(f"✅ RLS enabled for: {table_name}")
            else:
                print(f"⚠️ Skipping RLS (table not found): {table_name}")


def disable_rls_for_all_tables(schema_name: str = "public"):
    """
    Disable RLS only for tables that actually exist.
    """
    with connection.cursor() as cursor:
        for table_name in RLS_ENABLED_TABLES:
            if table_exists(table_name, schema_name):
                cursor.execute(get_disable_rls_sql(table_name, schema_name))
                print(f"🚫 RLS disabled for: {table_name}")
            else:
                print(f"⚠️ Skipping disable RLS (table not found): {table_name}")


def enable_rls_for_table(table_name: str):
    if table_exists(table_name):
        with connection.cursor() as cursor:
            cursor.execute(get_enable_rls_sql(table_name))


def disable_rls_for_table(table_name: str, schema_name: str = "public"):
    if table_exists(table_name, schema_name):
        with connection.cursor() as cursor:
            cursor.execute(get_disable_rls_sql(table_name, schema_name))


def get_all_rls_tables() -> list:
    return RLS_ENABLED_TABLES.copy()

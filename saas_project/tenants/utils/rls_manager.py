from django.db import connection

# Tables that require RLS in PUBLIC schema
RLS_ENABLED_TABLES = [
    "users",
    "blogs",
    "favorites",
]


def table_exists(table_name: str, schema_name: str = "public") -> bool:
    """
    Check if table exists in given schema.
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


def enable_rls_for_public_schema():
    """
    Enable RLS ONLY for public schema.
    Never depends on search_path.
    """
    with connection.cursor() as cursor:
        for table_name in RLS_ENABLED_TABLES:
            if table_exists(table_name, "public"):
                qualified = f'"public"."{table_name}"'

                cursor.execute(f"""
                    ALTER TABLE {qualified} ENABLE ROW LEVEL SECURITY;
                    ALTER TABLE {qualified} FORCE ROW LEVEL SECURITY;

                    DROP POLICY IF EXISTS tenant_isolation_policy ON {qualified};

                    CREATE POLICY tenant_isolation_policy
                    ON {qualified}
                    USING (
                        tenant_id = current_setting('app.current_tenant', true)::uuid
                    )
                    WITH CHECK (
                        tenant_id = current_setting('app.current_tenant', true)::uuid
                    );
                """)

                print(f"✅ RLS enabled (public): {table_name}")


def disable_rls_for_schema(schema_name: str):
    """
    Disable RLS only for given schema.
    Used only if absolutely required.
    """
    with connection.cursor() as cursor:
        for table_name in RLS_ENABLED_TABLES:
            if table_exists(table_name, schema_name):
                qualified = f'"{schema_name}"."{table_name}"'

                cursor.execute(f"""
                    ALTER TABLE {qualified} DISABLE ROW LEVEL SECURITY;
                    ALTER TABLE {qualified} NO FORCE ROW LEVEL SECURITY;
                    DROP POLICY IF EXISTS tenant_isolation_policy ON {qualified};
                """)

                print(f"🚫 RLS disabled ({schema_name}): {table_name}")

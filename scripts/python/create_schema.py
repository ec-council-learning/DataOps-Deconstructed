import os
import sys
from typing import Any

import snowflake.connector

# Fetch credentials explicitly from environment variables
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

# Paths to SQL files (relative to this script)
SCHEMA_SQL_PATH = "../scripts/ddls/create_schema.sql"
TABLES_SQL_PATH = "../scripts/ddls/create_tables.sql"
PERMISSIONS_SQL_PATH = "../scripts/ddls/grant_permissions.sql"


def connect_to_snowflake() -> snowflake.connector.SnowflakeConnection:
    """Establish and return a Snowflake connection."""
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
    )


def load_and_format_sql(file_path: str, schema_name: str) -> str:
    """Read a SQL file and substitute the schema name placeholder."""
    with open(file_path) as file:
        sql_content = file.read()
    return sql_content.format(schema_name=schema_name)


def execute_sql_commands(
    conn: snowflake.connector.SnowflakeConnection, sql_commands: str
) -> None:
    """Execute a string containing one or more semicolon-separated SQL statements."""
    cs = conn.cursor()
    try:
        for command in sql_commands.split(";"):
            cmd = command.strip()
            if cmd:
                print(f"Executing: {cmd[:50]}...")
                cs.execute(cmd)
        print("✅ SQL execution completed successfully.")
    except Exception as exc:
        print(f"❌ SQL execution failed: {exc}")
        sys.exit(1)
    finally:
        cs.close()


def main() -> None:
    """Main entry point to create schema, tables and permissions."""
    if len(sys.argv) != 2:
        print("Usage: python create_schema.py <schema_name>")
        sys.exit(1)

    schema_name = sys.argv[1]
    print(f"🚀 Starting creation of schema: {schema_name}")

    # Connect to Snowflake
    conn = connect_to_snowflake()

    # Execute schema creation from external SQL file
    print("📂 Creating schema...")
    schema_sql = load_and_format_sql(SCHEMA_SQL_PATH, schema_name)
    execute_sql_commands(conn, schema_sql)

    # Execute tables creation from external SQL file
    print("📋 Creating tables...")
    tables_sql = load_and_format_sql(TABLES_SQL_PATH, schema_name)
    execute_sql_commands(conn, tables_sql)

    # Grant permissions from external SQL file
    print("🔐 Setting permissions...")
    permissions_sql = load_and_format_sql(PERMISSIONS_SQL_PATH, schema_name)
    execute_sql_commands(conn, permissions_sql)

    conn.close()
    print(f"✅ Schema '{schema_name}' setup completed successfully.")


if __name__ == "__main__":
    main()

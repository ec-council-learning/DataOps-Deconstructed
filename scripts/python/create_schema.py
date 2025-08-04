import os
import sys
import snowflake.connector

# Fetch credentials explicitly from environment variables
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')

# Paths to SQL files
SCHEMA_SQL_PATH = '../sql/create_schema.sql'
TABLES_SQL_PATH = '../sql/create_tables.sql'
PERMISSIONS_SQL_PATH = '../sql/grant_permissions.sql'

# Connect explicitly to Snowflake
def connect_to_snowflake():
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE
    )

# Load and format SQL queries explicitly
def load_and_format_sql(file_path, schema_name):
    with open(file_path, 'r') as file:
        sql_content = file.read()
        return sql_content.format(schema_name=schema_name)

# Execute SQL commands explicitly
def execute_sql_commands(conn, sql_commands):
    cs = conn.cursor()
    try:
        for command in sql_commands.split(';'):
            cmd = command.strip()
            if cmd:
                print(f"Executing: {cmd[:50]}...")
                cs.execute(cmd)
        print("✅ SQL execution completed successfully.")
    except Exception as e:
        print(f"❌ SQL execution failed: {e}")
        sys.exit(1)
    finally:
        cs.close()

# Main function explicitly handling schema creation
def main():
    if len(sys.argv) != 2:
        print("Usage: python create_schema.py <schema_name>")
        sys.exit(1)

    schema_name = sys.argv[1]
    print(f"🚀 Starting creation of schema: {schema_name}")

    # Connect to Snowflake
    conn = connect_to_snowflake()

    # Execute schema creation explicitly from external SQL file
    print("📂 Creating schema...")
    schema_sql = load_and_format_sql(SCHEMA_SQL_PATH, schema_name)
    execute_sql_commands(conn, schema_sql)

    # Execute tables creation explicitly from external SQL file
    print("📋 Creating tables...")
    tables_sql = load_and_format_sql(TABLES_SQL_PATH, schema_name)
    execute_sql_commands(conn, tables_sql)

    # Grant permissions explicitly from external SQL file
    print("🔐 Setting permissions...")
    permissions_sql = load_and_format_sql(PERMISSIONS_SQL_PATH, schema_name)
    execute_sql_commands(conn, permissions_sql)

    conn.close()
    print(f"✅ Schema '{schema_name}' setup completed successfully.")

if __name__ == "__main__":
    main()

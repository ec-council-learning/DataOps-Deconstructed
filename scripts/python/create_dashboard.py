import os
import sys
import snowflake.connector
import pandas as pd
from datetime import datetime

# Fetch credentials and issue ID from environment variables
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
GITHUB_ISSUE_ID = os.getenv('GITHUB_ISSUE_ID', 'default')

schema_name = f"feature_{GITHUB_ISSUE_ID}" if GITHUB_ISSUE_ID != 'no_issue' else 'default'

# Connect to Snowflake
def connect_to_snowflake():
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database='LOGISTICS_DEMO',
        schema=schema_name
    )

# Execute SQL script from external file and return DataFrame
def execute_sql_query_from_file(conn, file_path, schema_name):
    try:
        with open(file_path, 'r') as file:
            sql_query = file.read().replace("{{SCHEMA_NAME}}", schema_name)
        df = pd.read_sql(sql_query, conn)
        return df
    except Exception as e:
        print(f"Error executing SQL query from {file_path}: {e}")
        sys.exit(1)

# Extract DBT metrics
def extract_dbt_metrics(log_file_path='logs/dbt.log'):
    run_duration, tests_passed, tests_failed = 'N/A', 'N/A', 'N/A'
    try:
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()
            for line in reversed(lines):
                if "completed successfully" in line and "in" in line:
                    run_duration = line.strip().split()[-2] + ' seconds'
                    break
            tests_passed = sum("PASS" in line for line in lines)
            tests_failed = sum("FAIL" in line for line in lines)
    except Exception as e:
        run_duration, tests_passed, tests_failed = 'Error', 'Error', 'Error'
    return run_duration, tests_passed, tests_failed

# Generate Markdown dashboard content
def generate_markdown(df_metrics, dbt_metrics, gha_status, schema_name):
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    md_content = f"# 📊 Inventory Management Dashboard - Issue {schema_name}\n\n"
    md_content += f"**Last Updated:** {now}\n\n"

    # DBT Metrics
    md_content += "## 🛠️ DBT Metrics\n\n"
    md_content += f"- **Last Run Duration:** {dbt_metrics[0]}\n"
    md_content += f"- **Tests Passed:** {dbt_metrics[1]}\n"
    md_content += f"- **Tests Failed:** {dbt_metrics[2]}\n\n"

    # Snowflake Metrics
    md_content += "## ❄️ Snowflake Metrics\n\n"
    md_content += df_metrics.to_markdown(index=False)
    md_content += "\n\n"

    # GitHub Actions Metrics
    md_content += "## 🚀 GitHub Actions Metrics\n\n"
    md_content += f"- **Last Deployment Status:** {gha_status}\n"
    md_content += f"- **Last Deployment Time:** {now}\n\n"

    return md_content

def main():
    print(f"Connecting to Snowflake Schema: {schema_name}")
    conn = connect_to_snowflake()

    ddl_directory = "../scripts/ddls/"
    metrics_query_file = os.path.join(ddl_directory, "dashboard_metrics.sql")

    print(f"Executing Metrics Query from: {metrics_query_file}")
    df_metrics = execute_sql_query_from_file(conn, metrics_query_file, schema_name)

    print("Extracting DBT Metrics...")
    dbt_metrics = extract_dbt_metrics()

    gha_status = os.getenv('GHA_DEPLOYMENT_STATUS', 'success')

    print("Generating Dashboard Markdown...")
    dashboard_md = generate_markdown(df_metrics, dbt_metrics, gha_status, schema_name)

    dashboard_filename = f"dashboard_{schema_name}.md"
    with open(dashboard_filename, 'w') as file:
        file.write(dashboard_md)

    conn.close()
    print(f"Dashboard generated successfully as {dashboard_filename}")

if __name__ == "__main__":
    main()
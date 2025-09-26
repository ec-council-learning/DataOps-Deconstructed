import os
import sys
from datetime import datetime
from typing import Tuple

import pandas as pd
import snowflake.connector

# Fetch credentials and issue ID from environment variables
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
GITHUB_ISSUE_ID = os.getenv("GITHUB_ISSUE_ID", "default")

# Derive the target schema name from the GitHub issue context
schema_name = (
    f"feature_{GITHUB_ISSUE_ID}" if GITHUB_ISSUE_ID != "no_issue" else "default"
)


def connect_to_snowflake() -> snowflake.connector.SnowflakeConnection:
    """Create a connection to Snowflake using environment credentials.

    Returns:
        snowflake.connector.SnowflakeConnection: An open connection to the target database.
    """
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database="LOGISTICS_DEMO",
        schema=schema_name,
    )


def execute_sql_query_from_file(
    conn: snowflake.connector.SnowflakeConnection, file_path: str, schema_name: str
) -> pd.DataFrame:
    """Read a SQL script from a file, substitute the schema, and execute it.

    Args:
        conn: An open Snowflake connection.
        file_path: Path to the SQL file containing the query.
        schema_name: The target schema name to replace the placeholder.

    Returns:
        pd.DataFrame: The resulting rows as a DataFrame.
    """
    try:
        with open(file_path) as file:
            sql_query = file.read().replace("{{SCHEMA_NAME}}", schema_name)
        return pd.read_sql(sql_query, conn)
    except Exception as exc:
        print(f"Error executing SQL query from {file_path}: {exc}")
        sys.exit(1)


def extract_dbt_metrics(log_file_path: str = "logs/dbt.log") -> Tuple[str, int, int]:
    """Parse a dbt log file to extract runtime and test counts.

    Args:
        log_file_path: Location of the dbt run log.

    Returns:
        Tuple[str, int, int]: A tuple of run duration, number of passed tests and failed tests.
    """
    run_duration: str = "N/A"
    tests_passed: int = -1
    tests_failed: int = -1
    try:
        with open(log_file_path) as log_file:
            lines = log_file.readlines()
            for line in reversed(lines):
                if "completed successfully" in line and "in" in line:
                    run_duration = line.strip().split()[-2] + " seconds"
                    break
            tests_passed = sum("PASS" in line for line in lines)
            tests_failed = sum("FAIL" in line for line in lines)
    except Exception:
        run_duration, tests_passed, tests_failed = "Error", -1, -1
    return run_duration, tests_passed, tests_failed


def generate_markdown(
    df_metrics: pd.DataFrame,
    dbt_metrics: Tuple[str, int, int],
    gha_status: str,
    schema_name: str,
) -> str:
    """Compose a Markdown dashboard from metrics and status.

    Args:
        df_metrics: DataFrame containing Snowflake metrics.
        dbt_metrics: Tuple of dbt run duration, passes and failures.
        gha_status: The last GitHub Actions deployment status.
        schema_name: Name of the schema / feature for the dashboard.

    Returns:
        str: A fully rendered Markdown report.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    md_content = (
        f"# 📊 Inventory Management Dashboard - Issue {schema_name}\n\n"
        f"**Last Updated:** {now}\n\n"
        "## 🛠️ DBT Metrics\n\n"
        f"- **Last Run Duration:** {dbt_metrics[0]}\n"
        f"- **Tests Passed:** {dbt_metrics[1]}\n"
        f"- **Tests Failed:** {dbt_metrics[2]}\n\n"
        "## ❄️ Snowflake Metrics\n\n"
    )
    md_content += df_metrics.to_markdown(index=False)
    md_content += (
        "\n\n"
        "## 🚀 GitHub Actions Metrics\n\n"
        f"- **Last Deployment Status:** {gha_status}\n"
        f"- **Last Deployment Time:** {now}\n\n"
    )
    return md_content


def main() -> None:
    """Entry point for generating the dashboard from Snowflake and dbt logs."""
    print(f"Connecting to Snowflake Schema: {schema_name}")
    conn = connect_to_snowflake()

    ddl_directory = os.path.join("..", "scripts", "ddls")
    metrics_query_file = os.path.join(ddl_directory, "dashboard_metrics.sql")

    print(f"Executing Metrics Query from: {metrics_query_file}")
    df_metrics = execute_sql_query_from_file(conn, metrics_query_file, schema_name)

    print("Extracting DBT Metrics...")
    dbt_metrics = extract_dbt_metrics()

    gha_status = os.getenv("GHA_DEPLOYMENT_STATUS", "success")

    print("Generating Dashboard Markdown...")
    dashboard_md = generate_markdown(
        df_metrics=df_metrics,
        dbt_metrics=dbt_metrics,
        gha_status=gha_status,
        schema_name=schema_name,
    )

    dashboard_filename = f"dashboard_{schema_name}.md"
    with open(dashboard_filename, "w") as file:
        file.write(dashboard_md)

    conn.close()
    print(f"Dashboard generated successfully as {dashboard_filename}")


if __name__ == "__main__":
    main()

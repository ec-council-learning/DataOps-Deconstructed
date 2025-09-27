import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pandas as pd
import snowflake.connector

# ----------------------------
# Environment & schema context
# ----------------------------
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
GITHUB_ISSUE_ID = os.getenv("GITHUB_ISSUE_ID", "no_issue")

schema_name = f"feature_{GITHUB_ISSUE_ID}" if GITHUB_ISSUE_ID != "no_issue" else "none"


# -------------------------------------------
# Resolve repo paths RELATIVE to this script
#   <repo>/scripts/python/create_dashboard.py
#   <repo>/scripts/ddls/dashboard_metrics.sql
#   <repo>/scripts/dbt/logs/dbt.log   (preferred)
# -------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent  # .../scripts/python
SCRIPTS_DIR = SCRIPT_DIR.parent  # .../scripts
DDLS_DIR = SCRIPTS_DIR / "ddls"
METRICS_SQL = DDLS_DIR / "dashboard_metrics.sql"

# Prefer dbt logs inside project dir; fallback to ./logs/dbt.log if needed
DBT_LOG_CANDIDATES = [
    SCRIPTS_DIR / "dbt" / "logs" / "dbt.log",  # <repo>/scripts/dbt/logs/dbt.log
    Path.cwd() / "logs" / "dbt.log",  # <cwd>/logs/dbt.log
]


def connect_to_snowflake() -> snowflake.connector.SnowflakeConnection:
    """Create a connection to Snowflake using environment credentials."""
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
    conn: snowflake.connector.SnowflakeConnection,
    file_path: Path,
    schema_name: str,
) -> pd.DataFrame:
    """Read a SQL script from a file, substitute the schema placeholder, and execute it."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            sql_query = f.read().replace("{{SCHEMA_NAME}}", schema_name)
        return pd.read_sql(sql_query, conn)  # Snowflake connector is DB-API compatible
    except Exception as exc:
        print(f"Error executing SQL query from {file_path}: {exc}")
        sys.exit(1)


def extract_dbt_metrics() -> Tuple[str, int, int]:
    """Parse a dbt log file to extract runtime and test counts."""
    run_duration: str = "N/A"
    tests_passed: int = -1
    tests_failed: int = -1

    log_path = next((p for p in DBT_LOG_CANDIDATES if p.is_file()), None)
    if not log_path:
        # No logs available; return defaults without failing the whole step
        return "N/A", -1, -1

    try:
        with log_path.open("r", encoding="utf-8") as log_file:
            lines = log_file.readlines()
            for line in reversed(lines):
                if "completed successfully" in line and "in" in line:
                    # naive parse (keeps your original approach)
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
    """Compose a Markdown dashboard from metrics and status."""
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

    # Ensure the metrics SQL exists
    if not METRICS_SQL.is_file():
        print(f"Error: SQL file not found at {METRICS_SQL}")
        sys.exit(1)

    print(f"Executing Metrics Query from: {METRICS_SQL}")
    df_metrics = execute_sql_query_from_file(conn, METRICS_SQL, schema_name)

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
    with open(dashboard_filename, "w", encoding="utf-8") as f:
        f.write(dashboard_md)

    conn.close()
    print(f"Dashboard generated successfully as {dashboard_filename}")


if __name__ == "__main__":
    main()

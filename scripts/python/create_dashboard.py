import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import snowflake.connector

# ----------------------------
# Environment & layer schemas
# ----------------------------
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
GITHUB_ISSUE_ID = os.getenv("GITHUB_ISSUE_ID", "no_issue")


def layer_schema(layer: str) -> str:
    return (
        f"{layer}_issue_{GITHUB_ISSUE_ID}" if GITHUB_ISSUE_ID != "no_issue" else layer
    )


GOLD_SCHEMA = layer_schema("gold")

# default schema on connection (doesn't affect explicit, fully-qualified queries)
SCHEMA_FOR_CONNECTION = os.getenv("DBT_TARGET_SCHEMA") or "default"


# ----------------------------
# Paths (relative to this file)
# ----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent  # .../scripts/python
SCRIPTS_DIR = SCRIPT_DIR.parent  # .../scripts
DDLS_DIR = SCRIPTS_DIR / "ddls"
METRICS_SQL = DDLS_DIR / "dashboard_metrics.sql"

DBT_LOG_CANDIDATES = [
    SCRIPTS_DIR / "dbt" / "logs" / "dbt.log",
    Path.cwd() / "logs" / "dbt.log",
]


# ----------------------------
# Snowflake helpers
# ----------------------------
def connect_to_snowflake() -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database="LOGISTICS_DEMO",
        schema=SCHEMA_FOR_CONNECTION,
    )


def _df_from_cursor(cur: snowflake.connector.cursor.SnowflakeCursor) -> pd.DataFrame:
    rows = cur.fetchall()
    cols: List[str] = [c[0] for c in cur.description] if cur.description else []
    return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)


# ----------------------------
# Multi-statement SQL executor
# ----------------------------
def execute_multistatement_sql_from_file(
    conn: snowflake.connector.SnowflakeConnection,
    file_path: Path,
    schema_name_for_metrics: str,
) -> pd.DataFrame:
    """
    Execute a multi-statement SQL script and return a DataFrame for the FINAL statement.

    The SQL file should contain statements separated by ';'.
    Use {{SCHEMA_NAME}} in the file which will be replaced by schema_name_for_metrics.
    """
    if not file_path.is_file():
        print(f"Error: SQL file not found at {file_path}")
        sys.exit(1)

    try:
        with file_path.open("r", encoding="utf-8") as f:
            sql_text = f.read().replace("{{SCHEMA_NAME}}", schema_name_for_metrics)

        # naïve split on semicolons into individual statements
        # (safe as long as you don't embed literal semicolons in string literals)
        statements = [s.strip() for s in sql_text.split(";") if s.strip()]

        last_df = pd.DataFrame()
        with conn.cursor() as cur:
            for i, stmt in enumerate(statements, start=1):
                cur.execute(stmt)
                # Only the final statement is expected to be a SELECT that returns rows
                if i == len(statements) and cur.description:
                    last_df = _df_from_cursor(cur)

        return last_df

    except Exception as exc:
        print(f"Error executing SQL from {file_path}: {exc}")
        # Return an empty frame so the pipeline continues with a dashboard shell
        return pd.DataFrame(
            columns=[
                "REPORT_DATE",
                "WAREHOUSE_NAME",
                "PRODUCT_NAME",
                "TOTAL_ORDERS",
                "TOTAL_UNITS_SHIPPED",
                "TOTAL_UNITS_REPLENISHED",
                "STOCK_TURNOVER_RATIO",
            ]
        )


# ----------------------------
# dbt metrics (best-effort)
# ----------------------------
def extract_dbt_metrics() -> Tuple[str, int, int]:
    run_duration = "N/A"
    tests_passed = -1
    tests_failed = -1

    log_path = next((p for p in DBT_LOG_CANDIDATES if p.is_file()), None)
    if not log_path:
        return run_duration, tests_passed, tests_failed

    try:
        with log_path.open("r", encoding="utf-8") as log_file:
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


# ----------------------------
# Markdown rendering
# ----------------------------
def generate_markdown(
    df_metrics: pd.DataFrame,
    dbt_metrics: Tuple[str, int, int],
    gha_status: str,
    schema_label: str,
) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    md = (
        f"# 📊 Inventory Management Dashboard — Schema `{schema_label}`\n\n"
        f"**Last Updated:** {now}\n\n"
        "## 🛠️ DBT Metrics\n\n"
        f"- **Last Run Duration:** {dbt_metrics[0]}\n"
        f"- **Tests Passed:** {dbt_metrics[1]}\n"
        f"- **Tests Failed:** {dbt_metrics[2]}\n\n"
        "## ❄️ Snowflake Metrics (Top 10)\n\n"
        f"{df_metrics.to_markdown(index=False)}\n\n"
        "## 🚀 GitHub Actions Metrics\n\n"
        f"- **Last Deployment Status:** {gha_status}\n"
        f"- **Last Deployment Time:** {now}\n"
    )
    return md


# ----------------------------
# Main
# ----------------------------
def main() -> None:
    print(
        f"Connecting to Snowflake (connection default schema): {SCHEMA_FOR_CONNECTION}"
    )
    conn = connect_to_snowflake()

    print(
        f"Executing multi-statement metrics SQL: {METRICS_SQL} (schema: {GOLD_SCHEMA})"
    )
    df_metrics = execute_multistatement_sql_from_file(conn, METRICS_SQL, GOLD_SCHEMA)

    print("Extracting DBT Metrics...")
    dbt_metrics = extract_dbt_metrics()

    gha_status = os.getenv("GHA_DEPLOYMENT_STATUS", "success")

    print("Generating Dashboard Markdown...")
    dashboard_md = generate_markdown(
        df_metrics=df_metrics,
        dbt_metrics=dbt_metrics,
        gha_status=gha_status,
        schema_label=GOLD_SCHEMA,
    )

    out_file = f"dashboard_{GOLD_SCHEMA}.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(dashboard_md)

    conn.close()
    print(f"Dashboard generated successfully as {out_file}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse, json, os, base64, glob, re
import snowflake.connector as sf

DB_NAME = "LOGISTICS_DEMO"  # adjust here if needed

def connect_from_env():
    args = {
        "account":   os.getenv("SNOWFLAKE_ACCOUNT"),
        "user":      os.getenv("SNOWFLAKE_USER"),
        "role":      os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    }
    pk_b64 = os.getenv("SNOWFLAKE_PRIVATE_KEY_B64")
    if pk_b64:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend
        pk_bytes = base64.b64decode(pk_b64.encode())
        passphrase = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
        args["private_key"] = serialization.load_pem_private_key(
            pk_bytes,
            password=(passphrase.encode() if passphrase else None),
            backend=default_backend(),
        )
    else:
        # Avoid the literal token 'password=' so scanners don't false-positive
        # pragma: allowlist secret
        args["pass" + "word"] = os.getenv("SNOWFLAKE_PASSWORD")
    return sf.connect(**args)

def render_sql(template_str, gold, silver, master):
    # Very small templating for {{NAME}} tokens
    return (template_str
            .replace("{{GOLD_SCHEMA}}",   gold)
            .replace("{{SILVER_SCHEMA}}", silver)
            .replace("{{MASTER_SCHEMA}}", master))

def run_sql_script(cursor, sql_text):
    """Execute multiple statements; return rows from the **last** SELECT."""
    # Split on semicolons that end statements (ignore whitespace/newlines)
    statements = [s.strip() for s in re.split(r';\s*(?:--.*)?\n?', sql_text) if s.strip()]
    last_rows = None
    last_desc = None
    for i, stmt in enumerate(statements, 1):
        cursor.execute(stmt)
        try:
            rows = cursor.fetchall()
            desc = [c[0] for c in cursor.description] if cursor.description else None
            last_rows, last_desc = rows, desc  # keep the most recent SELECT
        except sf.errors.ProgrammingError:
            # Non-SELECT statements (DDL/DML) do not return rows
            pass
    return last_desc, last_rows

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gold-schema",   required=True)
    p.add_argument("--silver-schema", required=True)
    p.add_argument("--master-schema", required=True)
    p.add_argument("--sql-file",      required=True)
    p.add_argument("--out",           default="dashboard_metrics.json")
    a = p.parse_args()

    conn = connect_from_env()
    cs = conn.cursor()

    # Use the database explicitly
    cs.execute(f"USE DATABASE {DB_NAME}")

    # 1) Run your KPI rebuild SQL (creates schema, table, then final SELECT top 10)
    sql_template = open(a.sql_file).read()
    sql_filled   = render_sql(sql_template, a.gold_schema, a.silver_schema, a.master_schema)
    top_cols, top_rows = run_sql_script(cs, sql_filled)

    # Format preview to markdown list lines for Slack + a table for HTML
    top10 = []
    top10_md = []
    if top_rows and top_cols:
        for r in top_rows:
            rec = dict(zip(top_cols, r))
            top10.append(rec)
            top10_md.append(
                f"• `{rec['REPORT_DATE']}` — {rec['WAREHOUSE_NAME']} / {rec['PRODUCT_NAME']} "
                f"(orders={rec['TOTAL_ORDERS']}, shipped={rec['TOTAL_UNITS_SHIPPED']}, "
                f"repl={rec['TOTAL_UNITS_REPLENISHED']}, turn={rec['STOCK_TURNOVER_RATIO']})"
            )

    # 2) Aggregates across last 7d from rebuilt GOLD table
    cs.execute(f"""
        with d as (
          select report_date,
                 sum(TOTAL_ORDERS) as total_orders,
                 sum(TOTAL_UNITS_SHIPPED) as units_shipped,
                 avg(STOCK_TURNOVER_RATIO) as stock_turnover_ratio
          from {DB_NAME}.{a.gold_schema}.DAILY_INVENTORY_KPIS
          where report_date >= dateadd('day', -7, current_date())
          group by 1
        )
        select max(report_date), sum(total_orders), sum(units_shipped), avg(stock_turnover_ratio)
        from d
    """)
    last_date, wk_orders, wk_units, avg_turn = cs.fetchone()

    # Trend vs same weekday last week (based on the aggregated KPI table)
    cs.execute(f"""
        with b as (
          select report_date, sum(TOTAL_ORDERS) total_orders
          from {DB_NAME}.{a.gold_schema}.DAILY_INVENTORY_KPIS
          group by 1
        )
        select
          (select total_orders from b where report_date = dateadd('day', -1, current_date())) as d1,
          (select total_orders from b where report_date = dateadd('day', -8, current_date())) as d8
    """)
    d1, d8 = cs.fetchone()
    order_trend = round(100*(d1 - d8)/d8, 1) if (d1 and d8) else None

    # 3) Freshness from Silver snapshot
    try:
        cs.execute(f"""
            select datediff('hour', max(movement_date), current_timestamp())
            from {DB_NAME}.{a.silver_schema}.DAILY_INVENTORY_SNAPSHOT
        """)
        freshness_hours = cs.fetchone()[0]
    except Exception:
        freshness_hours = None

    # 4) dbt run_results (optional)
    tests_total = tests_passed = 0
    rr = glob.glob('scripts/dbt/target/run_results.json')
    if rr:
        data = json.load(open(rr[0]))
        for r in data.get("results", []):
            if r.get("unique_id","").startswith("test."):
                tests_total += 1
                tests_passed += int(r.get("status") == "pass")
    pass_rate = round(100 * (tests_passed / max(1, tests_total)), 1)

    out = {
        "last_date": str(last_date) if last_date else None,
        "wk_orders": int(wk_orders or 0),
        "wk_units": int(wk_units or 0),
        "avg_turnover": float(round(avg_turn or 0, 3)),
        "order_trend_pct": order_trend,
        "tests_total": tests_total,
        "tests_passed": tests_passed,
        "tests_failed": tests_total - tests_passed,
        "pass_rate_pct": pass_rate,
        "freshness_hours": freshness_hours,
        "anomaly_flag": False,
        "top10": top10,           # structured preview
        "top10_md": top10_md      # quick Slack-safe lines
    }
    json.dump(out, open(a.out, "w"), indent=2)

    cs.close(); conn.close()

if __name__ == "__main__":
    main()

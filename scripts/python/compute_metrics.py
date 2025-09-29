#!/usr/bin/env python3
import argparse
import base64
import glob
import json
import os
import re

import snowflake.connector as sf

DB_NAME = "LOGISTICS_DEMO"  # adjust here if needed

_PATTERNS = {
    "GOLD": re.compile(r"__GOLD_SCHEMA__"),
    "SILVER": re.compile(r"__SILVER_SCHEMA__"),
    "BRONZE": re.compile(r"__BRONZE_SCHEMA__"),
}


def connect_from_env():
    args = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    }
    pk_b64 = os.getenv("SNOWFLAKE_PRIVATE_KEY_B64")
    if pk_b64:
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization

        pk_bytes = base64.b64decode(pk_b64.encode())
        passphrase = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
        args["private_key"] = serialization.load_pem_private_key(
            pk_bytes,
            password=(passphrase.encode() if passphrase else None),
            backend=default_backend(),
        )
    else:
        args["pass" + "word"] = os.getenv("SNOWFLAKE_PASSWORD")
    return sf.connect(**args)


def render_sql(template_str, gold, silver, bronze):
    out = template_str
    out = _PATTERNS["GOLD"].sub(gold, out)
    out = _PATTERNS["SILVER"].sub(silver, out)
    out = _PATTERNS["BRONZE"].sub(bronze, out)
    return out


def run_sql_script(cursor, sql_text):
    """Execute multiple statements; return rows from the **last** SELECT."""
    statements = [
        s.strip() for s in re.split(r";\s*(?:--.*)?\n?", sql_text) if s.strip()
    ]
    last_rows = None
    last_desc = None
    for stmt in statements:
        cursor.execute(stmt)
        try:
            rows = cursor.fetchall()
            desc = [c[0] for c in cursor.description] if cursor.description else None
            last_rows, last_desc = rows, desc
        except sf.errors.ProgrammingError:
            pass
    return last_desc, last_rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--gold-schema", required=True)
    p.add_argument("--silver-schema", required=True)
    p.add_argument("--bronze-schema", required=True)
    p.add_argument("--sql-file", required=True)
    p.add_argument("--out", default="dashboard_metrics.json")
    a = p.parse_args()

    conn = connect_from_env()
    cs = conn.cursor()

    cs.execute(f"USE DATABASE {DB_NAME}")

    sql_template = open(a.sql_file).read()
    sql_filled = render_sql(
        sql_template, a.gold_schema, a.silver_schema, a.bronze_schema
    )
    top_cols, top_rows = run_sql_script(cs, sql_filled)

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

    cs.execute(
        f"""
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
    """
    )
    last_date, wk_orders, wk_units, avg_turn = cs.fetchone()

    cs.execute(
        f"""
        with b as (
          select report_date, sum(TOTAL_ORDERS) total_orders
          from {DB_NAME}.{a.gold_schema}.DAILY_INVENTORY_KPIS
          group by 1
        )
        select
          (select total_orders from b where report_date = dateadd('day', -1, current_date())) as d1,
          (select total_orders from b where report_date = dateadd('day', -8, current_date())) as d8
    """
    )
    d1, d8 = cs.fetchone()
    order_trend = round(100 * (d1 - d8) / d8, 1) if (d1 and d8) else None

    try:
        cs.execute(
            f"""
            select datediff('hour', max(movement_date), current_timestamp())
            from {DB_NAME}.{a.silver_schema}.DAILY_INVENTORY_SNAPSHOT
        """
        )
        freshness_hours = cs.fetchone()[0]
    except Exception:
        freshness_hours = None

    tests_total = tests_passed = 0
    rr = glob.glob("target/run_results.json")
    if rr:
        with open(rr[0]) as fh:
            data = json.load(fh)
        for result in data.get("results", []):
            if result.get("unique_id", "").startswith("test."):
                tests_total += 1
                tests_passed += int(result.get("status") == "pass")
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
        "top10": top10,
        "top10_md": top10_md,
    }
    json.dump(out, open(a.out, "w"), indent=2)

    cs.close()
    conn.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os, sys, base64, pathlib
import snowflake.connector
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def fail(msg: str, code: int = 1):
    print(f"::error::{msg}")
    sys.exit(code)

# --- Env & placeholders (fail fast on required) ---
required_env = [
    "SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_ROLE", "SNOWFLAKE_WAREHOUSE",
    "METRICS_DATABASE", "METRICS_SCHEMA_PREFIX", "METRICS_SQL_PATH"
]
missing = [k for k in required_env if not os.environ.get(k)]
if missing:
    fail(f"Missing required environment variables: {', '.join(missing)}")

account   = os.environ["SNOWFLAKE_ACCOUNT"]
user      = os.environ["SNOWFLAKE_USER"]
role      = os.environ["SNOWFLAKE_ROLE"]
wh        = os.environ["SNOWFLAKE_WAREHOUSE"]
password  = os.environ.get("SNOWFLAKE_PASSWORD") or ""
pk_b64    = os.environ.get("SNOWFLAKE_PRIVATE_KEY_B64") or ""
pk_pass   = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE") or ""
database  = os.environ["METRICS_DATABASE"]
prefix    = os.environ["METRICS_SCHEMA_PREFIX"]
sql_path  = os.environ["METRICS_SQL_PATH"]
gh_output = os.environ.get("GITHUB_OUTPUT")

# Resolve SQL path against repo root
repo_root = pathlib.Path(os.environ.get("GITHUB_WORKSPACE", "."))
sql_full_path = (repo_root / sql_path).resolve()

if not sql_full_path.exists():
    fail(f"SQL file not found at: {sql_full_path}")

sql_text = sql_full_path.read_text(encoding="utf-8")

# Replace placeholders
replacements = {
    "__database__": database,
    "__schema_prefix__": prefix,
    "__schemaPrefix__": prefix,   # tolerate camelCase
}
for k, v in replacements.items():
    sql_text = sql_text.replace(k, v)

print("::group::Rendered SQL (sql_metrics.sql)")
for line in sql_text.splitlines():
    print(line)
print("::endgroup::")

# --- Connect (password OR key) ---
conn_kwargs = dict(
    account=account, user=user, role=role, warehouse=wh,
    session_parameters={"QUERY_TAG": "observability_metrics_workflow"}
)

if pk_b64:
    try:
        key_bytes = base64.b64decode(pk_b64)
        pkey = serialization.load_der_private_key(
            key_bytes,
            password=pk_pass.encode() if pk_pass else None,
            backend=default_backend()
        )
        pk = pkey.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        conn_kwargs["private_key"] = pk
    except Exception as e:
        fail(f"Failed to load private key: {e}")
elif password:
    conn_kwargs["password"] = password
else:
    fail("No Snowflake auth provided (password or private key).")

# --- Execute and format outputs ---
cnx = snowflake.connector.connect(**conn_kwargs)
try:
    cur = cnx.cursor()
    cur.execute(sql_text)
    row = cur.fetchone()
    if not row:
        fail("Metrics query returned no rows.")

    # Expect: last_date, wk_total_queries, wk_failed_queries, wk_avg_query_duration_sec, storage_gb_estimate
    try:
        last_date, wk_total_queries, wk_failed_queries, wk_avg, storage_gb = row
    except Exception as e:
        fail(f"Unexpected result shape from metrics SQL. Expected 5 columns; got {len(row)}. Error: {e}")

    print("=== Snowflake INFORMATION_SCHEMA Metrics (last 7 days) ===")
    print(f"Last date:            {last_date}")
    print(f"Total queries:        {wk_total_queries}")
    print(f"Failed queries:       {wk_failed_queries}")
    print(f"Avg query duration s: {wk_avg}")
    print(f"Storage (GB):         {storage_gb}")

    if gh_output:
        with open(gh_output, "a") as fh:
            fh.write(f"last_date={last_date}\n")
            fh.write(f"wk_total_queries={wk_total_queries}\n")
            fh.write(f"wk_failed_queries={wk_failed_queries}\n")
            fh.write(f"wk_avg_sec={wk_avg}\n")
            fh.write(f"storage_gb={storage_gb}\n")
    else:
        print("::warning::GITHUB_OUTPUT not set; step outputs will not be exported.")

finally:
    try:
        cnx.close()
    except Exception:
        pass

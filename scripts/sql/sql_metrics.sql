-- Snowflake INFORMATION_SCHEMA metrics over the last 7 days.
-- Placeholders replaced by your orchestrator (e.g., Python/DBT vars):
--   __database__       : target database (e.g. LOGISTICS_DEMO)
--   __schema_prefix__  : logical layer/prefix to focus (e.g. 'gold', 'silver')
--                        If you use dynamic issue-based schemas, pass 'gold_%' etc.
-- Optional: keep results scoped to one warehouse/user if desired
-- set warehouse_filter = 'LOGISTICS_WH';
-- set user_filter      = 'DATAOPS_DBT_USER';
select
  wk.last_date,
  wk.wk_total_queries,
  wk.wk_failed_queries,
  round(wk.wk_avg_query_duration_sec, 3)       as wk_avg_query_duration_sec,
  round(st.total_bytes / 1024.0 / 1024.0 / 1024.0, 3) as storage_gb_estimate
from week_kpis wk
cross join storage st;

WITH q AS (
  SELECT
    CAST(CONVERT_TIMEZONE ('UTC', end_time) AS DATE) AS run_date,
    qh.user_name,
    qh.warehouse_name,
    COUNT(*) AS total_queries,
    AVG(qh.total_elapsed_time / 1000.0) AS avg_query_duration_sec,
    SUM(
      CASE
        WHEN NOT qh.error_code IS NULL THEN 1
        ELSE 0
      END
    ) AS failed_queries
  FROM
    TABLE (
      information_schema.query_history (
        DATEADD (DAY, -1, CURRENT_TIMESTAMP())
        /* Changed from -7 to -1 day */,
        CURRENT_TIMESTAMP(),
        10000
      )
    ) AS qh
  where qh.database_name = '__database__'
    -- Uncomment to narrow further:
    -- and qh.warehouse_name = $warehouse_filter
    -- and qh.user_name      = $user_filter
  GROUP BY
    1,
    2,
    3
),
storage AS (
  SELECT
    CURRENT_DATE AS as_of_date,
    SUM(
      active_bytes + time_travel_bytes + failsafe_bytes
    ) AS total_bytes
  FROM
    LOGISTICS_DEMO.information_schema.table_storage_metrics
  where table_catalog = '__database__'
    and table_schema  ilike '__schema_prefix__%'  
),
q_agg AS (
  SELECT
    run_date,
    SUM(total_queries) AS total_queries,
    AVG(avg_query_duration_sec) AS avg_query_duration_sec,
    SUM(failed_queries) AS failed_queries
  FROM
    q
  GROUP BY
    1
),
week_kpis AS (
  SELECT
    MAX(run_date) AS last_date,
    SUM(total_queries) AS wk_total_queries,
    AVG(avg_query_duration_sec) AS wk_avg_query_duration_sec,
    SUM(failed_queries) AS wk_failed_queries
  FROM
    q_agg
)
SELECT
  wk.last_date,
  wk.wk_total_queries,
  wk.wk_failed_queries,
  ROUND(wk.wk_avg_query_duration_sec, 3) AS wk_avg_query_duration_sec,
  ROUND(st.total_bytes / 1024.0 / 1024.0 / 1024.0, 3) AS storage_gb_estimate
FROM
  week_kpis AS wk
  CROSS JOIN storage AS st;
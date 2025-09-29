--
-- This metrics query is executed by the Python compute_metrics script.
-- It uses Python string formatting to substitute the gold and silver
-- schema names at runtime (e.g. gold="prod", silver="silver").
-- The placeholders {gold} and {silver} are replaced by the caller.
--
WITH d AS (
  SELECT
    report_date,
    SUM(TOTAL_ORDERS)           AS total_orders,
    SUM(TOTAL_UNITS_SHIPPED)    AS units_shipped,
    AVG(STOCK_TURNOVER_RATIO)   AS stock_turnover_ratio
  FROM LOGISTICS_DEMO.{gold}.DAILY_INVENTORY_KPIS
  WHERE report_date >= DATEADD('day', -7, CURRENT_DATE())
  GROUP BY 1
)
SELECT
  MAX(report_date)             AS last_date,
  SUM(total_orders)            AS wk_orders,
  SUM(units_shipped)           AS wk_units,
  AVG(stock_turnover_ratio)    AS avg_turnover
FROM d;

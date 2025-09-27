-- 1) Ensure KPI schema exists
CREATE SCHEMA IF NOT EXISTS LOGISTICS_DEMO.{{GOLD_SCHEMA}};

-- 2) Rebuild KPI table in the gold schema from silver snapshot + master_data seeds
CREATE OR REPLACE TABLE LOGISTICS_DEMO.{{GOLD_SCHEMA}}.DAILY_INVENTORY_KPIS AS
WITH s AS (
    SELECT
        movement_date AS report_date,
        warehouse_id,
        product_id,
        COALESCE(qty_ordered, 0)     AS qty_ordered,
        COALESCE(qty_shipped, 0)     AS qty_shipped,
        COALESCE(qty_replenished, 0) AS qty_replenished,
        COALESCE(qty_adjusted, 0)    AS qty_adjusted
    FROM LOGISTICS_DEMO.{{SILVER_SCHEMA}}.DAILY_INVENTORY_SNAPSHOT
)
SELECT
    s.report_date                                   AS REPORT_DATE,
    w.WAREHOUSE_NAME                                AS WAREHOUSE_NAME,
    p.PRODUCT_NAME                                  AS PRODUCT_NAME,
    s.qty_ordered                                   AS TOTAL_ORDERS,
    s.qty_shipped                                   AS TOTAL_UNITS_SHIPPED,
    s.qty_replenished                               AS TOTAL_UNITS_REPLENISHED,
    ROUND(s.qty_shipped / NULLIF(s.qty_replenished + 1, 0), 2) AS STOCK_TURNOVER_RATIO
FROM LOGISTICS_DEMO.{{MASTER_SCHEMA}}.WAREHOUSES w
JOIN s
  ON s.warehouse_id = w.WAREHOUSE_ID
JOIN LOGISTICS_DEMO.{{MASTER_SCHEMA}}.PRODUCTS p
  ON s.product_id = p.PRODUCT_ID;

-- 3) Final SELECT (this is the result set the Python returns)
SELECT
    REPORT_DATE,
    WAREHOUSE_NAME,
    PRODUCT_NAME,
    TOTAL_ORDERS,
    TOTAL_UNITS_SHIPPED,
    TOTAL_UNITS_REPLENISHED,
    STOCK_TURNOVER_RATIO
FROM LOGISTICS_DEMO.{{GOLD_SCHEMA}}.DAILY_INVENTORY_KPIS
ORDER BY REPORT_DATE DESC
LIMIT 10;

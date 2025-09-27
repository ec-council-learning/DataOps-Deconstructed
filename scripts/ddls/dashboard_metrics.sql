CREATE SCHEMA IF NOT EXISTS LOGISTICS_DEMO.{{SCHEMA_NAME}};

CREATE OR REPLACE TABLE LOGISTICS_DEMO.{{SCHEMA_NAME}}.DAILY_INVENTORY_KPIS AS
WITH s AS (
    SELECT
        movement_date AS report_date,
        warehouse_id,
        product_id,
        COALESCE(qty_ordered, 0)     AS qty_ordered,
        COALESCE(qty_shipped, 0)     AS qty_shipped,
        COALESCE(qty_replenished, 0) AS qty_replenished,
        COALESCE(qty_adjusted, 0)    AS qty_adjusted
    FROM LOGISTICS_DEMO.{{SCHEMA_NAME | replace('gold','silver') }}.DAILY_INVENTORY_SNAPSHOT
)
SELECT
    s.report_date                                   AS REPORT_DATE,
    w.warehouse_name                                AS WAREHOUSE_NAME,
    p.product_name                                  AS PRODUCT_NAME,
    s.qty_ordered                                   AS TOTAL_ORDERS,
    s.qty_shipped                                   AS TOTAL_UNITS_SHIPPED,
    s.qty_replenished                               AS TOTAL_UNITS_REPLENISHED,
    ROUND( s.qty_shipped / NULLIF(s.qty_replenished + 1, 0), 2) AS STOCK_TURNOVER_RATIO
FROM LOGISTICS_DEMO.{{SCHEMA_NAME | replace('gold','master_data') }}.warehouses w
JOIN s
  ON s.warehouse_id = w.warehouse_id
JOIN LOGISTICS_DEMO.{{SCHEMA_NAME | replace('gold','master_data') }}.products p
  ON s.product_id = p.product_id;

-- final SELECT (the script will return this result set)
SELECT
    REPORT_DATE,
    WAREHOUSE_NAME,
    PRODUCT_NAME,
    TOTAL_ORDERS,
    TOTAL_UNITS_SHIPPED,
    TOTAL_UNITS_REPLENISHED,
    STOCK_TURNOVER_RATIO
FROM LOGISTICS_DEMO.{{SCHEMA_NAME}}.DAILY_INVENTORY_KPIS
ORDER BY REPORT_DATE DESC
LIMIT 10;

-- scripts/dbt/models/gold/daily_inventory_kpis.sql

SELECT
    movement_date AS report_date,
    warehouse_name,
    product_name,
    category,
    SUM(qty_ordered) AS total_orders,
    SUM(qty_shipped) AS total_units_shipped,
    SUM(qty_replenished) AS total_units_replenished,
    AVG(net_inventory_change) AS avg_daily_inventory_change,
    CASE
        WHEN
            SUM(qty_shipped) > 0
            THEN ROUND(SUM(qty_shipped) / NULLIF(SUM(qty_replenished), 0), 2)
        ELSE 0
    END AS stock_turnover_ratio
FROM LOGISTICS_DEMO.silver.daily_inventory_snapshot
GROUP BY
    report_date,
    warehouse_name,
    product_name,
    category
ORDER BY report_date DESC, warehouse_name ASC, product_name ASC
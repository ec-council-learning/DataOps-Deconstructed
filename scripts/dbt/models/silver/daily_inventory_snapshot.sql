-- scripts/dbt/models/silver/daily_inventory_snapshot.sql

WITH inventory AS (
    SELECT
        MOVEMENT_DATE,
        WAREHOUSE_ID,
        PRODUCT_ID,
        SUM(CASE WHEN MOVEMENT_TYPE = 'replenishment' THEN QUANTITY ELSE 0 END) AS qty_replenished,
        SUM(CASE WHEN MOVEMENT_TYPE = 'outbound'      THEN ABS(QUANTITY) ELSE 0 END) AS qty_shipped,
        SUM(CASE WHEN MOVEMENT_TYPE = 'adjustment'    THEN QUANTITY ELSE 0 END) AS qty_adjusted
    FROM {{ ref('stg_inventory_movements') }}
    GROUP BY MOVEMENT_DATE, WAREHOUSE_ID, PRODUCT_ID
),

orders AS (
    SELECT
        ORDER_DATE   AS movement_date,
        WAREHOUSE_ID,
        PRODUCT_ID,
        SUM(QUANTITY) AS qty_ordered
    FROM {{ ref('stg_customers_orders') }}
    GROUP BY ORDER_DATE, WAREHOUSE_ID, PRODUCT_ID
)

SELECT
    inv.MOVEMENT_DATE                                             AS movement_date,
    inv.WAREHOUSE_ID                                              AS warehouse_id,
    wh.WAREHOUSE_NAME                                             AS warehouse_name,
    inv.PRODUCT_ID                                                AS product_id,
    prd.PRODUCT_NAME                                              AS product_name,
    prd.CATEGORY                                                  AS product_category,
    COALESCE(inv.qty_replenished, 0)                              AS qty_replenished,
    COALESCE(inv.qty_shipped, 0)                                  AS qty_shipped,
    COALESCE(inv.qty_adjusted, 0)                                 AS qty_adjusted,
    COALESCE(ord.qty_ordered, 0)                                  AS qty_ordered,
    COALESCE(inv.qty_replenished, 0)
      - COALESCE(inv.qty_shipped, 0)
      + COALESCE(inv.qty_adjusted, 0)                             AS net_inventory_change
FROM inventory inv
LEFT JOIN orders ord
  ON  inv.MOVEMENT_DATE = ord.movement_date
  AND inv.WAREHOUSE_ID  = ord.WAREHOUSE_ID
  AND inv.PRODUCT_ID    = ord.PRODUCT_ID
LEFT JOIN {{ ref('stg_products') }} prd
  ON inv.PRODUCT_ID = prd.PRODUCT_ID
LEFT JOIN {{ ref('stg_warehouses') }} wh
  ON inv.WAREHOUSE_ID = wh.WAREHOUSE_ID
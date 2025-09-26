-- scripts/dbt/models/bronze/stg_inventory_movements.sql

SELECT
    MOVEMENT_ID,
    PRODUCT_ID,
    WAREHOUSE_ID,
    MOVEMENT_DATE,
    QUANTITY,
    MOVEMENT_TYPE
FROM {{ source('bronze', 'inventory_movements') }}

-- staging for inventory_movements seed
-- use ref('inventory_movements') because the data is loaded from a seed
SELECT
    movement_id,
    product_id,
    warehouse_id,
    movement_date,
    quantity,
    movement_type
FROM {{ ref('inventory_movements') }}

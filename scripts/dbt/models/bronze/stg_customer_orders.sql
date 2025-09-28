-- staging for customer_orders seed
-- use ref('customer_orders') because the data is loaded from a seed
SELECT
    order_id,
    product_id,
    warehouse_id,
    order_date,
    quantity,
    sales_channel
FROM {{ ref('customer_orders') }}

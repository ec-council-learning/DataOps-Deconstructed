-- scripts/dbt/models/bronze/stg_customer_orders.sql

SELECT
    ORDER_ID,
    PRODUCT_ID,
    WAREHOUSE_ID,
    ORDER_DATE,
    QUANTITY,
    SALES_CHANNEL
FROM {{ source(generate_schema_name('bronze', this), generate_alias_name('customer_orders', this)) }}

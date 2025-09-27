-- scripts/dbt/models/bronze/stg_customer_orders.sql

SELECT
    ORDER_ID,
    PRODUCT_ID,
    WAREHOUSE_ID,
    ORDER_DATE,
    QUANTITY,
    SALES_CHANNEL
FROM LOGISTICS_DEMO.None.customer_orders
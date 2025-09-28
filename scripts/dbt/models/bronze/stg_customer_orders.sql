-- Stage FROM Bronze Snowflake table (not seeds)
with raw as (
  select
    order_id,
    product_id,
    warehouse_id,
    order_date,
    quantity,
    sales_channel
  from {{ source('bronze', 'customer_orders') }}
)

select
  order_id      as ORDER_ID,
  product_id    as PRODUCT_ID,
  warehouse_id  as WAREHOUSE_ID,
  cast(order_date as date) as ORDER_DATE,
  cast(quantity as int)    as QUANTITY,
  sales_channel as SALES_CHANNEL
from raw
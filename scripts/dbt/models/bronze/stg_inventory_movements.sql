-- Stage FROM Bronze Snowflake table (not seeds)
with raw as (
  select
    movement_id,
    product_id,
    warehouse_id,
    movement_date,
    quantity,
    movement_type
  from {{ source('bronze', 'inventory_movements') }}
)

select
  movement_id   as MOVEMENT_ID,
  product_id    as PRODUCT_ID,
  warehouse_id  as WAREHOUSE_ID,
  cast(movement_date as date) as MOVEMENT_DATE,
  cast(quantity as int)       as QUANTITY,
  movement_type as MOVEMENT_TYPE
from raw
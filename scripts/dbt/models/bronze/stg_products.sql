-- Stage FROM Bronze Snowflake table (not seeds)
with raw as (
  select
    product_id,
    product_name,
    category,
    unit_cost,
    weight_kg,
    dimensions_cm
  from {{ source('bronze', 'products') }}
)

select
  product_id    as PRODUCT_ID,
  product_name  as PRODUCT_NAME,
  category      as CATEGORY,
  unit_cost     as UNIT_COST,
  weight_kg     as WEIGHT_KG,
  dimensions_cm as DIMENSIONS_CM
from raw
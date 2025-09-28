-- Stage FROM Bronze Snowflake table (not seeds)
with raw as (
  select
    warehouse_id,
    warehouse_name,
    location,
    capacity_units,
    manager_name
  from {{ source('bronze', 'warehouses') }}
)

select
  warehouse_id   as WAREHOUSE_ID,
  warehouse_name as WAREHOUSE_NAME,
  location       as LOCATION,
  capacity_units as CAPACITY_UNITS,
  manager_name   as MANAGER_NAME
from raw
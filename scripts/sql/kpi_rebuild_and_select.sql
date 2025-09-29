--
-- KPI table rebuild & preview. Placeholders are neutral and replaced by Python:
--   __gold_schema__, __silver_schema__, __bronze_schema__
--

-- 1) Ensure KPI schema exists
create schema if not exists logistics_demo.__gold_schema__;

-- 2) Rebuild KPI table in the gold schema from silver snapshot + bronze staging
create or replace table logistics_demo.__gold_schema__.daily_inventory_kpis as
with s as (
  select
    movement_date as report_date,
    warehouse_id,
    product_id,
    coalesce(qty_ordered, 0)     as qty_ordered,
    coalesce(qty_shipped, 0)     as qty_shipped,
    coalesce(qty_replenished, 0) as qty_replenished,
    coalesce(qty_adjusted, 0)    as qty_adjusted
  from logistics_demo.__silver_schema__.daily_inventory_snapshot
)
select
  s.report_date,
  w.warehouse_name,
  p.product_name,
  p.category,
  s.qty_ordered,
  s.qty_shipped,
  s.qty_replenished,
  -- classic turnover: shipped / replenished (avoid div-by-zero)
  round( s.qty_shipped / nullif(s.qty_replenished, 0), 2 ) as stock_turnover_ratio
from logistics_demo.__bronze_schema__.stg_warehouses w
join s
  on s.warehouse_id = logistics_demo.__bronze_schema__.stg_warehouses.warehouse_id
join logistics_demo.__bronze_schema__.stg_products
  on s.product_id = logistics_demo.__bronze_schema__.stg_products.product_id;

-- 3) Final SELECT (Python returns this result set)
select
  report_date,
  warehouse_name,
  product_name,
  category,
  total_orders,
  total_units_shipped,
  total_units_replenished,
  stock_turnover_ratio
from logistics_demo.__gold_schema__.daily_inventory_kpis
order by report_date desc
limit 10;

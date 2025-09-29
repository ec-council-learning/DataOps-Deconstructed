-- sqlfluff: rules disabled none (placeholders use defaults to avoid TMP/JJ01)
--
-- This script is used by the compute_metrics Python script (and the
-- dashboard rebuild) to construct and query a KPI table in Snowflake.
-- Placeholders are replaced at runtime by Python.
--   {{ GOLD_SCHEMA }}, {{ SILVER_SCHEMA }}, {{ BRONZE_SCHEMA }}
--

-- 1) Ensure KPI schema exists
create schema if not exists logistics_demo.{{ GOLD_SCHEMA | default('gold') }};

-- 2) Rebuild KPI table in the gold schema from silver snapshot + bronze staging
create or replace table logistics_demo.{{ GOLD_SCHEMA | default('gold') }}.daily_inventory_kpis as
with s as (
  select
    movement_date as report_date,
    warehouse_id,
    product_id,
    coalesce(qty_ordered, 0)     as qty_ordered,
    coalesce(qty_shipped, 0)     as qty_shipped,
    coalesce(qty_replenished, 0) as qty_replenished,
    coalesce(qty_adjusted, 0)    as qty_adjusted
  from logistics_demo.{{ SILVER_SCHEMA | default('silver') }}.daily_inventory_snapshot
)
select
  s.report_date                                     as report_date,
  w.warehouse_name                                  as warehouse_name,
  p.product_name                                    as product_name,
  p.category                                        as category,
  s.qty_ordered                                     as total_orders,
  s.qty_shipped                                     as total_units_shipped,
  s.qty_replenished                                 as total_units_replenished,
  /* classic turnover: shipped / replenished (avoid div-by-zero) */
  round( s.qty_shipped / nullif(s.qty_replenished, 0), 2 ) as stock_turnover_ratio
from logistics_demo.{{ BRONZE_SCHEMA | default('bronze') }}.stg_warehouses w
join s
  on s.warehouse_id = w.warehouse_id
join logistics_demo.{{ BRONZE_SCHEMA | default('bronze') }}.stg_products p
  on s.product_id = p.product_id;

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
from logistics_demo.{{ GOLD_SCHEMA | default('gold') }}.daily_inventory_kpis
order by report_date desc
limit 10;

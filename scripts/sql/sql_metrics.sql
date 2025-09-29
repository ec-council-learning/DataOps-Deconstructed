--
-- Metrics aggregation over the last 7 days.
-- Placeholder replaced by Python: __GOLD_SCHEMA__
--

with d as (
  select
    report_date,
    sum(total_orders)          as total_orders,
    sum(total_units_shipped)   as units_shipped,
    avg(stock_turnover_ratio)  as stock_turnover_ratio
  from logistics_demo.__GOLD_SCHEMA__.daily_inventory_kpis
  where report_date >= dateadd('day', -7, current_date())
  group by 1
)

select
  max(report_date)            as last_date,
  sum(total_orders)           as wk_orders,
  sum(units_shipped)          as wk_units,
  avg(stock_turnover_ratio)   as avg_turnover
from d;

--
-- This metrics query is executed by the Python compute_metrics script.
-- It uses Python string formatting to substitute the gold and silver
-- schema names at runtime (e.g. gold="prod", silver="silver").  The
-- placeholders {gold} and {silver} are replaced by the calling
-- script to target the correct schema during execution.
--
with d as (
  select
    report_date,
    sum(total_orders)          as total_orders,
    sum(total_units_shipped)   as units_shipped,
    avg(stock_turnover_ratio)  as stock_turnover_ratio
  from {gold}.daily_inventory_kpis
  where report_date >= dateadd('day', -7, current_date())
  group by 1
)
select
  max(report_date)                      as last_date,
  sum(total_orders)                     as wk_orders,
  sum(units_shipped)                    as wk_units,
  avg(stock_turnover_ratio)            as avg_turnover
from d;

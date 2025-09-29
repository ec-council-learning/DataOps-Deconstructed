{{ config(materialized='table') }}

with execs as (
  select
    invocation_id,
    status
  from {{ ref('fct_dbt__test_executions') }}
),

inv as (
  select
    invocation_id,
    started_at as run_started_at
  from {{ ref('fct_dbt__invocations') }}
),

tests as (
  select
    e.invocation_id,
    i.run_started_at,
    /* portable across warehouses */
    sum(case when e.status = 'pass' then 1 else 0 end) as tests_passed,
    count(*)                                          as tests_total
    /* If you're Snowflake-only, you can replace the two lines above with:
       count_if(e.status = 'pass') as tests_passed,
       count(*)                     as tests_total
    */
  from execs e
  inner join inv i
    on e.invocation_id = i.invocation_id
  group by 1, 2
)

select
  invocation_id,
  run_started_at,
  tests_passed,
  tests_total,
  round(100.0 * tests_passed / nullif(tests_total, 0), 1) as pass_rate_pct
from tests

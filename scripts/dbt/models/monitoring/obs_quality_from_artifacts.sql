{{ config(materialized='table') }}

with tests as (
  select
    invocation_id,
    max(started_at)                   as run_started_at,
    count_if(status='pass')           as tests_passed,
    count(*)                          as tests_total
  from {{ ref('artifact_tests') }}     -- provided by dbt_artifacts
  group by 1
)

select
  invocation_id,
  run_started_at,
  tests_passed,
  tests_total,
  round(100.0 * tests_passed / nullif(tests_total,0), 1) as pass_rate_pct
from tests

-- scripts/dbt/models/bronze/stg_warehouses.sql

--
-- Staging model for the warehouses seed.
--
-- The warehouses seed (warehouses.csv) is generated via the create_seed.py script and
-- contains the following columns:
--   warehouse_id, warehouse_name, location, capacity_units, manager_name
--
-- This model selects from the seed using the ref() macro and aliases each
-- column to an uppercase name. Aligning column names in uppercase with other
-- staging models improves readability and ensures consistency across the
-- project. The resulting model can be referenced from downstream layers
-- (e.g. silver) using ref('stg_warehouses').

SELECT
    warehouse_id,
    warehouse_name,
    location,
    capacity_units,
    manager_name
FROM {{ ref('warehouses') }}

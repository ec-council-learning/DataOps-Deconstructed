-- scripts/dbt/models/bronze/stg_products.sql

--
-- Staging model for the products seed.
--
-- The products seed (products.csv) is generated via the create_seed.py script and
-- contains the following columns:
--   product_id, product_name, category, unit_cost, weight_kg, dimensions_cm
--
-- In keeping with the pattern used by other staging models (e.g. stg_customer_orders
-- and stg_inventory_movements), we select from the seed using the ref() macro
-- and alias each column to an uppercase name. This makes the column names
-- consistent across staging models and simplifies downstream references.

SELECT
    product_id,
    product_name,
    category,
    unit_cost,
    weight_kg,
    dimensions_cm
FROM {{ ref('stg_products') }}

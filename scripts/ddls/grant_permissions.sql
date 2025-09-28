--
-- Grant usage and DML privileges on all tables in the dynamically
-- generated schema.  The {{SCHEMA_NAME}} token will be replaced at
-- runtime (e.g. `bronze_issue_123` or `ci_456`) so that the
-- appropriate Snowflake role gains access to the feature-specific
-- schema and its tables.  This script is executed by the Python
-- `create_schema.py` helper as part of provisioning.
GRANT USAGE ON SCHEMA LOGISTICS_DEMO.{{SCHEMA_NAME}} TO ROLE LOGISTICS_DBT_ROLE;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA LOGISTICS_DEMO.{{SCHEMA_NAME}} TO ROLE LOGISTICS_DBT_ROLE;
GRANT SELECT, INSERT, UPDATE, DELETE ON FUTURE TABLES IN SCHEMA LOGISTICS_DEMO.{{SCHEMA_NAME}} TO ROLE LOGISTICS_DBT_ROLE;

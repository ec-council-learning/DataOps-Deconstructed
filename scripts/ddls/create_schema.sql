--
-- Create (or replace) a Snowflake schema in the LOGISTICS_DEMO database.
-- The {{SCHEMA_NAME}} placeholder is filled in by the provisioning
-- script so that feature runs and CI runs use isolated schemas (e.g.
-- `bronze_issue_123`).  This file is consumed by `create_schema.py`.
CREATE OR REPLACE SCHEMA LOGISTICS_DEMO.{{SCHEMA_NAME}};

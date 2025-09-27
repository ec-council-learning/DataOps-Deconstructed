# 🚀 **DBT Models – Fulfillment Logistics Scenario**

This document explicitly provides a clear overview of your DBT models structured dynamically around the Fulfillment Logistics Intelligent Inventory Management scenario. The models explicitly follow the Medallion Architecture (Bronze → Silver → Gold), leveraging dynamic naming macros based on GitHub Issue IDs.

---

## ✅ **Overview of DBT Transformations**

Your pipeline explicitly follows a clear and organized transformation strategy:

* **Bronze → Silver**: Validates, enriches, and integrates transactional data (`inventory_movements`, `customer_orders`) with master data (`products`, `warehouses`) explicitly.
* **Silver → Gold**: Generates aggregated KPIs explicitly to support actionable analytics, performance tracking, and predictive forecasting.

---

## 📂 **Explicit DBT Project Structure**

The DBT models explicitly reside within:

```
scripts/dbt/models/
├── bronze/
│   ├── stg_inventory_movements.sql
│   └── stg_customer_orders.sql
├── silver/
│   └── daily_inventory_snapshot.sql
└── gold/
    └── daily_inventory_kpis.sql
```

---

## 🔗 **DBT Dynamic Macros and Configuration**

DBT explicitly leverages macros located at:

```
scripts/dbt/macros/dynamic_naming.sql
```

These macros are explicitly configured in your project's `dbt_project.yml`:

```yaml
models:
  logistics_demo:
    bronze:
      schema: "{{ generate_schema_name('bronze', this) }}"
      alias: "{{ generate_alias_name(this.name, this) }}"
      materialized: view

    silver:
      schema: "{{ generate_schema_name('silver', this) }}"
      alias: "{{ generate_alias_name(this.name, this) }}"
      materialized: table

    gold:
      schema: "{{ generate_schema_name('gold', this) }}"
      alias: "{{ generate_alias_name(this.name, this) }}"
      materialized: table
```

---

## 📋 **Explicit DBT Model Descriptions**

### 🔹 **Bronze Layer Models**

* `stg_inventory_movements.sql`: Explicitly structures inventory transaction data, sourced dynamically from seed files.
* `stg_customer_orders.sql`: Explicitly structures customer order data, dynamically referencing seed sources.

### 🔹 **Silver Layer Model**

* `daily_inventory_snapshot.sql`: Integrates and explicitly enriches Bronze layer models with master product and warehouse data. Produces a detailed daily snapshot of inventory activities and order information.

### 🔹 **Gold Layer Model**

* `daily_inventory_kpis.sql`: Explicitly aggregates daily inventory data into actionable business KPIs, enabling analytics on inventory turnover, warehouse performance, and order fulfillment efficiency.

---

## 🗃️ **Explicit Data Quality and Testing**

Tests explicitly defined in:

```
scripts/dbt/models/schema.yml
```

These tests include explicit validation of unique identifiers, relational integrity, and data value ranges leveraging the `dbt_expectations` package.

---

## 🚦 **Pipeline Execution (Explicit Instructions)**

To explicitly run and validate your DBT models via GitHub Actions (`dbt_ci_cd.yml`):

1. Ensure all GitHub secrets are explicitly configured (`SNOWFLAKE_*`).
2. Explicitly trigger a deployment by pushing a tag `"pipeline validation"`:

```bash
git commit -am "Update for pipeline validation"
git tag "pipeline validation"
git push origin --tags
```

GitHub Actions explicitly execute all DBT models and tests, dynamically manage schemas, and explicitly generate comprehensive observability dashboards.

---

## 📖 **DBT Documentation (Lineage and Models)**

Generate explicit documentation using:

```bash
cd scripts/dbt
dbt docs generate
dbt docs serve
```

---

## 🎯 **Explicit Benefits of Dynamic DBT Models**

* **Clear data governance:** Dynamic naming explicitly associates data models with individual GitHub issues or feature branches.
* **Explicit pipeline traceability:** Simplifies incident response and troubleshooting through clearly structured, dynamically named schemas.
* **Improved observability:** Explicit DBT model documentation and observability dashboards facilitate proactive pipeline management.

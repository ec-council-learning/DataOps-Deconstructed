# 🚀 **Dynamic DBT Naming with GitHub Issues**

## 📖 **Overview**

This guide explicitly covers how DBT leverages macros for dynamic schema and model naming based on GitHub Issue IDs. Dynamic naming allows clear, organized, and automated management of data pipelines and schemas tailored explicitly for each development feature.

---

## ⚙️ **Dynamic Naming Macros**

The macros for dynamic naming are explicitly located in:

```
scripts/dbt/macros/dynamic_naming.sql
```

### **Included Macros**

* `get_issue_id()`: Fetches the current GitHub Issue ID explicitly from the environment.
* `generate_schema_name(custom_schema_name, node)`: Generates explicit schema names based on GitHub Issue ID.
* `generate_alias_name(custom_alias_name, node)`: Generates explicit model alias names dynamically based on GitHub Issue ID.

---

## 🗃️ **DBT Models Directory**

Your DBT models explicitly use these dynamic naming macros, structured as follows:

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

*These DBT models explicitly use references to sources and models defined using macros.*

---

## ✅ **DBT Schema Testing**

Data quality and model validation tests are explicitly defined in:

```
scripts/dbt/models/schema.yml
```

This file explicitly includes data-quality checks leveraging your dynamically named models.

---

## 🚦 **Explicit Workflow Usage**

When executing DBT via GitHub Actions, explicitly set the `GITHUB_ISSUE_ID` variable in your workflow:

```yaml
env:
  GITHUB_ISSUE_ID: ${{ github.event.issue.number }}
```

This explicit definition ensures dynamic naming is correctly applied, for example:

| Layer  | Schema Name       | Model Name                          |
| ------ | ----------------- | ----------------------------------- |
| Bronze | `bronze_issue_45` | `stg_inventory_movements_issue_45`  |
| Bronze | `bronze_issue_45` | `stg_customer_orders_issue_45`      |
| Silver | `silver_issue_45` | `daily_inventory_snapshot_issue_45` |
| Gold   | `gold_issue_45`   | `daily_inventory_kpis_issue_45`     |

---

## 🎯 **Practical Benefits of Dynamic DBT Macros**

* **Clear isolation** of DBT schemas and models explicitly per GitHub issue or feature branch.
* **Enhanced governance and observability**, providing explicit traceability of changes.
* **Simplified pipeline automation** explicitly managed via GitHub Actions workflows.

# 📦 Intelligent Inventory Management DataOps Sandbox

This repository provides a robust, hands-on implementation of modern DataOps and DataSecOps methodologies, leveraging DBT, Snowflake, and GitHub Actions for fully automated, secure, and observable data pipelines.

---

## 🎯 **Objectives**

* Build automated and dynamic data pipelines with DBT.
* Securely manage data in Snowflake using Infrastructure as Code (IaC).
* Automate deployments explicitly aligned with GitFlow using GitHub Actions.
* Implement comprehensive observability, monitoring, and incident response explicitly.
* Enforce robust security standards through automated testing, auditing, and policy controls.

---

## ✅ **Prerequisites**

Ensure these explicit configurations are set before starting:

* **DBT Cloud Account**: [cloud.getdbt.com](https://cloud.getdbt.com/signup)
* **Snowflake Account**: [signup.snowflake.com](https://signup.snowflake.com)
* **GitHub Repository**: Configure repository secrets (`SNOWFLAKE_*`, `SLACK_WEBHOOK_URL`)
* **Slack Integration**: Configure webhook explicitly for real-time notifications ([Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks))

---

## 📂 **Final Repository Structure**

```bash
dataops/
├── docs/
│   ├── 00_services_configuration.md
│   ├── 01_dbt_seed_data.md
│   ├── 02_dbt_dynamic_macros.md
│   ├── 03_dbt_models.md
│   ├── 04_snowflake_setup.md
│   ├── 05_github_actions_automation.md
│   ├── 06_github_issue_templates.md
│   └── 07_security_policy.md
├── metadata/
├── scripts/
│   ├── dbt/
│   │   ├── macros/
│   │   │   └── dynamic_naming.sql
│   │   ├── models/
│   │   │   ├── bronze/
│   │   │   │   ├── stg_customer_orders.sql
│   │   │   │   └── stg_inventory_movements.sql
│   │   │   ├── silver/
│   │   │   │   └── daily_inventory_snapshot.sql
│   │   │   ├── gold/
│   │   │   │   └── daily_inventory_kpis.sql
│   │   │   └── schema.yml
│   │   ├── dbt_project.yml
│   │   ├── packages.yml
│   │   ├── profiles.yml
│   │   └── seeds/
│   ├── ddls/
│   │   ├── create_schema.sql
│   │   ├── create_tables.sql
│   │   ├── dashboard_metrics.sql
│   │   └── grant_permissions.sql
│   └── python/
│       ├── create_dashboard.py
│       ├── create_schema.py
│       ├── drop_schema.py
│       ├── create_seed.py
│       └── requirements.txt
├── workflows/
│   ├── dbt_ci_cd.yml
│   ├── observability_metrics.yml
│   └── security_sast_scan.yml
├── README.md
└── LICENSE
```

---

## 📚 **Explicit File and Directory Descriptions**

### 📌 **`docs/`**

Detailed markdown documentation for explicit setup and configuration.

| File Name                         | Description                                                                                    |
| --------------------------------- | ---------------------------------------------------------------------------------------------- |
| `00_services_configuration.md`    | Explicit setup for external services (DBT, Snowflake, GitHub, Slack).                          |
| `01_dbt_seed_data.md`             | Explicit instructions for generating dynamic seed data for DBT.                                |
| `02_dbt_dynamic_macros.md`        | Explicit guidance on dynamic schema/model naming macros.                                       |
| `03_dbt_models.md`                | Explanation of dynamic DBT models and pipeline structure explicitly.                           |
| `04_snowflake_setup.md`           | Instructions for explicit dynamic Snowflake schema creation.                                   |
| `05_github_actions_automation.md` | Detailed guidance on GitHub Actions CI/CD, security, and observability automation explicitly.  |
| `06_github_issue_templates.md`    | GitHub issue templates explicitly for pipeline object lifecycle management.                    |
| `07_security_policy.md`           | Explicit security policy documentation with declarative controls and service boundaries.       |

---

### 📌 **`scripts/dbt/`**

Explicit DBT project and pipeline management files.

| Path                                | Description                                                   |
| ----------------------------------- | ------------------------------------------------------------- |
| `dbt_project.yml`                   | Explicit DBT project configuration and macros.                |
| `profiles.yml`                      | Explicit dynamic DBT profile configurations.                  |
| `macros/dynamic_naming.sql`         | Macros explicitly for dynamic naming based on GitHub Issues.  |
| `models/{bronze,silver,gold}/*.sql` | Explicit DBT models implementing the Medallion Architecture.  |
| `schema.yml`                        | Explicit data quality checks and testing schemas.             |
| `seeds/*.csv`                       | CSV seed files explicitly generated via `create_seed.py`.     |
| `packages.yml`                      | DBT package dependencies explicitly declared.                 |

---

### 📌 **`scripts/ddls/`**

Externalized SQL scripts explicitly for schema/object management.

| SQL File Name           | Description                                             |
| ----------------------- | ------------------------------------------------------- |
| `create_schema.sql`     | Explicit schema creation SQL template.                  |
| `create_tables.sql`     | Explicit SQL template for table creation.               |
| `dashboard_metrics.sql` | SQL explicitly for observability metrics.               |
| `grant_permissions.sql` | SQL explicitly defining permissions and access control. |

---

### 📌 **`scripts/python/`**

Python scripts explicitly for pipeline automation tasks.

| Script Name           | Description                                                            |
| --------------------- | ---------------------------------------------------------------------- |
| `create_seed.py`      | Dynamically generates DBT seed CSV data explicitly.                    |
| `create_schema.py`    | Explicit dynamic schema/table creation in Snowflake.                   |
| `drop_schema.py`      | Explicit cleanup of dynamically created Snowflake schemas and objects. |
| `create_dashboard.py` | Explicit automated generation of metrics dashboards.                   |
| `requirements.txt`    | Python dependencies explicitly for automation scripts.                 |

---

### 📌 **`github/workflows/`**

Explicit GitHub Actions automation workflows.

| Workflow File Name          | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| `dbt_ci_cd.yml`             | Explicit DBT CI/CD pipeline automation aligned with GitFlow. |
| `observability_metrics.yml` | Automated metrics dashboard generation explicitly.           |
| `security_sast_scan.yml`    | Explicit SQL security auditing and linting automation.       |

---

### 📌 **`github/issue_templates/`**

Explicit GitHub Actions automation issue templates.

| Workflow File Name          | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| `feature_request.yml`       | Action triggered Issue template Creation.                    |
| `cleanup_request.yml`       | Action triggered Issue template Deletion.                    |

---

## 🚀 **Quick Start (Explicit Pipeline Validation)**

Explicitly trigger a full pipeline validation using a Git tag:

```bash
git commit -am "Explicit changes for pipeline validation"
git tag "pipeline validation"
git push origin --tags
```

This explicitly triggers:

* Dynamic seed generation (`create_seed.py`).
* Explicit schema and DBT model deployment (`create_schema.py`, DBT).
* Metrics dashboard generation (`create_dashboard.py`).
* Comprehensive pipeline validation with automated alerts.

---

## ✅ **Explicit Next Steps**

* Explicitly configure GitHub secrets (`SNOWFLAKE_*`, `SLACK_WEBHOOK_URL`).
* Review detailed documentation under `docs/` explicitly.
* Collaborate using explicitly structured GitHub issues templates provided.

---

## 🔒 **Explicit Support and Security**

Explicitly contact the Runink Logistics team for support or security concerns:

* 📧 [paes@runink.org](mailto:paes@runink.org)

---

## 🛡️ **License and Contributions**

This repository explicitly adheres to the [MIT License](LICENSE). Contributions explicitly welcome via GitHub issues or pull requests.
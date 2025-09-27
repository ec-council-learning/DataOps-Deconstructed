# 🚀 GitHub Actions Workflows for DataOps Sandbox

## Comprehensive Automation: CI/CD, Security, and Observability

This document provides detailed guidance and comprehensive GitHub Actions workflows covering:

* **Pipeline automation** (CI/CD with GitFlow principles)
* **Security auditing** (CIS-aligned controls, Pre-commit hooks, SQL linting/SAST)
* **Observability and Metrics** (Dashboards, alerts, Slack integration)

---

## ✅ **Workflow Overview**

Your GitHub Actions workflows provide:

* Automated deployments of DBT & Snowflake schemas and tables based on GitHub issue IDs.
* Continuous integration and delivery aligned with GitFlow.
* Automated enforcement of CIS Security benchmarks.
* Real-time observability through metrics dashboards and Slack alerts.

---

## 📂 **Workflows Structure**

```
.github/workflows/
├── dbt_ci_cd.yml
├── sast_scan.yml
└── metrics_dashboard.yml
```

---

## ⚙️ **1. DBT CI/CD Workflow** (`dbt_ci_cd.yml`)

This workflow dynamically deploys DBT and Snowflake environments based on GitHub Issues, aligning with GitFlow (PROD, DEV, Feature):

---

## 🔒 **2. Security Auditing and CIS Controls** (`sast_scan.yml`)

Automated security audits aligned explicitly with CIS Benchmarks and secure coding best practices using SQLFluff and pre-commit hooks.

**Controls Covered (aligned with CIS Benchmarks):**

* Secure configuration management.
* Access control enforcement.
* Security auditing for infrastructure changes.

---

# 📊 Snowflake & DBT Metrics, Alerts, and GitHub Actions Dashboard

This guide explains how to:

* Collect **relevant pipeline metrics** from DBT & Snowflake.
* Automate **alerts** via Slack notifications for critical pipeline events.
* Generate and publish an automated **pipeline metrics dashboard** using GitHub Actions & GitHub Pages.

---

## ✅ **Metrics Collected**

| Source             | Metric                                               | Purpose                             |
| ------------------ | ---------------------------------------------------- | ----------------------------------- |
| **DBT Logs**       | Transformation duration, success rate, test outcomes | Monitor DBT job performance, health |
| **Snowflake**      | Query runtime, cost, error rate                      | Track warehouse usage, efficiency   |
| **GitHub Actions** | Deployment durations, success/failure rate           | Ensure CI/CD reliability            |

---

## 🚦 **Step-by-Step Implementation**

---

## 🔸 **1. Metrics Collection SQL (Snowflake)**

Create a View in your Snowflake Gold schema:

---

## 🔸 **2. DBT Metrics Extraction (GitHub Action)**

Workflow file: `.github/workflows/metrics_dashboard.yml`

This action runs daily, extracts DBT logs and Snowflake metrics, and publishes a dashboard.

---

## 📖 **4. Configure GitHub Pages**

* On your repository:

  * Navigate to **Settings → Pages**.
  * Set **Source** as `gh-pages` branch.
  * Your dashboard will be accessible via:
    `https://<your-github-username>.github.io/<your-repo>/dashboard.md`

---

## 🖥️ **Sample Dashboard Output**

```markdown
## DBT Metrics
- **Last Run Duration:** 35.4 seconds
- **Tests Passed:** 10
- **Tests Failed:** 0

## Snowflake Pipeline Metrics (Last 7 Days)

| RUN_DATE   | USER_NAME        | TOTAL_QUERIES | AVG_QUERY_DURATION_SEC | TOTAL_CREDITS_USED |
|------------|------------------|---------------|------------------------|--------------------|
| 2024-01-10 | DATAOPS_DBT_USER | 25            | 1.2                    | 0.015              |
| 2024-01-09 | DATAOPS_DBT_USER | 30            | 1.5                    | 0.017              |

## GitHub Actions Deployment Metrics
- **Last Deployment Status:** success
- **Last Deployment Time:** 2024-01-10 01:00:00 UTC
```

---

## 🔐 **Security Notes**

* All credentials and sensitive data are secured using GitHub repository secrets.
* No sensitive information exposed in logs or repository.

---

## 🔑 **Additional Resources and Reference**

* [FINOS CCC Primer](https://github.com/finos/common-cloud-controls/blob/main/docs/resources/training/FINOS-CCC-Primer-June-2024.pdf)
* [CIS Security Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
* [Snowflake Security Best Practices](https://docs.snowflake.com/en/user-guide/security-best-practices.html)
* [DBT Security & Governance](https://docs.getdbt.com/docs/security-and-governance)

---

## ✅ **Summary**

This consolidated document ensures clarity and consistency in your DataOps sandbox automation, integrating comprehensive CI/CD, security controls, observability, and alerting—all via GitHub Actions workflows.

---

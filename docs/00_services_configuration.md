# ⚙️ Services Configuration

## Intelligent Inventory Management DataOps Sandbox

This guide clearly outlines the initial configurations required to set up external services used in the Intelligent Inventory Management DataOps Sandbox.

---

## ✅ **Service Overview**

You'll configure these primary services:

* [DBT Cloud](#dbt-cloud-setup)
* [Snowflake](#snowflake-setup)
* [GitHub Repository](#github-setup)
* [Slack Integration](#slack-integration)

---

## 📋 **DBT Cloud Setup**

Follow these explicit steps to configure your DBT Cloud account:

1. Sign up at [DBT Cloud Signup](https://cloud.getdbt.com/signup).
2. Create a new workspace:

   * Choose Snowflake as your target warehouse.
   * Enter your Snowflake account credentials (below).
3. Create a new DBT Project named `logistics_demo`.

---

## ❄️ **Snowflake Setup**

Configure Snowflake explicitly for your sandbox:

1. Sign up for a free trial at [Snowflake Signup](https://signup.snowflake.com).
2. Log in to your Snowflake account and set up:

   * A warehouse named `LOGISTICS_WH`.
   * A role named `LOGISTICS_DBT_ROLE`.
   * A database named `LOGISTICS_DEMO`.
3. Run the initial DDL script provided in [snowflake\_setup.md](../docs/04_snowflake_setup.md).

**Credentials to Note:**

* Account ID
* Username & Password
* Role (`LOGISTICS_DBT_ROLE`)
* Warehouse (`LOGISTICS_WH`)

---

## 🔧 **GitHub Setup**

Ensure the following GitHub configurations explicitly for repository automation:

### 1. **Fork or Clone the Repository**

```bash
git clone <your-repository-url>
```

### 2. **GitHub Secrets**

Set these clearly defined secrets in your GitHub repository (`Settings > Secrets and Variables > Actions`):

| Secret Name           | Description                           |
| --------------------- | ------------------------------------- |
| `SNOWFLAKE_ACCOUNT`   | Your Snowflake Account ID             |
| `SNOWFLAKE_USER`      | Your Snowflake username               |
| `SNOWFLAKE_PASSWORD`  | Password for Snowflake user           |
| `SNOWFLAKE_ROLE`      | Snowflake role (`LOGISTICS_DBT_ROLE`) |
| `SNOWFLAKE_WAREHOUSE` | Warehouse (`LOGISTICS_WH`)            |
| `SLACK_WEBHOOK_URL`   | Slack webhook URL for notifications   |

### 3. **GitHub Pages Setup (Dashboard)**

* Activate GitHub Pages explicitly from `Settings > Pages`.
* Choose `gh-pages` branch as your deployment source.

---

## 🔔 **Slack Integration**

Slack integration provides real-time alerts clearly for observability and incidents.

1. Create a Slack workspace if you don't have one: [Slack Signup](https://slack.com/get-started).
2. Add an Incoming Webhook App:

   * Visit [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks).
   * Select a channel (e.g., `#dataops-alerts`) to receive notifications.
   * Copy and store the generated webhook URL.
3. Add this webhook URL explicitly as a secret (`SLACK_WEBHOOK_URL`) in your GitHub repository.

**Alerts you'll receive:**

* DBT pipeline failures
* Security audit failures (SAST)
* Dashboard generation errors

---

## 🗂️ **Final Checklist**

Before proceeding, confirm clearly that you have:

* [ ] DBT Cloud account and workspace set up.
* [ ] Snowflake account configured (Database, Role, Warehouse).
* [ ] GitHub repository secrets explicitly configured.
* [ ] Slack integration webhook set up and tested.

---

## 🚨 **Troubleshooting & Support**

If you encounter any issues:

* Verify credentials clearly for Snowflake and GitHub secrets.
* Ensure the Slack webhook URL is correctly configured.

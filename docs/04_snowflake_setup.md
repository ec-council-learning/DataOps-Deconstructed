# ❄️ Snowflake DDL – Dynamic Schema and Object Creation Based on GitHub Issue ID

This document outlines the Snowflake DDL setup required to dynamically generate schemas and tables based on the **GitHub Issue ID** provided by GitHub Actions.

## ✅ **Dynamic Schema and Object Creation**

### **Objective:**

* Automatically generate Snowflake schemas and tables using GitHub Issue IDs.
* Automatically grant necessary access for the roles managing DBT and Snowflake objects.

---

## 📌 **Snowflake Schema Creation Logic**

We will use the GitHub Issue ID to create schemas dynamically for different feature branches, clearly isolating them for each specific feature being worked on.

### **1. Create Schema with Dynamic Naming**

This statement uses the GitHub Issue ID (from environment variables) as a suffix for schema names. If no Issue ID is provided, it falls back to using a default schema name (`default_schema`).

---

### **2. Create Tables with Dynamic Naming**

The `GITHUB_ISSUE_ID` is used dynamically for table names. If a feature branch is tied to an issue ID, it will automatically generate tables with that issue ID as a suffix.

---

### **3. Automatically Grant Access to Roles**

After schema and table creation, we will ensure the **DataOps DBT roles** have the necessary permissions to access these objects.
* **Automatic permissions:** Each new schema and its objects will have the required access for the **LOGISTICS\_DBT\_ROLE** used in DBT.

---

## 🚦 **GitHub Actions Integration**

Ensure the `GITHUB_ISSUE_ID` environment variable is passed to Snowflake via GitHub Actions for dynamic object creation. The following snippet illustrates this in your GitHub Actions workflow (`dbt_ci_cd.yml`):

---

## ✅ **Summary**

With the newly defined Snowflake DDL:

* **Schemas and tables** are dynamically created based on the GitHub Issue ID.
* **Permissions** are automatically granted to DBT roles for the relevant objects.
* **GitHub Actions** automatically populates the `GITHUB_ISSUE_ID` for each feature branch, ensuring the environment is correctly named and isolated.

---

✅ **Commit Suggestion:**

```
docs(snowflake): add dynamic schema and table creation logic with GitHub Issue ID
```

---

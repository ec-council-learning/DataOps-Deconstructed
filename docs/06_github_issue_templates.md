# 📝 GitHub Issue Templates & Labels for Automation

## Logistics Demo – DBT and Snowflake Lifecycle Management

This document provides clearly defined GitHub issue templates and labels to automate the lifecycle (creation/deletion) of DBT/Snowflake objects based on GitHub issue workflows.

---

## ✅ **Key Benefits**

* Clearly structured workflows for object creation & cleanup.
* Automated schema and object lifecycle management.
* Enhanced collaboration and tracking.
* Precise automation with GitHub Actions.

---

## 📂 **Structure Overview**

```
.github/
└── ISSUE_TEMPLATE/
    ├── feature_request.yml
    └── cleanup_request.yml
```

## 📌 **1. Feature Request Template (`feature_request.yml`)**

Use this template to clearly initiate DBT/Snowflake object creation workflows:

## 📌 **2. Cleanup Request Template (`cleanup_request.yml`)**

Use this template to clearly trigger automated cleanup of obsolete DBT/Snowflake objects:

---

## 🔖 **GitHub Labels Definition**

Clearly define labels in your GitHub repository settings for precise automation:

| Label Name  | Description                                | Color                  |
| ----------- | ------------------------------------------ | ---------------------- |
| `feature`   | Creation of new DBT/Snowflake objects      | `#1d76db` (blue)       |
| `cleanup`   | Deletion of obsolete DBT/Snowflake objects | `#ff4242` (red)        |
| `dbt`       | DBT-specific changes                       | `#f78c0f` (orange)     |
| `snowflake` | Snowflake-specific changes                 | `#29abe2` (light blue) |

---

## ⚙️ **Automation Workflow (GitHub Actions)**

To fully automate schema/object creation and cleanup clearly based on issues, include this step into your existing DBT CI/CD workflow (`dbt_ci_cd.yml`):

**Example GitHub Actions snippet (add to existing workflow):**

```yaml
- name: Handle Feature Request Automation
  if: contains(github.event.issue.labels.*.name, 'feature')
  run: |
    FEATURE_NAME=$(jq -r '.issue.body' "$GITHUB_EVENT_PATH" | grep 'Schema/Object Name' | cut -d':' -f2 | xargs | tr '-' '_')
    echo "Automating creation of schema/object: $FEATURE_NAME"
    # Run DBT commands or Snowflake SQL via scripts to create the new schema/object
    # dbt run-operation create_schema --args '{schema_name: $FEATURE_NAME}'

- name: Handle Cleanup Automation
  if: contains(github.event.issue.labels.*.name, 'cleanup')
  run: |
    OBJECT_NAME=$(jq -r '.issue.body' "$GITHUB_EVENT_PATH" | grep 'Schema/Object Name to Delete' | cut -d':' -f2 | xargs | tr '-' '_')
    echo "Automating deletion of schema/object: $OBJECT_NAME"
    # Run DBT commands or Snowflake SQL via scripts to drop the schema/object
    # dbt run-operation drop_schema --args '{schema_name: $OBJECT_NAME}'
```

> **Note:** Create DBT macros (`create_schema`, `drop_schema`) for secure, controlled schema/object management.

---

## 🚨 **Slack Notifications (Optional Enhancement)**

Integrate Slack notifications clearly to inform teams of schema/object changes:

```yaml
- name: Slack Notify on Schema/Object Creation
  if: contains(github.event.issue.labels.*.name, 'feature')
  uses: slackapi/slack-github-action@v1.26.0
  with:
    payload: |
      {"text":"✅ Created schema/object: ${{ env.FEATURE_NAME }}"}
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
    SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK

- name: Slack Notify on Schema/Object Deletion
  if: contains(github.event.issue.labels.*.name, 'cleanup')
  uses: slackapi/slack-github-action@v1.26.0
  with:
    payload: |
      {"text":"🧹 Deleted schema/object: ${{ env.OBJECT_NAME }}"}
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
    SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK
```

---

## ✅ **Summary**

You now have:

* Structured GitHub issue templates clearly managing object lifecycle automation.
* Precise labels triggering automatic DBT/Snowflake schema/object management.
* Optional Slack notifications clearly communicating changes to teams.

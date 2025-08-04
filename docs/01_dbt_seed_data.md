# 📦 **Fulfillment Logistics Scenario: Intelligent Inventory Management with Dynamic DBT Seed Data**

## ✅ **Scenario Overview**

You operate a global fulfillment network managing diverse products across multiple warehouses. Your primary objective is to implement intelligent inventory management that optimizes stock levels, minimizes holding costs, and forecasts demand through historical data analysis.

To simulate realistic conditions, your pipeline uses dynamically generated data representing:

* **Products Master Data** (categories, dimensions, cost)
* **Warehouse Master Data** (locations, capacities, managers)
* **Inventory Movements** (stock replenishments, warehouse transfers, adjustments)
* **Customer Orders** (online, retail, wholesale channels)

These data points are dynamically generated and seeded into your DBT project to demonstrate a fully automated DataOps workflow explicitly.

---

## 🛠️ **Dynamic Seed Data Generation**

To provide realistic scenarios and flexible testing, seed data is dynamically generated via a Python script (`create_seed.py`) using the `faker` library.

**Generated Seed Data Files:**

| Seed File                 | DBT Schema    | Description                                           |
| ------------------------- | ------------- | ----------------------------------------------------- |
| `products.csv`            | `master_data` | Master product catalog with detailed attributes.      |
| `warehouses.csv`          | `master_data` | Information about warehouse locations and capacities. |
| `inventory_movements.csv` | `bronze`      | Daily transactional data on inventory movements.      |
| `customer_orders.csv`     | `bronze`      | Daily transactional customer order data.              |

### 📂 **DBT Seed Directory Structure**

```
scripts/dbt/seeds/
├── products.csv
├── warehouses.csv
├── inventory_movements.csv
└── customer_orders.csv
```

---

## ⚙️ **Explicit DBT Seeds Configuration**

Explicitly configured within `dbt_project.yml`:

```yaml
seeds:
  logistics_demo:
    products:
      +schema: master_data
    warehouses:
      +schema: master_data
    inventory_movements:
      +schema: bronze
    customer_orders:
      +schema: bronze
```

* Master data explicitly separated for clarity.
* Transactional data explicitly managed in the Bronze schema.

---

## 🚀 **Generating DBT Seed Data Explicitly**

Use the provided Python script to dynamically create realistic seed data:

```bash
cd scripts/python
pip install -r ../requirements.txt
python create_seed.py
```

Then explicitly load the seed data into Snowflake via DBT:

```bash
cd ../dbt
dbt seed --profiles-dir ./
```

---

## 🗃️ **How Seed Data is Leveraged in DBT Models**

Your dynamically generated seed data explicitly supports:

* **Bronze → Silver** transformations:

  * Data validation, enrichment, and integration with master data.
  * Creation of structured inventory and order snapshots.

* **Silver → Gold** transformations:

  * Aggregation of explicit daily and weekly inventory KPIs.
  * Calculation of essential metrics explicitly:

    * **Stock Turnover Rate**
    * **Warehouse Utilization**
    * **Sales Channel Efficiency**
    * **Demand Forecasting Metrics**

---

## 📈 **Example of Aggregated KPIs (Gold Layer)** *(Dynamic Data Example)*

| report\_date | warehouse\_name  | product\_name   | total\_orders | total\_units\_shipped | avg\_daily\_inventory | stock\_turnover\_ratio |
| ------------ | ---------------- | --------------- | ------------- | --------------------- | --------------------- | ---------------------- |
| 2024-01-09   | San Francisco FC | Ergonomic Chair | 45            | 120                   | 500                   | 0.24                   |
| 2024-01-09   | Frankfurt FC     | Yoga Mat        | 60            | 200                   | 400                   | 0.50                   |

*(Actual data explicitly generated dynamically)*

---

## 🎯 **Advantages of Explicit Dynamic Seed Data Generation**

* **Realistic** and varied datasets explicitly improve testing scenarios.
* **Scalable** approach: easily regenerate and adapt seed data explicitly.
* Clearly aligned with real-world scenarios, explicitly beneficial for DataOps learning.

---

## ✅ **Next Steps Explicitly Recommended**

After confirming this approach, explicitly move forward to:

* Execute your DBT pipeline explicitly via GitHub Actions (`dbt_ci_cd.yml`).
* Validate explicit data quality and pipeline integration.
* Leverage explicit dashboard generation for observability (`create_dashboard.py`).

---

## 🚨 **Important Explicit Note**

Ensure all Python dependencies are explicitly installed by executing:

```bash
pip install -r scripts/requirements.txt
```



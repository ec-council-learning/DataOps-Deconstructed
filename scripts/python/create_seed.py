import csv
import os
import random
from datetime import datetime, timedelta

from faker import Faker

# Importing typing for potential type annotations if needed.
# Removed invalid import of `None` alias as it caused syntax errors.


fake = Faker()

# Directory to store generated seed files
SEED_DIR = "../scripts/dbt/seeds/"
NUM_ROWS = 9999  # Use a plain integer to avoid lib2to3 parse issues with underscores.

# Ensure the seed directory exists
os.makedirs(SEED_DIR, exist_ok=True)


def generate_products() -> None:
    """Generate a products.csv file with synthetic product data."""
    categories = ["Electronics", "Sports", "Home & Kitchen", "Books", "Toys"]
    with open(os.path.join(SEED_DIR, "products.csv"), mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "product_id",
                "product_name",
                "category",
                "unit_cost",
                "weight_kg",
                "dimensions_cm",
            ]
        )
        for i in range(NUM_ROWS):
            product_id = f"PRD{i + 1:05d}"
            product_name = (
                f"{fake.unique.word().title()} "
                f"{random.choice(['Pro', 'Max', 'Lite', 'Standard'])}"
            )
            category = random.choice(categories)
            unit_cost = round(random.uniform(10.0, 500.0), 2)
            weight_kg = round(random.uniform(0.1, 20.0), 2)
            dimensions_cm = (
                f"{random.randint(5, 100)}x"
                f"{random.randint(5, 100)}x"
                f"{random.randint(5, 100)}"
            )
            writer.writerow(
                [
                    product_id,
                    product_name,
                    category,
                    unit_cost,
                    weight_kg,
                    dimensions_cm,
                ]
            )


def generate_warehouses() -> None:
    """Generate a warehouses.csv file with warehouse metadata."""
    with open(os.path.join(SEED_DIR, "warehouses.csv"), mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "warehouse_id",
                "warehouse_name",
                "location",
                "capacity_units",
                "manager_name",
            ]
        )
        for i in range(1, 21):  # 20 warehouses
            warehouse_id = f"WH{i:03d}"
            warehouse_name = f"{fake.city()} Warehouse"
            location = f"{fake.city()}, {fake.country_code()}"
            capacity_units = random.randint(5000, 100000)
            manager_name = fake.name()
            writer.writerow(
                [warehouse_id, warehouse_name, location, capacity_units, manager_name]
            )


def generate_inventory_movements() -> None:
    """Generate an inventory_movements.csv file with stock movement events."""
    movement_types = ["replenishment", "outbound", "adjustment"]
    with open(
        os.path.join(SEED_DIR, "inventory_movements.csv"), mode="w", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "movement_id",
                "product_id",
                "warehouse_id",
                "movement_date",
                "quantity",
                "movement_type",
            ]
        )
        for i in range(NUM_ROWS):
            movement_id = f"MV{i + 1:07d}"
            product_id = f"PRD{random.randint(1, NUM_ROWS):05d}"
            warehouse_id = f"WH{random.randint(1, 20):03d}"
            movement_date = (
                datetime.today() - timedelta(days=random.randint(0, 365))
            ).strftime("%Y-%m-%d")
            quantity = random.randint(-500, 1000)
            movement_type = random.choice(movement_types)
            writer.writerow(
                [
                    movement_id,
                    product_id,
                    warehouse_id,
                    movement_date,
                    quantity,
                    movement_type,
                ]
            )


def generate_customer_orders() -> None:
    """Generate a customer_orders.csv file with order data."""
    sales_channels = ["online", "retail", "wholesale"]
    with open(
        os.path.join(SEED_DIR, "customer_orders.csv"), mode="w", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "order_id",
                "product_id",
                "warehouse_id",
                "order_date",
                "quantity",
                "sales_channel",
            ]
        )
        for i in range(NUM_ROWS):
            order_id = f"ORD{i + 1:07d}"
            product_id = f"PRD{random.randint(1, NUM_ROWS):05d}"
            warehouse_id = f"WH{random.randint(1, 20):03d}"
            order_date = (
                datetime.today() - timedelta(days=random.randint(0, 365))
            ).strftime("%Y-%m-%d")
            quantity = random.randint(1, 50)
            sales_channel = random.choice(sales_channels)
            writer.writerow(
                [
                    order_id,
                    product_id,
                    warehouse_id,
                    order_date,
                    quantity,
                    sales_channel,
                ]
            )


def main() -> None:
    """Run all seed generation routines in sequence."""
    print("Generating products.csv...")
    generate_products()
    print("products.csv generated successfully.")

    print("Generating warehouses.csv...")
    generate_warehouses()
    print("warehouses.csv generated successfully.")

    print("Generating inventory_movements.csv...")
    generate_inventory_movements()
    print("inventory_movements.csv generated successfully.")

    print("Generating customer_orders.csv...")
    generate_customer_orders()
    print("customer_orders.csv generated successfully.")


if __name__ == "__main__":
    main()

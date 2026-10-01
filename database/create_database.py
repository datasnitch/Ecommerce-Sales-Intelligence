import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path


# PROJECT PATHS


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ecommerce.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

DATA_DIR.mkdir(exist_ok=True)



# CONNECT TO DATABASE


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# Enable foreign key relationships
cursor.execute("PRAGMA foreign_keys = ON")

print("Database connected successfully.")


# CREATE TABLES


with open(SCHEMA_PATH, "r") as file:
    schema = file.read()

cursor.executescript(schema)

print("Tables created successfully.")



# CLEAR OLD DATA


cursor.execute("DELETE FROM OrderItems")
cursor.execute("DELETE FROM Orders")
cursor.execute("DELETE FROM Products")
cursor.execute("DELETE FROM Customers")

print("Old data cleared.")


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

cities = [
    "Pune",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Nagpur",
    "Ahmedabad",
    "Jaipur"
]

customers = []

for customer_id in range(1, 1001):

    name = f"Customer {customer_id}"

    city = random.choice(cities)

    signup_date = datetime.now() - timedelta(
        days=random.randint(0, 730)
    )

    customers.append(
        (
            customer_id,
            name,
            city,
            signup_date.strftime("%Y-%m-%d")
        )
    )


cursor.executemany(
    """
    INSERT INTO Customers
    (
        customer_id,
        name,
        city,
        signup_date
    )
    VALUES (?, ?, ?, ?)
    """,
    customers
)

print(f"Customers inserted: {len(customers)}")


# GENERATE PRODUCTS


categories = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books",
    "Grocery",
    "Accessories"
]

products = []

for product_id in range(1, 151):

    category = random.choice(categories)

    product_name = f"{category} Product {product_id}"

    price = round(
        random.uniform(100, 50000),
        2
    )

    products.append(
        (
            product_id,
            product_name,
            category,
            price
        )
    )


cursor.executemany(
    """
    INSERT INTO Products
    (
        product_id,
        name,
        category,
        price
    )
    VALUES (?, ?, ?, ?)
    """,
    products
)

print(f"Products inserted: {len(products)}")



# GENERATE ORDERS AND ORDER ITEMS

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash on Delivery",
    "Net Banking"
]

# Generate 9 months of order data
start_date = datetime.now() - timedelta(days=270)

orders = []
order_items = []

order_id = 1
order_item_id = 1


for day in range(271):

    current_date = start_date + timedelta(days=day)

    # 15-40 orders every day
    daily_orders = random.randint(15, 40)

    for _ in range(daily_orders):

        customer_id = random.randint(1, 1000)

        payment_method = random.choice(
            payment_methods
        )

        discount = random.choice([
            0,
            0,
            0,
            5,
            10,
            15,
            20
        ])

        number_of_items = random.randint(1, 5)

        total_before_discount = 0

        temporary_items = []


        # ----------------------------------------------------
        # Generate products for this order
        # ----------------------------------------------------

        for _ in range(number_of_items):

            product_id = random.randint(1, 150)

            quantity = random.randint(1, 3)

            cursor.execute(
                """
                SELECT price
                FROM Products
                WHERE product_id = ?
                """,
                (product_id,)
            )

            product_price = cursor.fetchone()[0]

            price_at_purchase = round(
                product_price *
                random.uniform(0.90, 1.05),
                2
            )

            item_total = (
                quantity *
                price_at_purchase
            )

            total_before_discount += item_total

            temporary_items.append(
                (
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    price_at_purchase
                )
            )

            order_item_id += 1


        
        # Apply discount
        

        discount_amount = (
            total_before_discount *
            discount /
            100
        )

        final_amount = round(
            total_before_discount -
            discount_amount,
            2
        )


        
        # Store order
        

        orders.append(
            (
                order_id,
                customer_id,
                current_date.strftime("%Y-%m-%d"),
                payment_method,
                discount,
                final_amount
            )
        )

        order_items.extend(
            temporary_items
        )

        order_id += 1



# INSERT ORDERS


cursor.executemany(
    """
    INSERT INTO Orders
    (
        order_id,
        customer_id,
        order_date,
        payment_method,
        discount_applied,
        total_amount
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    orders
)

print(f"Orders inserted: {len(orders)}")


# INSERT ORDER ITEMS


cursor.executemany(
    """
    INSERT INTO OrderItems
    (
        order_item_id,
        order_id,
        product_id,
        quantity,
        price_at_purchase
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    order_items
)

print(f"Order items inserted: {len(order_items)}")



# SAVE DATABASE


conn.commit()

conn.close()



# FINAL MESSAGE


print()
print("=" * 60)
print("DATABASE CREATED SUCCESSFULLY")
print("=" * 60)

print(f"Database location: {DB_PATH}")

print()
print("Task 1 data generation completed.")
import sqlite3
from pathlib import Path


# Project path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ecommerce.db"


# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


print("=" * 60)
print("E-COMMERCE DATABASE VERIFICATION")
print("=" * 60)


# RECORD COUNTS


tables = [
    "Customers",
    "Products",
    "Orders",
    "OrderItems"
]

print("\nRecord Counts")
print("-" * 40)

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table:<15}: {count:,}")


# ORDER DATE RANGE

cursor.execute("""
    SELECT
        MIN(order_date),
        MAX(order_date)
    FROM Orders
""")

first_date, last_date = cursor.fetchone()

print("\nOrder Date Range")
print("-" * 40)

print("First Order:", first_date)
print("Last Order :", last_date)


# DISTINCT ORDER DAYS


cursor.execute("""
    SELECT COUNT(DISTINCT order_date)
    FROM Orders
""")

distinct_days = cursor.fetchone()[0]

print("\nDistinct Order Days")
print("-" * 40)

print("Days with orders:", distinct_days)


# TOTAL REVENUE


cursor.execute("""
    SELECT SUM(total_amount)
    FROM Orders
""")

total_revenue = cursor.fetchone()[0]

print("\nTotal Revenue")
print("-" * 40)

print(f"₹{total_revenue:,.2f}")


# CLOSE DATABASE

conn.close()


print("\n" + "=" * 60)
print("DATABASE VERIFICATION COMPLETED")
print("=" * 60)
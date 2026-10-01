import sqlite3
from pathlib import Path



# PROJECT PATHS


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "ecommerce.db"



# CONNECT TO DATABASE


conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


print("=" * 70)
print("E-COMMERCE SALES INTELLIGENCE")
print("TASK 1 - SQL QUERY RESULTS")
print("=" * 70)


# QUERY 1
# TOTAL REVENUE BY PRODUCT CATEGORY


print("\n")
print("=" * 70)
print("QUERY 1: TOTAL REVENUE BY PRODUCT CATEGORY")
print("=" * 70)

cursor.execute("""
    SELECT
        p.category,
        ROUND(
            SUM(oi.quantity * oi.price_at_purchase),
            2
        ) AS total_revenue
    FROM OrderItems oi
    JOIN Products p
        ON oi.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC;
""")


results = cursor.fetchall()


print(f"\n{'Category':<25} {'Revenue':>20}")
print("-" * 50)


for category, revenue in results:

    print(
        f"{category:<25} ₹{revenue:>18,.2f}"
    )



# QUERY 2
# TOP 10 BEST-SELLING PRODUCTS


print("\n")
print("=" * 70)
print("QUERY 2: TOP 10 BEST-SELLING PRODUCTS BY REVENUE")
print("=" * 70)


cursor.execute("""
    SELECT
        p.product_id,
        p.name,
        SUM(oi.quantity) AS units_sold,
        ROUND(
            SUM(
                oi.quantity * oi.price_at_purchase
            ),
            2
        ) AS revenue
    FROM OrderItems oi
    JOIN Products p
        ON oi.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.name
    ORDER BY revenue DESC
    LIMIT 10;
""")


results = cursor.fetchall()


print(
    f"\n{'ID':<6}"
    f"{'Product':<35}"
    f"{'Units':>10}"
    f"{'Revenue':>20}"
)

print("-" * 75)


for product_id, name, units, revenue in results:

    print(
        f"{product_id:<6}"
        f"{name:<35}"
        f"{units:>10}"
        f"₹{revenue:>18,.2f}"
    )



# QUERY 3
# MONTHLY ORDER COUNT AND REVENUE


print("\n")
print("=" * 70)
print("QUERY 3: MONTHLY ORDER COUNT AND REVENUE")
print("=" * 70)


cursor.execute("""
    SELECT
        strftime('%Y-%m', order_date) AS month,
        COUNT(order_id) AS order_count,
        ROUND(
            SUM(total_amount),
            2
        ) AS revenue
    FROM Orders
    GROUP BY month
    ORDER BY month;
""")


results = cursor.fetchall()


print(
    f"\n{'Month':<15}"
    f"{'Orders':>15}"
    f"{'Revenue':>25}"
)

print("-" * 55)


for month, order_count, revenue in results:

    print(
        f"{month:<15}"
        f"{order_count:>15,}"
        f"₹{revenue:>23,.2f}"
    )


# CLOSE DATABASE

conn.close()


print("\n")
print("=" * 70)
print("ALL 3 SQL QUERIES EXECUTED SUCCESSFULLY")
print("=" * 70)
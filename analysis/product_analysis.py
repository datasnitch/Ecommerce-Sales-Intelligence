import sqlite3

DB_PATH = "data/ecommerce.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# 1. PRODUCT PERFORMANCE ANALYSIS
# ============================================================

def product_performance():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.product_id,
            p.name,
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * oi.price_at_purchase), 2) AS revenue
        FROM Products p
        JOIN OrderItems oi
            ON p.product_id = oi.product_id
        GROUP BY
            p.product_id,
            p.name,
            p.category
        ORDER BY revenue DESC
        LIMIT 20;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + "=" * 110)
    print("TOP 20 PRODUCT PERFORMANCE")
    print("=" * 110)

    print(
        f"{'ID':<5} | "
        f"{'Product':<28} | "
        f"{'Category':<18} | "
        f"{'Units Sold':<12} | "
        f"Revenue"
    )

    print("-" * 110)

    for row in results:

        product_id = row[0]
        name = row[1]
        category = row[2]
        units_sold = row[3]
        revenue = row[4]

        print(
            f"{product_id:<5} | "
            f"{name:<28} | "
            f"{category:<18} | "
            f"{units_sold:<12} | "
            f"₹{revenue:,.2f}"
        )

    conn.close()


# ============================================================
# 2. CATEGORY PERFORMANCE ANALYSIS
# ============================================================

def category_performance():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            p.category,
            SUM(oi.quantity) AS units_sold,
            ROUND(
                SUM(oi.quantity * oi.price_at_purchase),
                2
            ) AS revenue
        FROM Products p
        JOIN OrderItems oi
            ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + "=" * 100)
    print("CATEGORY PERFORMANCE")
    print("=" * 100)

    print(
        f"{'Category':<20} | "
        f"{'Units Sold':<12} | "
        f"Revenue"
    )

    print("-" * 100)

    for row in results:

        category = row[0]
        units_sold = row[1]
        revenue = row[2]

        print(
            f"{category:<20} | "
            f"{units_sold:<12} | "
            f"₹{revenue:,.2f}"
        )

    conn.close()


# ============================================================
# 3. MONTHLY SALES PERFORMANCE
# ============================================================

def monthly_sales_performance():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            strftime('%Y-%m', o.order_date) AS month,
            COUNT(DISTINCT o.order_id) AS orders,
            SUM(oi.quantity) AS units_sold,
            ROUND(
                SUM(oi.quantity * oi.price_at_purchase),
                2
            ) AS revenue
        FROM Orders o
        JOIN OrderItems oi
            ON o.order_id = oi.order_id
        GROUP BY month
        ORDER BY month;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + "=" * 100)
    print("MONTHLY SALES PERFORMANCE")
    print("=" * 100)

    print(
        f"{'Month':<12} | "
        f"{'Orders':<10} | "
        f"{'Units Sold':<12} | "
        f"Revenue"
    )

    print("-" * 100)

    for row in results:

        month = row[0]
        orders = row[1]
        units_sold = row[2]
        revenue = row[3]

        print(
            f"{month:<12} | "
            f"{orders:<10} | "
            f"{units_sold:<12} | "
            f"₹{revenue:,.2f}"
        )

    conn.close()


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    product_performance()

    category_performance()

    monthly_sales_performance()
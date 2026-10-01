import sqlite3

DB_PATH = "data/ecommerce.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# 1. CUSTOMER PURCHASING BEHAVIOR
# ============================================================

def customer_summary():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            COUNT(o.order_id) AS order_count,
            ROUND(SUM(o.total_amount), 2) AS total_spending,
            ROUND(AVG(o.total_amount), 2) AS average_order_value
        FROM Customers c
        JOIN Orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.name,
            c.city
        ORDER BY total_spending DESC
        LIMIT 20;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + "=" * 100)
    print("CUSTOMER PURCHASING BEHAVIOR ANALYSIS")
    print("=" * 100)

    print(
        "ID | Customer | City | Orders | Total Spending | Average Order"
    )

    print("-" * 100)

    for row in results:

        customer_id = row[0]
        name = row[1]
        city = row[2]
        orders = row[3]
        spending = row[4]
        average_order = row[5]

        print(
            customer_id,
            "|",
            name,
            "|",
            city,
            "| Orders:",
            orders,
            "| Total: ₹",
            f"{spending:,.2f}",
            "| Average: ₹",
            f"{average_order:,.2f}"
        )

    conn.close()


# ============================================================
# 2. CITY-WISE PURCHASING BEHAVIOR
# ============================================================

def city_analysis():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            c.city,
            COUNT(DISTINCT c.customer_id) AS customers,
            COUNT(o.order_id) AS orders,
            ROUND(SUM(o.total_amount), 2) AS revenue,
            ROUND(AVG(o.total_amount), 2) AS average_order_value
        FROM Customers c
        JOIN Orders o
            ON c.customer_id = o.customer_id
        GROUP BY c.city
        ORDER BY revenue DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + "=" * 100)
    print("CITY-WISE PURCHASING BEHAVIOR")
    print("=" * 100)

    print(
        "City | Customers | Orders | Revenue | Average Order"
    )

    print("-" * 100)

    for row in results:

        city = row[0]
        customers = row[1]
        orders = row[2]
        revenue = row[3]
        average_order = row[4]

        print(
            city,
            "| Customers:",
            customers,
            "| Orders:",
            orders,
            "| Revenue: ₹",
            f"{revenue:,.2f}",
            "| Average: ₹",
            f"{average_order:,.2f}"
        )

    conn.close()


# ============================================================
# 3. CUSTOMER SEGMENTATION
# ============================================================

def customer_segmentation():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            ROUND(SUM(o.total_amount), 2) AS total_spending,

            CASE
                WHEN SUM(o.total_amount) >= 2000000
                    THEN 'High Value'

                WHEN SUM(o.total_amount) >= 1000000
                    THEN 'Medium Value'

                ELSE 'Low Value'
            END AS customer_segment

        FROM Customers c

        JOIN Orders o
            ON c.customer_id = o.customer_id

        GROUP BY
            c.customer_id,
            c.name,
            c.city

        ORDER BY total_spending DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n" + "=" * 100)
    print("CUSTOMER SEGMENTATION")
    print("=" * 100)

    print(
        "ID | Customer | City | Total Spending | Segment"
    )

    print("-" * 100)

    for row in results:

        customer_id = row[0]
        name = row[1]
        city = row[2]
        spending = row[3]
        segment = row[4]

        print(
            customer_id,
            "|",
            name,
            "|",
            city,
            "| Spending: ₹",
            f"{spending:,.2f}",
            "|",
            segment
        )

    conn.close()


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    customer_summary()

    city_analysis()

    customer_segmentation()
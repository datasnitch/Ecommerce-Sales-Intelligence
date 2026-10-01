from flask import Flask, render_template
import sqlite3
import os
import json
import pandas as pd
from sklearn.linear_model import LinearRegression


app = Flask(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "ecommerce.db"
)

FORECAST_FILE = os.path.join(
    BASE_DIR,
    "static",
    "forecast_data.json"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# GENERATE PRODUCT FORECAST
# ============================================================

def generate_forecast(product_id=107):

    conn = get_connection()

    # --------------------------------------------------------
    # GET PRODUCT DETAILS
    # --------------------------------------------------------

    product_query = """
        SELECT
            name,
            category
        FROM Products
        WHERE product_id = ?
    """

    product = conn.execute(
        product_query,
        (product_id,)
    ).fetchone()

    if product is None:

        conn.close()

        return {
            "product_id": product_id,
            "product_name": "Unknown Product",
            "category": "Unknown",
            "historical_months": [],
            "historical_sales": [],
            "future_months": [],
            "forecast_sales": []
        }


    # --------------------------------------------------------
    # GET MONTHLY SALES
    # --------------------------------------------------------

    sales_query = """
        SELECT
            strftime('%Y-%m', o.order_date) AS month,
            SUM(oi.quantity) AS units_sold
        FROM Orders o
        JOIN OrderItems oi
            ON o.order_id = oi.order_id
        WHERE oi.product_id = ?
        GROUP BY strftime('%Y-%m', o.order_date)
        ORDER BY month
    """

    sales = conn.execute(
        sales_query,
        (product_id,)
    ).fetchall()

    conn.close()


    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not sales:

        return {
            "product_id": product_id,
            "product_name": product["name"],
            "category": product["category"],
            "historical_months": [],
            "historical_sales": [],
            "future_months": [],
            "forecast_sales": []
        }


    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------

    df = pd.DataFrame(
        [
            {
                "month": row["month"],
                "units_sold": row["units_sold"]
            }
            for row in sales
        ]
    )


    # --------------------------------------------------------
    # CLEAN DATA
    # --------------------------------------------------------

    df["units_sold"] = pd.to_numeric(
        df["units_sold"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["units_sold"]
    )

    df["month"] = pd.to_datetime(
        df["month"]
    )

    df = df.sort_values(
        "month"
    ).reset_index(drop=True)


    # --------------------------------------------------------
    # HISTORICAL DATA
    # --------------------------------------------------------

    historical_months = [
        date.strftime("%Y-%m")
        for date in df["month"]
    ]

    historical_sales = [
        int(round(value))
        for value in df["units_sold"]
    ]


    # ========================================================
    # MACHINE LEARNING FORECAST
    # ========================================================

    # Month number for ML
    df["month_number"] = range(
        1,
        len(df) + 1
    )


    X = df[
        ["month_number"]
    ]

    y = df[
        "units_sold"
    ]


    # --------------------------------------------------------
    # LINEAR REGRESSION
    # --------------------------------------------------------

    model = LinearRegression()

    model.fit(
        X,
        y
    )


    # --------------------------------------------------------
    # NEXT 3 MONTHS
    # --------------------------------------------------------

    future_numbers = [
        len(df) + 1,
        len(df) + 2,
        len(df) + 3
    ]

    future_X = pd.DataFrame({
        "month_number": future_numbers
    })


    predictions = model.predict(
        future_X
    )


    # --------------------------------------------------------
    # PREVENT NEGATIVE FORECAST
    # --------------------------------------------------------

    forecast_sales = [
        max(
            0,
            round(float(value))
        )
        for value in predictions
    ]


    # --------------------------------------------------------
    # FUTURE MONTH NAMES
    # --------------------------------------------------------

    last_month = df["month"].max()

    future_dates = pd.date_range(
        start=last_month + pd.DateOffset(months=1),
        periods=3,
        freq="MS"
    )

    future_months = [
        date.strftime("%Y-%m")
        for date in future_dates
    ]


    # ========================================================
    # FORECAST RESULT
    # ========================================================

    forecast_data = {

        "product_id": product_id,

        "product_name": product["name"],

        "category": product["category"],

        "historical_months":
            historical_months,

        "historical_sales":
            historical_sales,

        "future_months":
            future_months,

        "forecast_sales":
            forecast_sales
    }


    # ========================================================
    # SAVE FORECAST JSON
    # ========================================================

    try:

        with open(
            FORECAST_FILE,
            "w"
        ) as file:

            json.dump(
                forecast_data,
                file,
                indent=4
            )

    except Exception as error:

        print(
            f"Warning: Could not save forecast JSON: {error}"
        )


    return forecast_data


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    conn = get_connection()

    # ========================================================
    # KPI 1 - TOTAL CUSTOMERS
    # ========================================================

    total_customers = conn.execute("""
        SELECT COUNT(*) AS total_customers
        FROM Customers
    """).fetchone()["total_customers"]


    # ========================================================
    # KPI 2 - TOTAL ORDERS
    # ========================================================

    total_orders = conn.execute("""
        SELECT COUNT(*) AS total_orders
        FROM Orders
    """).fetchone()["total_orders"]


    # ========================================================
    # KPI 3 - TOTAL REVENUE
    # ========================================================

    total_revenue = conn.execute("""
        SELECT
            COALESCE(
                ROUND(SUM(total_amount), 2),
                0
            ) AS total_revenue
        FROM Orders
    """).fetchone()["total_revenue"]


    # ========================================================
    # KPI 4 - TOTAL PRODUCTS
    # ========================================================

    total_products = conn.execute("""
        SELECT COUNT(*) AS total_products
        FROM Products
    """).fetchone()["total_products"]


    # ========================================================
    # MONTHLY SALES
    # ========================================================

    monthly_sales = conn.execute("""
        SELECT
            strftime('%Y-%m', order_date) AS month,
            COUNT(order_id) AS orders,
            ROUND(SUM(total_amount), 2) AS revenue
        FROM Orders
        GROUP BY strftime('%Y-%m', order_date)
        ORDER BY month
    """).fetchall()


    # ========================================================
    # CATEGORY PERFORMANCE
    # ========================================================

    category_sales = conn.execute("""
        SELECT
            p.category,

            SUM(oi.quantity) AS units_sold,

            ROUND(
                SUM(
                    oi.quantity *
                    oi.price_at_purchase
                ),
                2
            ) AS revenue

        FROM Products p

        JOIN OrderItems oi
            ON p.product_id = oi.product_id

        GROUP BY p.category

        ORDER BY revenue DESC
    """).fetchall()


    # ========================================================
    # TOP 10 PRODUCTS
    # ========================================================

    top_products = conn.execute("""
        SELECT
            p.product_id,
            p.name,
            p.category,

            SUM(oi.quantity) AS units_sold,

            ROUND(
                SUM(
                    oi.quantity *
                    oi.price_at_purchase
                ),
                2
            ) AS revenue

        FROM Products p

        JOIN OrderItems oi
            ON p.product_id = oi.product_id

        GROUP BY
            p.product_id,
            p.name,
            p.category

        ORDER BY revenue DESC

        LIMIT 10
    """).fetchall()


    conn.close()


    # ========================================================
    # GENERATE FORECAST
    # ========================================================

    forecast = generate_forecast(
        product_id=107
    )


    # ========================================================
    # PREPARE MONTHLY CHART DATA
    # ========================================================

    monthly_labels = [
        row["month"]
        for row in monthly_sales
    ]

    monthly_revenue = [
        row["revenue"] or 0
        for row in monthly_sales
    ]

    monthly_orders = [
        row["orders"] or 0
        for row in monthly_sales
    ]


    # ========================================================
    # PREPARE CATEGORY CHART DATA
    # ========================================================

    category_labels = [
        row["category"]
        for row in category_sales
    ]

    category_revenue = [
        row["revenue"] or 0
        for row in category_sales
    ]


    # ========================================================
    # RENDER DASHBOARD
    # ========================================================

    return render_template(

        "dashboard.html",

        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------

        total_customers=total_customers,

        total_orders=total_orders,

        total_revenue=total_revenue,

        total_products=total_products,


        # ----------------------------------------------------
        # TABLES
        # ----------------------------------------------------

        monthly_sales=monthly_sales,

        category_sales=category_sales,

        top_products=top_products,


        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        monthly_labels=monthly_labels,

        monthly_revenue=monthly_revenue,

        monthly_orders=monthly_orders,

        category_labels=category_labels,

        category_revenue=category_revenue,


        # ----------------------------------------------------
        # FORECAST
        # ----------------------------------------------------

        forecast=forecast
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
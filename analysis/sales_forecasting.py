import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "ecommerce.db"
)

STATIC_DIR = os.path.join(
    PROJECT_ROOT,
    "static"
)

os.makedirs(STATIC_DIR, exist_ok=True)


# ============================================================
# PRODUCT SALES FORECASTING
# ============================================================

def product_sales_forecast(product_id):

    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    conn = sqlite3.connect(DB_PATH)

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

    df = pd.read_sql_query(
        sales_query,
        conn,
        params=(product_id,)
    )

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

    product_df = pd.read_sql_query(
        product_query,
        conn,
        params=(product_id,)
    )

    conn.close()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df.empty:
        print("No sales data found for this product.")
        return

    if product_df.empty:
        print("Product not found.")
        return

    # --------------------------------------------------------
    # PRODUCT INFORMATION
    # --------------------------------------------------------

    product_name = product_df.iloc[0]["name"]
    category = product_df.iloc[0]["category"]

    # --------------------------------------------------------
    # CLEAN SALES DATA
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

    # --------------------------------------------------------
    # SORT BY MONTH
    # --------------------------------------------------------

    df = df.sort_values(
        "month"
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # DISPLAY INFORMATION
    # --------------------------------------------------------

    print("\n" + "=" * 100)
    print("PRODUCT SALES FORECASTING")
    print("=" * 100)

    print(f"Product ID : {product_id}")
    print(f"Product    : {product_name}")
    print(f"Category   : {category}")

    print("\nHistorical Monthly Sales")
    print("-" * 100)

    display_df = df.copy()

    display_df["month"] = display_df[
        "month"
    ].dt.strftime("%Y-%m")

    print(
        display_df[
            ["month", "units_sold"]
        ].to_string(index=False)
    )

    # ========================================================
    # PREPARE MACHINE LEARNING DATA
    # ========================================================

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

    # ========================================================
    # LINEAR REGRESSION MODEL
    # ========================================================

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    # ========================================================
    # NEXT 3 MONTHS
    # ========================================================

    future_month_numbers = [
        len(df) + 1,
        len(df) + 2,
        len(df) + 3
    ]

    future_X = pd.DataFrame({
        "month_number":
            future_month_numbers
    })

    predictions = model.predict(
        future_X
    )

    # --------------------------------------------------------
    # PREVENT NEGATIVE SALES
    # --------------------------------------------------------

    predictions = [
        max(
            0,
            round(float(value))
        )
        for value in predictions
    ]

    # ========================================================
    # CREATE ACTUAL FUTURE MONTH LABELS
    # ========================================================

    last_month = df["month"].max()

    future_dates = pd.date_range(
        start=last_month + pd.DateOffset(months=1),
        periods=3,
        freq="MS"
    )

    future_labels = [
        date.strftime("%Y-%m")
        for date in future_dates
    ]

    # ========================================================
    # PRINT FORECAST
    # ========================================================

    print("\n" + "=" * 100)
    print("NEXT 3 MONTH SALES FORECAST")
    print("=" * 100)

    for month, prediction in zip(
        future_labels,
        predictions
    ):

        print(
            f"{month}: "
            f"Predicted Units Sold = {prediction}"
        )

    # ========================================================
    # CREATE FORECAST GRAPH
    # ========================================================

    print("\nCreating forecast graph...")

    plt.figure(
        figsize=(12, 6),
        dpi=150
    )

    # --------------------------------------------------------
    # HISTORICAL SALES
    # --------------------------------------------------------

    historical_x = list(
        range(
            1,
            len(df) + 1
        )
    )

    plt.plot(
        historical_x,
        df["units_sold"].tolist(),
        marker="o",
        linewidth=2,
        label="Historical Sales"
    )

    # --------------------------------------------------------
    # FORECAST SALES
    # --------------------------------------------------------

    plt.plot(
        future_month_numbers,
        predictions,
        marker="o",
        linestyle="--",
        linewidth=2,
        label="Forecast"
    )

    # --------------------------------------------------------
    # X AXIS LABELS
    # --------------------------------------------------------

    historical_labels = [
        date.strftime("%Y-%m")
        for date in df["month"]
    ]

    x_positions = (
        historical_x
        + future_month_numbers
    )

    x_labels = (
        historical_labels
        + future_labels
    )

    plt.xticks(
        x_positions,
        x_labels,
        rotation=45
    )

    # --------------------------------------------------------
    # TITLES
    # --------------------------------------------------------

    plt.title(
        f"Sales Forecast - {product_name}",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Month",
        fontsize=12
    )

    plt.ylabel(
        "Units Sold",
        fontsize=12
    )

    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    plt.grid(
        True,
        linestyle="--",
        alpha=0.3
    )

    # --------------------------------------------------------
    # LEGEND
    # --------------------------------------------------------

    plt.legend()

    # --------------------------------------------------------
    # LAYOUT
    # --------------------------------------------------------

    plt.tight_layout()

    # ========================================================
    # SAVE GRAPH
    # ========================================================

    output_file = os.path.join(
        STATIC_DIR,
        f"product_{product_id}_forecast.png"
    )

    plt.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close()

    # ========================================================
    # VERIFY FILE
    # ========================================================

    if os.path.exists(output_file):

        file_size = os.path.getsize(
            output_file
        )

        print(
            "\nForecast graph saved as:"
        )

        print(
            output_file
        )

        print(
            f"File size: {file_size:,} bytes"
        )

    else:

        print(
            "\nERROR: Forecast graph "
            "was not created."
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    product_sales_forecast(107)
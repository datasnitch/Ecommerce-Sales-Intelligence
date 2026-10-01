
# E-Commerce Sales Intelligence Platform

An end-to-end **E-Commerce Sales Intelligence and Analytics Platform** built using **Python, SQL, SQLite, Flask, Pandas, Scikit-learn, Matplotlib, HTML, and CSS**.

The platform analyzes customer, order, product, category, and sales data and presents the results through an interactive web dashboard. It also uses **Linear Regression** to forecast product sales for the next three months.

---

## 📌 Project Overview

The E-Commerce Sales Intelligence Platform is designed to convert raw e-commerce transaction data into meaningful business insights.

The system provides:

- Sales and revenue analysis
- Customer and order analysis
- Product performance analysis
- Category-wise revenue analysis
- Monthly sales trends
- Top-selling product analysis
- Product-level sales forecasting
- Interactive dashboard visualization

---

## 🎯 Objectives

The main objectives of this project are:

1. Analyze e-commerce sales and transaction data.
2. Identify top-performing products and categories.
3. Analyze monthly revenue and order trends.
4. Understand product sales performance.
5. Generate business insights using SQL queries.
6. Forecast future product sales using Machine Learning.
7. Present analytical results through a web-based dashboard.

---

## 🚀 Key Features

### 📊 Sales Dashboard

The dashboard provides important KPIs including:

- Total Customers
- Total Orders
- Total Revenue
- Total Products

### 📈 Monthly Sales Analysis

Analyzes monthly:

- Revenue
- Number of Orders
- Sales trends

### 🛍️ Category Performance

Displays category-wise:

- Units Sold
- Revenue
- Revenue contribution

### 🏆 Top 10 Best-Selling Products

Identifies the top 10 products based on revenue.

The table includes:

- Product
- Category
- Units Sold
- Revenue
- Rank

### 🔮 Sales Forecasting

The project uses **Linear Regression** to forecast product sales for the next 3 months.

For example:

**Product:** Books Product 107

The model uses historical monthly sales data and predicts future units sold.

### 📉 Forecast Visualization

The system generates a graph containing:

- Historical Sales
- Forecast Sales
- Monthly sales trend
- Next 3-month prediction

---

## 🧠 Machine Learning

### Algorithm Used

**Linear Regression**

The model uses the month number as the independent variable and units sold as the dependent variable.

### Input

Historical monthly product sales.

### Output

Predicted sales for the next 3 months.

### Example

```text
Historical Sales
2026-01 → 31
2026-02 → 32
2026-03 → 45
2026-04 → 53
...

Forecast
Future Month 1 → 24
Future Month 2 → 22
Future Month 3 → 21

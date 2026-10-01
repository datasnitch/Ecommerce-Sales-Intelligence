# E-Commerce Sales Intelligence Platform

**MSc Data Science & Big Data Analytics — Mini Project**

**Name:** Akash Jadhav  
**University:** MIT World Peace University, Pune

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

**Example Product:** Books Product 107

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

The model uses the **month number** as the independent variable and **units sold** as the dependent variable.

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
```

---

## 🗄️ Database

The project uses **SQLite** for storing and querying e-commerce data.

### Main Tables

```text
Customers
Products
Orders
OrderItems
```

### Database Relationship

```text
Customers
    │
    │ customer_id
    ▼
Orders
    │
    │ order_id
    ▼
OrderItems
    │
    │ product_id
    ▼
Products
```

SQL is used to perform analysis such as:

- Total customers
- Total orders
- Total revenue
- Total products
- Monthly revenue
- Monthly orders
- Category-wise revenue
- Product sales
- Top 10 products

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **SQL** | Data querying and analysis |
| **SQLite** | Database management |
| **Pandas** | Data processing and analysis |
| **Scikit-learn** | Machine Learning |
| **Linear Regression** | Sales forecasting |
| **Matplotlib** | Forecast visualization |
| **Flask** | Web application |
| **HTML** | Dashboard structure |
| **CSS** | Dashboard styling |
| **Git & GitHub** | Version control |

---

## 📁 Project Structure

```text
Ecommerce-Sales-Intelligence/
│
├── analysis/
│   └── sales_forecasting.py
│
├── data/
│   └── ecommerce.db
│
├── database/
│   └── queries.sql
│
├── static/
│   ├── forecast_data.json
│   ├── product_107_forecast.png
│   └── sales_forecast.png
│
├── templates/
│   └── dashboard.html
│
├── app.py
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/datasnitch/Ecommerce-Sales-Intelligence.git
```

```bash
cd Ecommerce-Sales-Intelligence
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

Activate the environment:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install flask pandas matplotlib scikit-learn
```

---

## ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The E-Commerce Sales Intelligence dashboard will be displayed in the browser.

---

## 🔮 Run Sales Forecasting

To generate the product sales forecast:

```bash
python analysis/sales_forecasting.py
```

The script:

1. Connects to the SQLite database.
2. Retrieves monthly product sales.
3. Prepares the Machine Learning dataset.
4. Trains the Linear Regression model.
5. Predicts the next 3 months.
6. Generates the forecast graph.
7. Saves the graph in the `static` directory.

---

## 📊 Dashboard Sections

The dashboard contains:

```text
E-Commerce Sales Intelligence
│
├── Total Customers
├── Total Orders
├── Total Revenue
├── Total Products
│
├── Monthly Revenue
├── Revenue by Category
├── Monthly Orders
│
├── Sales Forecast
│
└── Top 10 Best-Selling Products
```

---

## 🔍 Key SQL Analysis

### Revenue by Category

```sql
SELECT
    p.category,
    SUM(oi.quantity * oi.price_at_purchase) AS revenue
FROM Products p
JOIN OrderItems oi
    ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```

### Top 10 Products

```sql
SELECT
    p.product_id,
    p.name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.price_at_purchase) AS revenue
FROM Products p
JOIN OrderItems oi
    ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.name,
    p.category
ORDER BY revenue DESC
LIMIT 10;
```

### Monthly Sales

```sql
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(order_id) AS orders,
    SUM(total_amount) AS revenue
FROM Orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;
```

---

## 💡 Business Insights

The platform can help answer questions such as:

- What is the total revenue?
- How many orders have been placed?
- Which categories generate the most revenue?
- Which products are selling the most?
- How are monthly sales changing?
- What are the expected sales for a product in the next 3 months?

---

## 🔮 Future Enhancements

Possible future improvements include:

- Advanced time-series forecasting
- Forecasting for multiple products
- Customer segmentation
- Customer Lifetime Value analysis
- Sales anomaly detection
- Product recommendation system
- Interactive dashboard filters
- Automated business reports
- Cloud deployment

---

## 👨‍💻 Author

**Akash Jadhav**

**MSc Data Science & Big Data Analytics**  
**MIT World Peace University, Pune**

### GitHub

https://github.com/datasnitch

---

## 📄 Project Information

**Project:** E-Commerce Sales Intelligence Platform  
**Program:** MSc Data Science & Big Data Analytics  
**Project Type:** Mini Project  
**Academic Institution:** MIT World Peace University, Pune

---

## 📜 License

This project is developed for **academic and educational purposes**.

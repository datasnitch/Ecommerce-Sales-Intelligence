    
-- QUERY 1: TOTAL REVENUE BY PRODUCT CATEGORY

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



-- QUERY 2: TOP 10 BEST-SELLING PRODUCTS BY REVENUE


SELECT
    p.product_id,
    p.name,
    SUM(oi.quantity) AS units_sold,
    ROUND(
        SUM(oi.quantity * oi.price_at_purchase),
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


-- QUERY 3: MONTHLY ORDER COUNT AND REVENUE


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
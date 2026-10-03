-- Required SQL queries for the hackathon
-- Revenue uses: unit_price * quantity * (1 - discount)
-- Returned orders are excluded from net revenue.

-- 1. Total net revenue
SELECT ROUND(SUM(unit_price * quantity * (1 - discount)), 2) AS total_net_revenue
FROM orders
WHERE returned = 0 AND unit_price > 0 AND quantity > 0;

-- 2. Top 10 customers by total spending
SELECT c.customer_name, c.city,
       COUNT(DISTINCT o.order_id) AS number_of_orders,
       ROUND(SUM(o.unit_price * o.quantity * (1 - o.discount)), 2) AS total_spending
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.returned = 0 AND o.unit_price > 0 AND o.quantity > 0
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_spending DESC
LIMIT 10;

-- 3. Category-wise revenue, order count and quantity sold
SELECT TRIM(p.category) AS category,
       ROUND(SUM(o.unit_price * o.quantity * (1 - o.discount)), 2) AS revenue,
       COUNT(DISTINCT o.order_id) AS order_count,
       SUM(o.quantity) AS quantity_sold
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.returned = 0 AND o.unit_price > 0 AND o.quantity > 0
GROUP BY p.category
ORDER BY revenue DESC;

-- 4. Monthly net revenue trend
SELECT strftime('%Y-%m', order_date) AS month,
       ROUND(SUM(unit_price * quantity * (1 - discount)), 2) AS net_revenue
FROM orders
WHERE returned = 0 AND unit_price > 0 AND quantity > 0
  AND date(order_date) IS NOT NULL
GROUP BY month
ORDER BY month;

-- 5. Top 5 products by net revenue
SELECT p.product_name, TRIM(p.category) AS category,
       ROUND(SUM(o.unit_price * o.quantity * (1 - o.discount)), 2) AS net_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.returned = 0 AND o.unit_price > 0 AND o.quantity > 0
GROUP BY p.product_id, p.product_name, p.category
ORDER BY net_revenue DESC
LIMIT 5;

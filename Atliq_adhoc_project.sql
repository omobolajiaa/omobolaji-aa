## SQL Project - Answering Atliq Hardware Key Stakeholders Business Queries
USE gdb023;

## 1. List of markets in which customer "Atliq Exclusive" operates its business in the APAC region.

SELECT 
    customer, market
FROM
    dim_customer
WHERE
    customer = 'Atliq Exclusive'
        AND region = 'APAC'
GROUP BY market;

## 2. The percentage of unique product increase in 2021 vs. 2020.

WITH CTE AS (
	SELECT 
		COUNT(DISTINCT CASE
				WHEN fiscal_year = 2020 THEN p.product
			END) AS unique_products_2020,
		COUNT(DISTINCT CASE
				WHEN fiscal_year = 2021 THEN p.product
			END) AS unique_products_2021
	FROM
		dim_product p
			JOIN
		fact_sales_monthly s ON p.product_code = s.product_code)
	SELECT 
		*,
		ROUND(((unique_products_2021/unique_products_2020) - 1) * 100,2) AS percentage_change
	FROM
		CTE;

## 3. Unique product counts for each segment.

SELECT 
    segment, 
    COUNT(DISTINCT product) AS product_count
FROM
    dim_product
GROUP BY 
	segment
ORDER BY
	product_count DESC;

## 4. Segment with the most increase in unique products in 2021 vs 2020.

WITH CTE1 AS (
	SELECT 
		p.segment,
		COUNT(DISTINCT CASE
				WHEN fiscal_year = 2020 THEN p.product
			END) AS product_count_2020,
		COUNT(DISTINCT CASE
				WHEN fiscal_year = 2021 THEN p.product
			END) AS product_count_2021
	FROM
		dim_product p
			JOIN
		fact_sales_monthly s ON p.product_code = s.product_code
	GROUP BY 
		p.segment)
	SELECT 
		*,
		product_count_2021 - product_count_2020 AS difference
	FROM
		CTE1
	ORDER BY 
		difference DESC;

## 5. Products with highest and lowest manufacturing costs.

WITH manufacturing_cost AS (
	SELECT 
		p.product_code,
		p.product,
		manufacturing_cost
	FROM
		dim_product p
		JOIN fact_manufacturing_cost m 
		ON m.product_code = p.product_code),
	min_max_costs AS(
	SELECT
		MIN(manufacturing_cost) AS min_cost,
		MAX(manufacturing_cost) AS max_cost
	FROM
		fact_manufacturing_cost
	)
	SELECT
		mc.product_code,
		mc.product,
		mc.manufacturing_cost
	FROM
		manufacturing_cost mc
		JOIN min_max_costs mm
		ON mc.manufacturing_cost = mm.min_cost
		OR mc.manufacturing_cost = mm.max_cost
	ORDER BY mc.manufacturing_cost DESC;

## 6. Top 5 Customers who received an average high pre-invoice-discount-pct for the fiscal year 2021 in India.

SELECT 
    c.customer_code,
    c.customer,
    ROUND(AVG(pre_invoice_discount_pct), 2) AS average_discount_percentage
FROM
    dim_customer c
        JOIN
    fact_pre_invoice_deductions pre ON c.customer_code = pre.customer_code
WHERE
    fiscal_year = 2021 AND market = 'India'
GROUP BY c.customer , c.customer_code
ORDER BY average_discount_percentage DESC
LIMIT 5;

## 7. Gross monthly sales for Atliq Exclusive

WITH Atliq_exclusive_data AS(
	SELECT 
		c.customer_code, 
		c.customer, 
		date,
		gross_price,
		sold_quantity, 
		s.fiscal_year,
		gross_price * sold_quantity AS gross_sales_amount
	FROM
		fact_sales_monthly s
		JOIN fact_gross_price gp ON s.product_code = gp.product_code
			AND s.fiscal_year = gp.fiscal_year
		JOIN dim_customer c ON c.customer_code = s.customer_code
	WHERE customer = "Atliq Exclusive")
	SELECT
		MONTHNAME(date) AS month,
		YEAR(date) AS year,
		ROUND(SUM(gross_sales_amount),2) AS gross_sales_amount
	FROM 
		Atliq_exclusive_data
	GROUP BY month, year;

## 8. Maximum total sold quantity by quarter in 2020

SELECT 
    QUARTER(date) AS Quarter,
    YEAR(date) AS Year,
    SUM(sold_quantity) AS total_sold_quantity
FROM
    fact_sales_monthly
WHERE
    YEAR(date) = 2020
GROUP BY Quarter , Year
ORDER BY total_sold_quantity DESC;

## 9. Channels percentage contribution to gross sales in FS 2021	

WITH All_data AS(
	SELECT 
		c.customer_code, 
		c.channel,
		gross_price,
		sold_quantity, 
		s.fiscal_year,
		gross_price * sold_quantity AS gross_sales_amount
	FROM
		fact_sales_monthly s
		JOIN fact_gross_price gp ON s.product_code = gp.product_code
			AND s.fiscal_year = gp.fiscal_year
		JOIN dim_customer c ON c.customer_code = s.customer_code
	WHERE s.fiscal_year = 2021),
	channel_sales AS (
	SELECT
		channel,
		ROUND(SUM(gross_sales_amount)/1000000,2) AS gross_sales_mln
	FROM 
		All_data
	GROUP BY channel)
	SELECT 
		channel,
		gross_sales_mln,
		ROUND(gross_sales_mln/SUM(gross_sales_mln) OVER () * 100, 2) AS percentage_contribution
	FROM
		channel_sales
	ORDER BY percentage_contribution DESC;

## 10. Top 3 products  in each product division based on total_sold_quantity in FS 2021

WITH FS_2021_data AS (
	SELECT 
		p.product_code,
		division,
		product,
		SUM(sold_quantity) AS total_sold_quantity
	FROM
		dim_product p
		JOIN fact_sales_monthly s ON p.product_code = s.product_code
	WHERE fiscal_year = 2021
    GROUP BY division, p.product_code, product
),
	ranked_data AS (
    SELECT
		*,
        DENSE_RANK() OVER(PARTITION BY division ORDER BY total_sold_quantity DESC) AS ranking
	FROM
		FS_2021_data
)
	SELECT
		*
	FROM
		ranked_data
	WHERE ranking <=3;
    

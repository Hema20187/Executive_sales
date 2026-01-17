# Executive Sales and Customers

# Project Overview
This Executive Sales and Customer Analysis project evaluates how overall sales are contributed across multiple business dimensions such as new vs returning customers, products, categories, payment methods, and brands.
The raw data was provided in CSV format and imported as a flat file.
•	SQL was used for data cleaning, validation, and transformation
•	Python was used for exploratory data analysis (EDA) and statistical analysis
•	Power BI was used to build interactive dashboards and visualize insights
The goal of the project is to identify key revenue drivers, customer behavior patterns, and risk factors, and provide actionable recommendations to improve sales performance.
# Project Workflow & Code Structure
Data processing and analysis in this project follow a structured end-to-end workflow:
•	Excel was used to inspect and validate the raw CSV data before database ingestion.
•	SQL was used for data cleaning, null handling, deduplication. All SQL logic is consolidated into a single, well-documented SQL script, with clear section comments to represent different transformation stages.
•	Python was used for exploratory data analysis (EDA) and advanced statistical analysis, including outlier detection, revenue concentration analysis, customer segmentation, skewness analysis, and abnormal sales detection.
Python logic is intentionally maintained in a single script, organized with clearly separated analytical sections for readability and execution clarity.
•	Power BI consumes both transactional and analytical tables to build executive-level dashboards and supporting exploratory visuals.
# Insights
•	Sales trend analysis shows that current year sales have increased compared to the previous year, indicating positive growth.
•	Top products are heavily concentrated in the Water category, which contributes the highest share of revenue.
•	Excluding missing values (Unknown), the Electronics category generates the highest revenue.
•	Credit card is the most frequently used payment method, which may increase the risk of delayed payments.
•	Approximately 70% of customers are returning customers, and they contribute significantly to overall sales growth.
•	The Pepsi brand is one of the top contributors to total revenue, next to missing brand values.

# Recommendations
•	Since Pepsi brand products generate high revenue, expanding the product range from this brand can further increase sales.
•	Encouraging debit card payments may help reduce potential revenue delays associated with credit card usage.
•	As returning customers form the majority of revenue, personalized offers and targeted promotions should be introduced to retain and upsell this customer segment.
•	Focus marketing and inventory planning on high-performing categories and products to maximize profitability.
# Tools & Technologies Used
•	Excel – Initial data extraction and raw data handling
•	SQL – Data cleaning, validation, and transformation
•	Python – Exploratory Data Analysis (EDA) and statistical computations
•	Power BI – Interactive dashboards and data visualization


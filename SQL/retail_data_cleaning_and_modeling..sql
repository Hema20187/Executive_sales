--order_id duplicates
select order_id, count(*) from retail_data group by order_id having count(*) > 1
with order_duplicates as(
select *,
row_number() over (partition by order_id order by date desc) as rn
from retail_data
)
delete from order_duplicates where rn >1
--customer_id duplicates
select customer_id, count(*) from retail_data group by customer_id having count(*) >1
with cust_duplicates as(
select *,
row_number() over (partition by customer_id order by date desc) as rn
from retail_data
)
delete from cust_duplicates where rn >1

---overallcnt 

select count(*) from retail_data



--removing unused columns 

alter table retail_data drop column year,month,zipcode,city,country,income
--data cleaning
--checking nulls for ids
select * from retail_data where order_id is null
delete from retail_data where order_id is null
select * from retail_data where customer_id is null
delete from retail_data where customer_id is null
delete from retail_data where date is null
--updating unknown for missing values
select * from retail_data where name is null
update retail_data set name = 'unknown' where name is null
select * from retail_data where state is null
update retail_data set state = 'unknown' where state is null
--checking nulls 
select
sum(case when customer_segment is null then 1 else 0 end ) as csnull,
sum(case when quantity is null then 1 else 0 end) as qnull,
sum(case when price is null then 1 else 0 end) as pricenull,
sum(case when sales is null then 1 else 0 end) as salesnull,
sum(case when product_category is null then 1 else 0 end) as pcnull,
sum(case when product_brand is null then 1 else 0 end) as bnull,
sum(case when product_type is null then 1 else 0 end) as ptypenull,
sum(case when feedback is null then 1 else 0 end) as bnull,
sum(case when shipping_method is null then 1 else 0 end) as smnull,
sum(case when payment_method is null then 1 else 0 end) as pnull,
sum(case when order_status is null then 1 else 0 end) as osnull,
sum(case when ratings is null then 1 else 0 end) as ratingnull,
sum(case when products is null then 1 else 0 end) as pdnull
from retail_data
--updating with unknown for categorical columns
update retail_data set products = 'unknown' where products is null
--updating with 0 for numerical columns
update retail_data set ratings = 0 where ratings is null

--adding region column 
alter table retail_data add  region varchar(20) 

--updating region

UPDATE retail_data
SET region = CASE 
    
    WHEN state IN ('Connecticut','Maine','Massachusetts','New Hampshire','New Jersey','New York','Pennsylvania','Vermont','Rhode Island') THEN 'Northeast'
    WHEN state IN ('Illinois','Indiana','Iowa','Kansas','Michigan','Minnesota','Missouri','Nebraska','North Dakota','Ohio','South Dakota','Wisconsin') THEN 'Midwest'
    WHEN state IN ('Delaware','Florida','Georgia','Maryland','North Carolina','South Carolina','Virginia','West Virginia','Alabama','Kentucky','Mississippi','Tennessee','Arkansas','Louisiana','Oklahoma','Texas') THEN 'South'
    WHEN state IN ('Arizona','Colorado','Idaho','Montana','Nevada','New Mexico','Utah','Wyoming','Alaska','California','Hawaii','Oregon','Washington') THEN 'West'
    WHEN state IN ('England','New South Wales','Ontario','Berlin') THEN 'Other'
    ELSE 'Unknown'
END;
---seperating one into many tables 
select * from retail_data
--customers

SELECT DISTINCT 
    customer_id,
    name,
    state,
    Customer_Segment,
	region
INTO customers
FROM retail_data;
--products
SELECT DISTINCT
    products AS product_name,
    product_category,
    product_brand,
    product_type,
    price
INTO products
FROM retail_data;
--orders

SELECT DISTINCT
    order_id,
    customer_id,
    date AS order_date,
    order_status,
	Payment_Method,
	Shipping_Method
	
INTO orders
FROM retail_data;
--order_items
SELECT
    order_id,
    products AS product_name,
    quantity,
    price,
    sales,
	ratings,
	feedback
INTO order_items
FROM retail_data;
--adding product_id column
ALTER TABLE products ADD product_id INT IDENTITY(1,1);

ALTER TABLE order_items ADD product_id INT;

UPDATE oi
SET oi.product_id = p.product_id
FROM order_items oi
JOIN products p
ON oi.product_name = p.products;
--validating data from python code
select * from customer_segments
select * from abnormal_sales
select * from distribution_summary
select * from outlier_revenue_contribution


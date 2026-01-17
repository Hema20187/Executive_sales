import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# ================================
# DATABASE CONNECTION
# ================================
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    r'SERVER=DESKTOP-9BIF79B\SQLEXPRESS;'
    'DATABASE=retail;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
cq = "select * from customers"
oq="select * from orders"
pq="select * from products"
oiq="select * from order_items"
# ================================
# OUTLIER REVENUE CONTRIBUTION
# ================================
order_items = pd.read_sql(oiq,conn)
q1= order_items['sales'].quantile(0.25)
q3=order_items['sales'].quantile(0.75)
iqr_quantile=q3-q1
multiply_iqr= iqr_quantile*1.5
lower_bound=q1-multiply_iqr
upper_bound=q3+multiply_iqr
outliers= order_items[(order_items['sales']<lower_bound)|(order_items['sales']>upper_bound)]
outlier_total = round(outliers['sales'].sum(),2)
overall_total = round(order_items['sales'].sum(),2)
percentage_contribution = round((outlier_total/overall_total) *100.0,2)
print("Total of outlier sales:",round(outlier_total,2))
print("Total sales:",round(overall_total,2))
print("Percentage contribution of outlier sales in total sales:",round(percentage_contribution,2))
#moving to DB
create_table_query = """
IF OBJECT_ID('dbo.outlier_revenue_contribution', 'U') IS NOT NULL
    DROP TABLE dbo.outlier_revenue_contribution;
CREATE TABLE dbo.outlier_revenue_contribution (
    total_outlier_sales FLOAT,
    total_sales FLOAT,
    percentage_contribution FLOAT
)
"""
cursor.execute(create_table_query)
conn.commit()
insert_query = """
INSERT INTO dbo.outlier_revenue_contribution (total_outlier_sales, total_sales, percentage_contribution)
VALUES (?, ?, ?)
"""
cursor.execute(insert_query, outlier_total, overall_total, percentage_contribution)
conn.commit()
print("outlier revenue table created")

# ================================
# DISTRIBUTION SHAPE VALIDATION
# ================================

mean_value=np.mean(order_items['sales'])
median_value = np.median(order_items['sales'])
#optional using skew than mean and median
# skewness = order_items['sales'].skew()
# print(skewness)
if mean_value < median_value:
    skewness =" Left skewed"
elif mean_value > median_value:
    skewness="right skewed"
else:
    skewness="normally distributed"
print("Mean value of sales:",mean_value)
print("Median value of sales:",median_value)
print("skenewss distribution:",skewness)
#moving to DB
create_query_distribution ="""
    if object_id('DISTRIBUTION_SUMMARY','U') is not null
        drop table dbo.DISTRIBUTION_SUMMARY;
    create table dbo.DISTRIBUTION_SUMMARY(
    mean_value float,
    median_value float,
    skewness varchar(20)
    )
"""
conn.execute(create_query_distribution)
conn.commit()
insert_query = """
insert INTO dbo.DISTRIBUTION_SUMMARY (mean_value,median_value,skewness) values(?,?,?)
"""
conn.execute(insert_query,mean_value,median_value,skewness)
conn.commit()
# ================================
# ORDER SEGMENTATION ANALYSIS
# ================================
order_segments = order_items.groupby('order_id')['sales'].sum().reset_index()
quantile1=round(order_segments['sales'].quantile(0.25),2)
quantile3=round(order_segments['sales'].quantile(0.75),2)
order_segments['segmentation']=np.where((order_segments['sales'] < quantile1),
                                        "low",np.where((order_segments['sales']>quantile1)
                                         & (order_segments['sales']<=quantile3),"medium","high"))
segment_distribution = order_segments.groupby('segmentation').agg(
    total_order_count = ("order_id","nunique"),
    total_sales =("sales","sum"),
    average_sales=("sales","mean"),
).reset_index()
print("The segment distribution to find which segemnt leads the sales:\n",segment_distribution)
#moving to DB
create_query_segments="""
if object_id('customer_segments','U') is not null
drop table customer_segments
create table customer_segments(
    segments varchar(20),
    total_orders int,
    total_sales float,
    avg_sales float
    )
"""
conn.execute(create_query_segments)
conn.commit()
insert_query_segments = """
insert into customer_segments (segments,total_orders,total_sales,avg_sales) values (?,?,?,?)
"""
for index, row in segment_distribution.iterrows():
    conn.execute(
        insert_query_segments,
        row['segmentation'],
        row['total_order_count'],
        row['total_sales'],
        row['average_sales']
    )
# conn.execute(insert_query_segments,segment_distribution['segmentation'],segment_distribution['total_order_count'],
#              segment_distribution['total_sales'],segment_distribution['average_sales'])
conn.commit()
# ================================
# REVENUE CONCENTRATION RISK ANALYSIS
# ================================
revenue_Risk = order_items.groupby('order_id')['sales'].sum().reset_index()
revenue_Risk = revenue_Risk.sort_values(by='sales', ascending=False).reset_index(drop=True)
revenue_Risk['overall_sales']=round(revenue_Risk['sales'].sum(),2)
revenue_Risk['percentage_Contribution']=round((revenue_Risk['sales']/revenue_Risk['overall_sales'])*100.0,6)
revenue_Risk['cummulative_percentage']=revenue_Risk['percentage_Contribution'].cumsum()
revenue_Risk_top_ten=revenue_Risk.head(8500)
top_ten_sales=revenue_Risk_top_ten['sales'].sum()
overall_sales= revenue_Risk['sales'].sum()
overall_contribution = (top_ten_sales/overall_sales)*100.0
print(f"top 10 percent of orders contributes to {round(overall_contribution,2)} percentage of sales")
# ================================
# ABNORMAL SALES DETECTION
# ================================
orders = pd.read_sql(oq,conn)
order_with_order_items = order_items.merge(orders,on='order_id')
order_with_order_items=order_with_order_items.groupby('order_date')['sales'].sum().reset_index()
mean_value_abnormal= order_with_order_items['sales'].mean()
std_abnormal=order_with_order_items['sales'].std()
order_with_order_items['abnormal_flag'] = np.where((order_with_order_items['sales'] >=mean_value_abnormal+2*std_abnormal),"Abnormal spike","normal")
print("sales with abnormal flag:\n",order_with_order_items)
#moving to DB
create_query_abnormal ="""
if object_id('abnormal_sales','U') is not null
drop table abnormal_sales
create table abnormal_sales(
order_date date,
sales float,
flag varchar(20)
)
"""
conn.execute(create_query_abnormal)
conn.commit()
insert_query_abnormal = """
insert into abnormal_sales(order_date,sales,flag) values(?,?,?)
"""
for index,row in order_with_order_items.iterrows():
    conn.execute(
        insert_query_abnormal,
        row['order_date'],
        row['sales'],
        row['abnormal_flag']
    )
conn.commit()
# ================================
# CUSTOMER PURCHASE CONSISTENCY
# ================================
customer_behaviour = order_items.merge(orders,on='order_id')
customer_behaviour = customer_behaviour.groupby(['order_id','customer_id'])['sales'].sum().sort_values(ascending=True).reset_index()
customer_behaviour=customer_behaviour.groupby('customer_id').agg(
    mean_value = ("sales","mean"),
    std_value=("sales","std")
).reset_index()
customer_behaviour['std_value']=customer_behaviour['std_value'].fillna(0)
std_mean = customer_behaviour['std_value'].mean()
customer_behaviour['consistency_flag']=np.where((customer_behaviour['std_value']>std_mean),"Inconsistent purchase","consistent purchase")
print("customer behaviours can be seen through:\n",customer_behaviour)







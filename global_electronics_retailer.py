# File: global_electronics_retailer.py

# This script is basically meant to preprocess data on the Global Electronics Retailer project for Power BI visualization.

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Function to load data from a CSV file
# This function reads a CSV file and returns a pandas DataFrame.
# It also handles exceptions that may occur during the loading process.

def load_data(file_path, encoding="utf-8"):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.
    encoding (str): The encoding of the CSV file. Default is 'utf-8'.

    Returns:
    pd.DataFrame: The loaded data as a DataFrame.
    """
    try:
        data = pd.read_csv(file_path, encoding=encoding)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Load the customer dimension data
file_path = "/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/dim_customers.csv"

dim_customer = load_data(file_path, encoding="ISO-8859-1")

# Check if the data was loaded successfully
if dim_customer is not None:
    print("Customer dimension data loaded successfully.")
else:
    print("Failed to load customer dimension data.")

# Load the product dimension data
file_path = "/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/dim_products.csv"

dim_product = load_data(file_path, encoding="ISO-8859-1")

# Check if the data was loaded successfully
if dim_product is not None:
    print("Product dimension data loaded successfully.")
else:
    print("Failed to load product dimension data.")


# Load the store dimension data
file_path = "/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/dim_stores.csv"

dim_stores = load_data(file_path, encoding="ISO-8859-1")

# Check if the data was loaded successfully
if dim_stores is not None:
    print("Store dimension data loaded successfully.")
else:
    print("Failed to load store dimension data.")

# Load exchange rates dimension data
file_path = "/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/dim_exchange_rates.csv"

dim_exchange_rates = load_data(file_path, encoding="ISO-8859-1")

# Check if the data was loaded successfully
if dim_exchange_rates is not None:
    print("Exchange rates dimension data loaded successfully.")
else:
    print("Failed to load exchange rates dimension data.")

# Load the sales fact data
file_path = "/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/fact_sales.csv"

fact_sales = load_data(file_path, encoding="ISO-8859-1")

# Check if the data was loaded successfully
if fact_sales is not None:
    print("Sales fact data loaded successfully.")
else:
    print("Failed to load sales fact data.")


# Understanding customer demographics

dim_customer.head()

# Total number of customers by country, and gender
customer_country = dim_customer.groupby('Country').size().reset_index(name='total_customers')

customer_country = customer_country.sort_values(by='total_customers', ascending=False)

customer_country.reset_index(drop=True, inplace=True)

customer_country

# plotting the total number of customers by country
plt.figure(figsize=(12, 6))
sns.barplot(x='total_customers', y='Country', data=customer_country, palette='viridis',
            hue='Country', legend=False)
plt.title('Total Number of Customers by Country')
plt.xlabel('Total Customers')
plt.ylabel('Country')
plt.xticks(rotation=45)
plt.show()

# Total number of customers by gender
customer_gender = dim_customer.groupby('Gender').size().reset_index(name='total_customers')

customer_gender = customer_gender.sort_values(by='total_customers', ascending=False)

customer_gender.reset_index(drop=True, inplace=True)

customer_gender

# plotting the total number of customers by gender
plt.figure(figsize=(12, 6))
sns.barplot(x='total_customers', y='Gender', data=customer_gender, palette='viridis',
            hue='Gender', legend=False)
plt.title('Total Number of Customers by Gender')
plt.xlabel('Total Customers')
plt.ylabel('Gender')
plt.xticks(rotation=45)
plt.show()

# Handling missing values in field 'State Code'. 
# First show the data segment with missing values in 'State Code'

missing_state_code = dim_customer[dim_customer['State Code'].isnull()]

missing_state_code

# Fill missing values in 'State Code' with 'NA'
dim_customer['State Code'].fillna('NA', inplace=True)

# Coverting date date to datetime format
# Check the data types of the columns in the sales fact data
fact_sales.dtypes
# Convert 'Order Date' and 'Delivery Date' to datetime format
fact_sales['Order Date'] = pd.to_datetime(fact_sales['Order Date'], format='mixed')
fact_sales['Delivery Date'] = pd.to_datetime(fact_sales['Delivery Date'], format='mixed')

# Extract year and month from 'Order Date' for sales trends analysis
fact_sales['Order Year'] = fact_sales['Order Date'].dt.year
fact_sales['Order Month'] = fact_sales['Order Date'].dt.month

# Customer RFM Segmentation
# Calculate Recency, Frequency, and Monetary values for each customer

# Aggregate RFM metrics per customer
snapshot = fact_sales['Order Date'].max() + pd.Timedelta(days=1)

customer_rfm = fact_sales.groupby('CustomerKey').agg({
    'Order Date': lambda x: (snapshot - x.max()).days,  # Recency
    'Order Number': 'count',  # Frequency
    'Quantity': 'sum'  # Monetary
}).rename(columns={
    'Order Date': 'Recency',
    'Order Number': 'Frequency',
    'Quantity': 'Monetary'
}).reset_index()

# Display the RFM DataFrame
customer_rfm.head()

# Merge with customer dimension to get customer demographics
dim_customer = dim_customer.merge(customer_rfm[['CustomerKey', 'Recency', 'Frequency', 'Monetary']], on='CustomerKey', how='left')

dim_customer.head()

# Drop rows with NaN values in 'Recency', 'Frequency', or 'Monetary'
dim_customer = dim_customer.dropna(subset=['Recency', 'Frequency', 'Monetary'])

# Quantile-based scoring for RFM (1 = best, 4 = worst; reversed for Frequency/Monetary)
dim_customer['R_Score'] = pd.qcut(dim_customer['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
# Frequency and Monetary scores are reversed since lower values are better for Recency
dim_customer['F_Score'] = pd.qcut(dim_customer['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)
dim_customer['M_Score'] = pd.qcut(dim_customer['Monetary'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)

# Combine scores into segment labels
dim_customer['RFM_Score'] = dim_customer[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

dim_customer.head()

# Segmentation based on RFM scores
def customer_grouping(row):
    if row['RFM_Score'] >= 9:
        return 'Champions'
    elif row['RFM_Score'] >= 6:
        return 'Loyal Customers'
    elif row['RFM_Score'] >= 4:
        return 'Potential Loyalists'
    else:
        return 'At Risk'

dim_customer['Customer_Category'] = dim_customer.apply(customer_grouping, axis=1)

# Display the RFM DataFrame with segments
dim_customer.head()

# Plotting RFM Segments
plt.figure(figsize=(12, 6))
sns.countplot(data=dim_customer, x='Customer_Category', palette='viridis', hue='Customer_Category', legend=False)
plt.title('Customer Segments based on RFM Analysis')
plt.xlabel('Customer Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.show()

dim_customer.to_csv('/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/dim_customer.csv', index=False)

# RFM Analysis Summary
rfm_summary = dim_customer.groupby('Customer_Category').agg({
    'CustomerKey': 'count',
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).rename(columns={'CustomerKey': 'Total Customers'}).reset_index()

rfm_summary

# RFM analysis for products
# Merge Unit Price USD from dim_product into fact_sales using ProductKey
# Strip the dollar sign and comma from 'Unit Price USD' in dim_product and convert to float
dim_product['Unit Price USD'] = dim_product['Unit Price USD'].replace({'\$': '', ',': ''}, 
                                                                      regex=True).astype(float)

dim_product['Unit Cost USD'] = dim_product['Unit Cost USD'].replace({'\$': '', ',': ''},
                                                                      regex=True).astype(float)
# Display the first few rows of dim_product to verify the changes
dim_product.dtypes

fact_sales = fact_sales.merge(dim_product[['ProductKey', 'Unit Price USD']], 
                              on='ProductKey', how='left')

# remove columns unit price usdx and total revenue from fact_sales
fact_sales.drop(columns=['Unit Price USD_x', 'Total Revenue'], inplace=True, errors='ignore')

fact_sales.rename(columns={'Unit Price USD_y': 'Unit Price USD'}, inplace=True)
fact_sales.head()

fact_sales.dtypes

# Calculate total revenue for each order
fact_sales['Total Revenue'] = fact_sales['Quantity'] * fact_sales['Unit Price USD']
# Aggregate RFM metrics per product
rfm_product = fact_sales.groupby('ProductKey').agg({
    'Order Date': lambda x: (snapshot - x.max()).days,  # Recency
    'Order Number': 'count',  # Frequency
    'Total Revenue': 'sum'  # Monetary
}).rename(columns={
    'Order Date': 'Recency',
    'Order Number': 'Frequency',
    'Total Revenue': 'Monetary'
}).reset_index()

rfm_product.head()

# Merge rfm_product with product dimension to get product details
columns_to_merge = ['ProductKey', 'Recency', 'Frequency', 'Monetary']
dim_product = dim_product.merge(rfm_product[columns_to_merge], on='ProductKey', how='left')

dim_product.head()

# Remove rows with NaN values in 'Recency', 'Frequency', or 'Monetary'
dim_product = dim_product.dropna(subset=['Recency', 'Frequency', 'Monetary'])

# Quantile-based scoring for RFM (1 = best, 4 = worst; reversed for Frequency/Monetary)
dim_product['R_Score'] = pd.qcut(dim_product['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
# Frequency and Monetary scores are reversed since lower values are better for Recency
dim_product['F_Score'] = pd.qcut(
    dim_product['Frequency'].rank(
        method='first'), 4, labels=[1, 2, 3, 4]
    ).astype(int)
dim_product['M_Score'] = pd.qcut(
    dim_product['Monetary'].rank(
        method='first'), 4, labels=[1, 2, 3, 4]
    ).astype(int)

dim_product['RFM_Score'] = dim_product[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

dim_product.head()

dim_product['RFM_Segment'] = dim_product['R_Score'].astype(str) + dim_product['F_Score'].astype(str) + dim_product['M_Score'].astype(str)

# Segmentation based on RFM scores for product
def rfm_product_segment(row):
    if row['RFM_Score'] >= 9:
        return 'Best Sellers'
    elif row['RFM_Score'] >= 6:
        return 'Steady Movers'
    elif row['RFM_Score'] >= 4:
        return 'Potential Stars'
    elif row['RFM_Score'] >= 2:
        return 'Low Performers'
    else:
        return 'Underdogs'

dim_product['Product_Segment'] = dim_product.apply(rfm_product_segment, axis=1)

# Display the product RFM DataFrame with segments
dim_product.head()

# Plotting Product RFM Segments
plt.figure(figsize=(12, 6))
sns.countplot(data=dim_product, x='Product_Segment', palette='viridis',
            hue='Product_Segment', legend=False)
plt.title('Product Segments based on RFM Analysis')
plt.xlabel('Product Segment')
plt.ylabel('Number of Products')
plt.xticks(rotation=45)
plt.show()

# Product RFM Analysis Summary
product_rfm_summary = dim_product.groupby('Product_Segment').agg({
    'ProductKey': 'count',
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).rename(columns={'ProductKey': 'Total Products'}).reset_index().sort_values(by='Total Products', ascending=False)

product_rfm_summary

# Save the product RFM analysis to a CSV file
dim_product.to_csv('/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/product_rfm_analysis.csv', 
                   index=False)

# Store Performance Analysis
# Calculate total sales and average order value (AOV) for each store
store_performance = fact_sales.groupby('StoreKey').agg({
    'Total Revenue': 'sum',
    'Order Number': 'count'
}).rename(columns={
    'Total Revenue': 'Total Sales',
    'Order Number': 'Total Orders'
}).reset_index().sort_values(by='Total Sales', ascending=False)

# Display the store performance DataFrame
store_performance

# store_performance[store_performance['StoreKey']== 7]

# Merge with store dimension to get store details
dim_stores = dim_stores.merge(store_performance[['StoreKey', 'Total Sales', 'Total Orders']], 
                                            on='StoreKey', how='left')
dim_stores.head()
# Calculate Average Order Value (AOV)
dim_stores['AOV'] = dim_stores['Total Sales'] / dim_stores['Total Orders']

dim_stores.dropna(subset=['Total Sales', 'Total Orders', 'AOV'], inplace=True)

# Plotting Store Performance
plt.figure(figsize=(12, 6))
sns.barplot(x='Total Sales', y='StoreKey', data=store_performance,
            palette='viridis', hue='StoreKey', legend=False)
plt.title('Store Performance: Total Sales by Store')
plt.xlabel('Total Sales')
plt.ylabel('Store Key')
plt.xticks(rotation=45)
plt.show()

# Store Performance Summary
store_performance_summary = dim_stores[['StoreKey', 'Total Sales', 'State',
                                        'Total Orders', 'AOV']].sort_values(
                                            by='Total Sales', ascending=False)
                                        
store_performance_summary

# Save the dim_stores DataFrame to a CSV file
dim_stores.to_csv('/Users/HP/Documents/Data_Analytics/CodeBasics/Projects_Portfolio/Global+Electronics+Retailer/Data/dim_stores.csv',
                   index=False)
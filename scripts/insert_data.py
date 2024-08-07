# scripts/insert_data.py
import mysql.connector
import pandas as pd

# Database connection details
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'ecommerce_analytics',
    'auth_plugin': 'mysql_native_password'
}

# Establish connection to MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Load CSV data
customers_data = pd.read_csv('./data/customers.csv')
products_data = pd.read_csv('./data/products.csv')
sales_data = pd.read_csv('./data/sales.csv')

cursor.execute("set foreign_key_checks = 0")
cursor.execute("truncate customers")
cursor.execute("truncate sales")
cursor.execute("truncate products")
cursor.execute("set foreign_key_checks = 1")

# Insert data into MySQL
for _, row in customers_data.iterrows():
    cursor.execute("INSERT INTO customers (name, email, date_joined) VALUES (%s, %s, %s)",
                   (row['name'], row['email'], row['date_joined']))

for _, row in products_data.iterrows():
    cursor.execute("INSERT INTO products (name, category, price) VALUES (%s, %s, %s)",
                   (row['name'], row['category'], row['price']))

for _, row in sales_data.iterrows():
    cursor.execute("INSERT INTO sales (customer_id, product_id, sale_date, quantity, total_amount) VALUES (%s, %s, %s, %s, %s)",
                   (row['customer_id'], row['product_id'], row['sale_date'], row['quantity'], row['total_amount']))
    


connection.commit()
cursor.close()
connection.close()

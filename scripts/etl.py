# scripts/etl.py
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine


# Database connection details
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'ecommerce_analytics',
    'auth_plugin': 'mysql_native_password'
}

# Create SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# Extract data from MySQL
query = '''
SELECT 
    p.category, 
    SUM(s.total_amount) AS total_sales, 
    COUNT(DISTINCT s.customer_id) AS customer_count
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category;
'''
df = pd.read_sql(query, con=engine)

# Transform data
sales_growth = df['total_sales'].pct_change().fillna(0)
df['sales_growth'] = sales_growth


import os
# Define the path
output_path = './data/processed_data.csv'
directory = os.path.dirname(output_path)

# Create the directory if it does not exist
if not os.path.exists(directory):
    os.makedirs(directory)

# Save the DataFrame
df.to_csv(output_path, index=False)

# # Load transformed data to CSV
# df.to_csv('../data/processed_data.csv', index=False)


# df.to_csv('../data/processed_data.csv', index=False)

@echo off

rem Run SQL script to create tables
mysql -u root -p -D ecommerce_analytics < scripts\create_tables.sql

rem Run Python scripts
python scripts\insert_data.py
python scripts\etl.py
python scripts\visualize.py

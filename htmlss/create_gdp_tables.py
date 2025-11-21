"""
Script to create GDP database tables and load data from CSV files
"""
from db import get_db_connection
import csv
import os

def create_gdp_tables():
    """Create GDP tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Drop existing tables to ensure clean structure
    cursor.execute("DROP TABLE IF EXISTS gdp_details")
    cursor.execute("DROP TABLE IF EXISTS gdp_main")
    
    # Create gdp_main table
    create_main_table = """
    CREATE TABLE gdp_main (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Code_No INT,
        items VARCHAR(255),
        Q2020Q1 DECIMAL(10,2),
        Q2020Q2 DECIMAL(10,2),
        Q2020Q3 DECIMAL(10,2),
        Q2020Q4 DECIMAL(10,2),
        Q2021Q1 DECIMAL(10,2),
        Q2021Q2 DECIMAL(10,2),
        Q2021Q3 DECIMAL(10,2),
        Q2021Q4 DECIMAL(10,2),
        Q2022Q1 DECIMAL(10,2),
        Q2022Q2 DECIMAL(10,2),
        Q2022Q3 DECIMAL(10,2),
        Q2022Q4 DECIMAL(10,2),
        Q2023Q1 DECIMAL(10,2),
        Q2023Q2 DECIMAL(10,2),
        Q2023Q3 DECIMAL(10,2),
        Q2023Q4 DECIMAL(10,2),
        Q2024Q1 DECIMAL(10,2),
        Q2024Q2 DECIMAL(10,2),
        Q2024Q3 DECIMAL(10,2),
        Q2024Q4 DECIMAL(10,2),
        Q2025Q1 DECIMAL(10,2)
    )
    """
    
    # Create gdp_details table with same structure
    create_details_table = """
    CREATE TABLE gdp_details (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Code_No INT,
        items VARCHAR(255),
        Q2020Q1 DECIMAL(10,2),
        Q2020Q2 DECIMAL(10,2),
        Q2020Q3 DECIMAL(10,2),
        Q2020Q4 DECIMAL(10,2),
        Q2021Q1 DECIMAL(10,2),
        Q2021Q2 DECIMAL(10,2),
        Q2021Q3 DECIMAL(10,2),
        Q2021Q4 DECIMAL(10,2),
        Q2022Q1 DECIMAL(10,2),
        Q2022Q2 DECIMAL(10,2),
        Q2022Q3 DECIMAL(10,2),
        Q2022Q4 DECIMAL(10,2),
        Q2023Q1 DECIMAL(10,2),
        Q2023Q2 DECIMAL(10,2),
        Q2023Q3 DECIMAL(10,2),
        Q2023Q4 DECIMAL(10,2),
        Q2024Q1 DECIMAL(10,2),
        Q2024Q2 DECIMAL(10,2),
        Q2024Q3 DECIMAL(10,2),
        Q2024Q4 DECIMAL(10,2),
        Q2025Q1 DECIMAL(10,2)
    )
    """
    
    cursor.execute(create_main_table)
    cursor.execute(create_details_table)
    conn.commit()
    cursor.close()
    conn.close()
    print("✓ GDP tables created successfully")

def clean_number(value):
    """Clean number strings by removing commas and quotes"""
    if isinstance(value, str):
        value = value.strip().strip('"').replace(',', '')
        if value == '':
            return 0
    try:
        return float(value)
    except:
        return 0

def load_gdp_data():
    """Load GDP data from CSV files into database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Load gdp_main.csv
    gdp_main_path = os.path.join('gdp', 'gdp_main.csv')
    with open(gdp_main_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert_sql = """
            INSERT INTO gdp_main 
            (Code_No, items, Q2020Q1, Q2020Q2, Q2020Q3, Q2020Q4, Q2021Q1, Q2021Q2, Q2021Q3, Q2021Q4,
             Q2022Q1, Q2022Q2, Q2022Q3, Q2022Q4, Q2023Q1, Q2023Q2, Q2023Q3, Q2023Q4,
             Q2024Q1, Q2024Q2, Q2024Q3, Q2024Q4, Q2025Q1)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                int(row['Code_No']),
                row['items'],
                clean_number(row['2020Q1']), clean_number(row['2020Q2']), clean_number(row['2020Q3']), clean_number(row['2020Q4']),
                clean_number(row['2021Q1']), clean_number(row['2021Q2']), clean_number(row['2021Q3']), clean_number(row['2021Q4']),
                clean_number(row['2022Q1']), clean_number(row['2022Q2']), clean_number(row['2022Q3']), clean_number(row['2022Q4']),
                clean_number(row['2023Q1']), clean_number(row['2023Q2']), clean_number(row['2023Q3']), clean_number(row['2023Q4']),
                clean_number(row['2024Q1']), clean_number(row['2024Q2']), clean_number(row['2024Q3']), clean_number(row['2024Q4']),
                clean_number(row['2025Q1'])
            )
            cursor.execute(insert_sql, values)
    
    print("✓ gdp_main data loaded")
    
    # Load details_gdp.csv
    gdp_details_path = os.path.join('gdp', 'details_gdp.csv')
    with open(gdp_details_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert_sql = """
            INSERT INTO gdp_details 
            (Code_No, items, Q2020Q1, Q2020Q2, Q2020Q3, Q2020Q4, Q2021Q1, Q2021Q2, Q2021Q3, Q2021Q4,
             Q2022Q1, Q2022Q2, Q2022Q3, Q2022Q4, Q2023Q1, Q2023Q2, Q2023Q3, Q2023Q4,
             Q2024Q1, Q2024Q2, Q2024Q3, Q2024Q4, Q2025Q1)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                int(row['Code_No']),
                row['items'],
                clean_number(row['2020Q1']), clean_number(row['2020Q2']), clean_number(row['2020Q3']), clean_number(row['2020Q4']),
                clean_number(row['2021Q1']), clean_number(row['2021Q2']), clean_number(row['2021Q3']), clean_number(row['2021Q4']),
                clean_number(row['2022Q1']), clean_number(row['2022Q2']), clean_number(row['2022Q3']), clean_number(row['2022Q4']),
                clean_number(row['2023Q1']), clean_number(row['2023Q2']), clean_number(row['2023Q3']), clean_number(row['2023Q4']),
                clean_number(row['2024Q1']), clean_number(row['2024Q2']), clean_number(row['2024Q3']), clean_number(row['2024Q4']),
                clean_number(row['2025Q1'])
            )
            cursor.execute(insert_sql, values)
    
    print("✓ gdp_details data loaded")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n✓ GDP data integration complete!")

if __name__ == '__main__':
    print("Creating GDP tables...")
    create_gdp_tables()
    print("\nLoading GDP data...")
    load_gdp_data()

#!/usr/bin/env python3
"""
Database structure inspector
"""

from db import get_db_connection

def inspect_database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check export_commodities structure
        print("=== EXPORT_COMMODITIES TABLE ===")
        cursor.execute("DESCRIBE export_commodities")
        columns = cursor.fetchall()
        print("Structure:")
        for col in columns:
            print(f"  {col}")
        
        print("\nSample data:")
        cursor.execute("SELECT * FROM export_commodities LIMIT 3")
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        print(f"Columns: {column_names}")
        for row in data:
            print(f"  {row}")
        
        # Check if imports_commodities exists
        print("\n=== IMPORTS_COMMODITIES TABLE ===")
        try:
            cursor.execute("DESCRIBE imports_commodities")
            columns = cursor.fetchall()
            print("Structure:")
            for col in columns:
                print(f"  {col}")
            
            print("\nSample data:")
            cursor.execute("SELECT * FROM imports_commodities LIMIT 3")
            data = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            print(f"Columns: {column_names}")
            for row in data:
                print(f"  {row}")
        except Exception as e:
            print(f"Imports table error: {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    inspect_database()
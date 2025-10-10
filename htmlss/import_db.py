#!/usr/bin/env python3
import mysql.connector
import os
from urllib.parse import urlparse

def import_sql_to_jawsdb():
    # JawsDB URL from Heroku
    jawsdb_url = "mysql://f9bf480ab7za5v9t:horjpdnw78o354ab@t89yihg12rw77y6f.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/srpeclg1lhozd0gl"
    
    # Parse the URL
    parsed = urlparse(jawsdb_url)
    
    # Connection parameters
    config = {
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'database': parsed.path[1:],  # Remove leading slash
        'raise_on_warnings': True
    }
    
    try:
        # Connect to the database
        print("Connecting to JawsDB MySQL...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Read the SQL dump file
        print("Reading bigdata.sql...")
        with open('bigdata.sql', 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split SQL commands by semicolon and execute each
        print("Executing SQL commands...")
        sql_commands = sql_content.split(';')
        
        for i, command in enumerate(sql_commands):
            command = command.strip()
            if command and not command.startswith('--') and not command.startswith('/*'):
                try:
                    cursor.execute(command)
                    print(f"Executed command {i+1}")
                except mysql.connector.Error as err:
                    if "already exists" in str(err) or "doesn't exist" in str(err):
                        print(f"Skipping command {i+1}: {err}")
                        continue
                    else:
                        print(f"Error in command {i+1}: {err}")
                        print(f"Command: {command[:100]}...")
        
        # Commit the changes
        connection.commit()
        print("Database import completed successfully!")
        
        # Test the import by checking tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"Tables created: {[table[0] for table in tables]}")
        
        # Check data in key tables
        for table in ['datamap', 'export_commodities', 'imports_commodities', 'users']:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"Table {table}: {count} rows")
            except mysql.connector.Error as err:
                print(f"Could not query {table}: {err}")
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    import_sql_to_jawsdb()
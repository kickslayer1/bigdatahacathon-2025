"""
Export MySQL database to SQL file
"""
import mysql.connector
import os

def export_database():
    try:
        # Connect to your local database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kickslayer',
            database='bigdatahackaton'
        )
        cursor = conn.cursor()
        
        sql_content = []
        sql_content.append("-- Rwanda Trade Dashboard Database Export")
        sql_content.append("-- Generated automatically")
        sql_content.append("")
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            print(f"Exporting table: {table_name}")
            
            # Get table structure
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_table = cursor.fetchone()[1]
            
            sql_content.append(f"-- Table structure for {table_name}")
            sql_content.append(f"DROP TABLE IF EXISTS `{table_name}`;")
            sql_content.append(create_table + ";")
            sql_content.append("")
            
            # Get table data
            cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = cursor.fetchall()
            
            if rows:
                # Get column names
                cursor.execute(f"DESCRIBE `{table_name}`")
                columns = [col[0] for col in cursor.fetchall()]
                
                sql_content.append(f"-- Data for table {table_name}")
                
                for row in rows:
                    # Format values properly
                    values = []
                    for value in row:
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, str):
                            # Escape single quotes
                            escaped_value = value.replace("'", "''")
                            values.append(f"'{escaped_value}'")
                        else:
                            values.append(str(value))
                    
                    column_names = ", ".join([f"`{col}`" for col in columns])
                    values_str = ", ".join(values)
                    sql_content.append(f"INSERT INTO `{table_name}` ({column_names}) VALUES ({values_str});")
                
                sql_content.append("")
        
        # Write to file
        with open('database_export.sql', 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_content))
        
        print(f"✅ Database exported successfully to database_export.sql")
        print(f"📊 Exported {len(tables)} tables")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error exporting database: {e}")

if __name__ == "__main__":
    export_database()
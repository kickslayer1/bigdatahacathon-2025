# Exports Data Visualization from MySQL
# Requires: pandas, matplotlib, mysql-connector-python
# Usage: python exports.py

import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Database connection settings
conn = mysql.connector.connect(
    host='localhost',           # or your DB host
    user='root',     # replace with your MySQL username
    password='kickslayer', # replace with your MySQL password
    database='bigdatahackaton'  # replace with your database name
)

# Query data from the 'exportss' table
query = "SELECT period, exports, imports, `re-imports` FROM exportss"
df = pd.read_sql(query, conn)
conn.close()

# Sort by period if needed
df = df.sort_values('period')

# Plot line chart
plt.figure(figsize=(10,6))
plt.plot(df['period'], df['exports'], marker='o', label='Exports')
plt.plot(df['period'], df['imports'], marker='o', label='Imports')
plt.plot(df['period'], df['re-imports'], marker='o', label='Re-imports')
plt.title('Exports, Imports, and Re-imports Over Time')
plt.xlabel('Period')
plt.ylabel('Amount (in million dollars)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart to htmlss folder
plt.savefig('htmlss/exports_chart.png', dpi=120)
plt.close()

print('Line chart saved as htmlss/exports_chart.png')


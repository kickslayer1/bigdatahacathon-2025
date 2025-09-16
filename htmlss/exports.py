# Exports Data Visualization
# Requires: pandas, matplotlib
# Usage: python exports.py

import pandas as pd
import matplotlib.pyplot as plt

# Load dataset (assumes columns: time, item, amount)
df = pd.read_csv('datasetx.csv')

# Pivot data for grouped bar chart: time on x-axis, items as bars
pivot = df.pivot_table(index='time', columns='item', values='amount', aggfunc='sum', fill_value=0)

# Plot
ax = pivot.plot(kind='bar', figsize=(10,6), colormap='tab20')
plt.title('Exports Over Time by Item')
plt.xlabel('Time')
plt.ylabel('Amount')
plt.legend(title='Item', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save chart to htmlss folder
plt.savefig('htmlss/exports_chart.png', dpi=120)
plt.close()

print('Bar chart saved as htmlss/exports_chart.png')

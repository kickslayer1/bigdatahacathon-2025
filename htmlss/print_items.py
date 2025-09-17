# Print all unique items in the 'item' column of datasetx.csv
import pandas as pd

df = pd.read_csv('datasetx.csv')
items = df['item'].unique()
print('items in datasetx.csv:')
for item in items:
    print(item)

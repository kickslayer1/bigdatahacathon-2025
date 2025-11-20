import pandas as pd

# Load dataset
df = pd.read_csv('datasetx.csv')

# Prompt user for item and year
item = input(f"Choose an item from: {df['item'].unique().tolist()}\n> ")
year = int(input(f"Choose a year from: {df['time'].unique().tolist()}\n> "))

# Filter and print result
result = df[(df['item'] == item) & (df['time'] == year)]
if not result.empty:
    print(f"Predicted amount for {item} in {year}: {result.iloc[0]['amount']}")
else:
    print("No data found for the selected item and year.")
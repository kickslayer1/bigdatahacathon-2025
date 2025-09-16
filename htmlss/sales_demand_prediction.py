# Sales Demand Prediction using Random Forest
# Requires: pandas, scikit-learn, matplotlib
# Usage: python sales_demand_prediction.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('datasetx.csv')

# Encode categorical variables
le_item = LabelEncoder()
df['item_encoded'] = le_item.fit_transform(df['item'])

# Feature selection
features = ['item_encoded', 'export', 'import', 'price', 'market_trend', 'seasonality']
target = 'sales_demand'

X = df[features]
y = df[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse:.2f}')
print(f'R^2 Score: {r2:.2f}')

# Feature importance plot
importances = model.feature_importances_
plt.figure(figsize=(8,5))
plt.bar(features, importances, color='navy')
plt.title('Feature Importance for Sales Demand Prediction')
plt.ylabel('Importance')
plt.tight_layout()
plt.savefig('htmlss/sales_feature_importance.png', dpi=120)
plt.close()
print('Feature importance chart saved as htmlss/sales_feature_importance.png')

# Example: Predict for new data
# new_data = pd.DataFrame({
#     'item_encoded': [le_item.transform(['Gold'])[0]],
#     'export': [1000],
#     'import': [500],
#     'price': [1200],
#     'market_trend': [1.2],
#     'seasonality': [0.8]
# })
# predicted_demand = model.predict(new_data)
# print('Predicted sales demand:', predicted_demand)

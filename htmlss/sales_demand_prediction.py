# Sales Amount Prediction using Random Forest
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

# Encode Item (categorical)
le_item = LabelEncoder()
df['Item_encoded'] = le_item.fit_transform(df['Item'])

# Features: Item_encoded, time (year as integer)
features = ['Item_encoded', 'time']
target = 'amount'

X = df[features]
y = df[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2:", r2_score(y_test, y_pred))

# Feature importance plot
plt.bar(features, model.feature_importances_)
plt.title("Feature Importance")
plt.show()

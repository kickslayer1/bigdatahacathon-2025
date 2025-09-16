# predict.py

import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_demand(year, commodity, features=None, model=None):
    """
    Predicts demand for a given commodity and year.
    :param year: int, year for prediction
    :param commodity: str, commodity name
    :param features: pd.DataFrame, optional features for prediction
    :param model: sklearn model, optional model for prediction
    :return: str, prediction result
    """
    if model and features is not None:
        prediction = model.predict(features)
        return f"Predicted demand for {commodity} in {year}: {prediction[0]}"
    else:
        # Dummy logic
        return f"Predicted demand for {commodity} in {year}: Rising"

# Example usage:
if __name__ == "__main__":
    # Dummy usage
    print(predict_demand(2026, "Gold"))
    
    # Example with dummy ML model
    # data = pd.DataFrame({'year': [2025, 2026], 'gold_price': [1800, 1850]})
    # X = data[['year', 'gold_price']]
    # y = [100, 125]
    # model = LinearRegression().fit(X, y)
    # print(predict_demand(2026, "Gold", features=pd.DataFrame({'year':[2026], 'gold_price':[1850]}), model=model))
"""
Advanced Machine Learning Prediction System for Export Commodities
Uses Prophet, Linear Regression, and Time Series Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try importing ML libraries with fallbacks
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    print("Warning: Prophet not available, using fallback predictions")
    PROPHET_AVAILABLE = False

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.metrics import mean_absolute_error, r2_score
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: Scikit-learn not available, using basic predictions")
    SKLEARN_AVAILABLE = False

class CommodityPredictor:
    def __init__(self):
        self.prophet_model = None
        self.linear_model = None
        self.poly_features = None
        self.historical_data = None
        
    def prepare_data(self, commodity_data):
        """
        Prepare data for machine learning models
        Expected format: list of dictionaries with 'quarter' and 'value' keys
        """
        # Convert to DataFrame
        df = pd.DataFrame(commodity_data)
        
        # Convert quarter to datetime
        df['ds'] = pd.to_datetime(df['quarter'].str.replace('Q', '-Q'), format='%Y-Q%q')
        df['y'] = df['value'].astype(float)
        
        # Create numerical features for linear regression
        df['quarter_num'] = range(len(df))
        df['year'] = df['ds'].dt.year
        df['quarter'] = df['ds'].dt.quarter
        
        # Add trend and seasonal features
        df['trend'] = df['quarter_num']
        df['seasonal_sin'] = np.sin(2 * np.pi * df['quarter'] / 4)
        df['seasonal_cos'] = np.cos(2 * np.pi * df['quarter'] / 4)
        
        self.historical_data = df
        return df
    
    def train_prophet_model(self, df):
        """
        Train Facebook Prophet model for time series forecasting
        """
        if not PROPHET_AVAILABLE:
            return False
            
        try:
            # Prepare data for Prophet
            prophet_df = df[['ds', 'y']].copy()
            
            # Initialize and train Prophet model
            self.prophet_model = Prophet(
                yearly_seasonality=True,
                quarterly_seasonality=True,
                changepoint_prior_scale=0.1,
                seasonality_prior_scale=10,
                interval_width=0.95
            )
            
            self.prophet_model.fit(prophet_df)
            return True
        except Exception as e:
            print(f"Prophet model training failed: {e}")
            return False
    
    def train_linear_model(self, df):
        """
        Train advanced linear regression model with polynomial features
        """
        if not SKLEARN_AVAILABLE:
            return False, 0, 0
            
        try:
            # Prepare features
            features = ['quarter_num', 'seasonal_sin', 'seasonal_cos', 'year']
            X = df[features]
            y = df['y']
            
            # Create polynomial features for better fitting
            self.poly_features = PolynomialFeatures(degree=2, include_bias=False)
            X_poly = self.poly_features.fit_transform(X)
            
            # Train linear regression model
            self.linear_model = LinearRegression()
            self.linear_model.fit(X_poly, y)
            
            # Calculate model performance
            y_pred = self.linear_model.predict(X_poly)
            r2 = r2_score(y, y_pred)
            mae = mean_absolute_error(y, y_pred)
            
            return True, r2, mae
        except Exception as e:
            print(f"Linear model training failed: {e}")
            return False, 0, 0
    
    def predict_future(self, periods=2):
        """
        Generate predictions for future periods using both models
        """
        predictions = []
        
        # Generate future quarters
        last_quarter = self.historical_data['ds'].max()
        future_quarters = []
        
        for i in range(1, periods + 1):
            # Calculate next quarter
            if last_quarter.month <= 3:
                next_q = 2
                next_year = last_quarter.year
            elif last_quarter.month <= 6:
                next_q = 3
                next_year = last_quarter.year
            elif last_quarter.month <= 9:
                next_q = 4
                next_year = last_quarter.year
            else:
                next_q = 1
                next_year = last_quarter.year + 1
            
            future_date = datetime(next_year, (next_q-1)*3 + 1, 1)
            future_quarters.append(future_date)
            last_quarter = future_date
        
        # Prophet predictions
        prophet_predictions = []
        if self.prophet_model:
            future_df = pd.DataFrame({'ds': future_quarters})
            forecast = self.prophet_model.predict(future_df)
            prophet_predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
        
        # Linear model predictions
        linear_predictions = []
        if self.linear_model and self.poly_features:
            for i, future_date in enumerate(future_quarters):
                quarter_num = len(self.historical_data) + i
                year = future_date.year
                quarter = ((future_date.month - 1) // 3) + 1
                
                features = np.array([[
                    quarter_num,
                    np.sin(2 * np.pi * quarter / 4),
                    np.cos(2 * np.pi * quarter / 4),
                    year
                ]])
                
                features_poly = self.poly_features.transform(features)
                pred_value = self.linear_model.predict(features_poly)[0]
                
                linear_predictions.append({
                    'ds': future_date,
                    'predicted_value': pred_value
                })
        
        # Combine predictions (ensemble method)
        for i in range(periods):
            quarter_str = f"{future_quarters[i].year}Q{((future_quarters[i].month-1)//3)+1}"
            
            # Get predictions from both models
            prophet_pred = prophet_predictions[i]['yhat'] if prophet_predictions else 0
            linear_pred = linear_predictions[i]['predicted_value'] if linear_predictions else 0
            
            # Ensemble prediction (weighted average)
            if prophet_pred > 0 and linear_pred > 0:
                # Weight Prophet more for trend, Linear more for seasonality
                ensemble_pred = (prophet_pred * 0.6) + (linear_pred * 0.4)
                confidence = "High"
            elif prophet_pred > 0:
                ensemble_pred = prophet_pred
                confidence = "Medium"
            elif linear_pred > 0:
                ensemble_pred = linear_pred
                confidence = "Medium"
            else:
                # Fallback to simple trend extrapolation
                last_values = self.historical_data['y'].tail(4).values
                trend = np.mean(np.diff(last_values))
                ensemble_pred = self.historical_data['y'].iloc[-1] + (trend * (i + 1))
                confidence = "Low"
            
            # Add confidence intervals
            confidence_interval = ensemble_pred * 0.15  # 15% confidence interval
            
            predictions.append({
                'quarter': quarter_str,
                'predicted_value': max(0, int(ensemble_pred)),
                'prophet_prediction': max(0, int(prophet_pred)) if prophet_pred > 0 else None,
                'linear_prediction': max(0, int(linear_pred)) if linear_pred > 0 else None,
                'confidence_level': confidence,
                'upper_bound': max(0, int(ensemble_pred + confidence_interval)),
                'lower_bound': max(0, int(ensemble_pred - confidence_interval)),
                'is_prediction': True
            })
        
        return predictions
    
    def get_model_performance(self):
        """
        Return model performance metrics
        """
        if not self.historical_data.empty and self.linear_model:
            features = ['quarter_num', 'seasonal_sin', 'seasonal_cos', 'year']
            X = self.historical_data[features]
            y = self.historical_data['y']
            X_poly = self.poly_features.transform(X)
            y_pred = self.linear_model.predict(X_poly)
            
            return {
                'r2_score': round(r2_score(y, y_pred), 3),
                'mean_absolute_error': round(mean_absolute_error(y, y_pred), 2),
                'model_accuracy': round(r2_score(y, y_pred) * 100, 1)
            }
        return None

def generate_ml_predictions(commodity_data, commodity_name):
    """
    Main function to generate ML predictions for a commodity
    """
    predictor = CommodityPredictor()
    
    # Prepare and train models
    df = predictor.prepare_data(commodity_data)
    
    # Train both models
    prophet_success = predictor.train_prophet_model(df)
    linear_success, r2, mae = predictor.train_linear_model(df)
    
    # Generate predictions
    predictions = predictor.predict_future(periods=2)
    
    # Get model performance
    performance = predictor.get_model_performance()
    
    return {
        'predictions': predictions,
        'model_performance': performance,
        'models_used': {
            'prophet': prophet_success,
            'linear_regression': linear_success,
            'ensemble_method': 'Weighted Average (Prophet 60% + Linear 40%)'
        }
    }
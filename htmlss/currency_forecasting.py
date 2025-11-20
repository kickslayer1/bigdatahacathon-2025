"""
Currency Forecasting Module
Uses Prophet and statistical models to forecast 2026 exchange rates
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
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: Scikit-learn not available, using basic predictions")
    SKLEARN_AVAILABLE = False

from currency_analysis import load_currency_data, AVAILABLE_CURRENCIES


class CurrencyForecaster:
    """
    Currency exchange rate forecaster using Prophet and regression models
    """
    
    def __init__(self, currency_code='USD'):
        self.currency_code = currency_code
        self.currency_name = AVAILABLE_CURRENCIES.get(currency_code, currency_code)
        self.historical_data = None
        self.prophet_model = None
        self.linear_model = None
        self.predictions = None
        
    def load_data(self):
        """Load historical currency data"""
        self.historical_data = load_currency_data(self.currency_code)
        if self.historical_data is None or self.historical_data.empty:
            raise ValueError(f"No data available for {self.currency_code}")
        return self
    
    def prepare_prophet_data(self):
        """Prepare data in Prophet format (ds, y columns)"""
        if self.historical_data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        prophet_df = pd.DataFrame({
            'ds': self.historical_data['post_date'],
            'y': self.historical_data['average_rate']
        })
        
        return prophet_df
    
    def train_prophet_model(self):
        """Train Prophet model for forecasting"""
        if not PROPHET_AVAILABLE:
            return None
        
        try:
            # Prepare data
            prophet_df = self.prepare_prophet_data()
            
            # Initialize and train Prophet model
            self.prophet_model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                changepoint_prior_scale=0.05,
                seasonality_prior_scale=10,
                interval_width=0.95
            )
            
            self.prophet_model.fit(prophet_df)
            return self.prophet_model
        
        except Exception as e:
            print(f"Error training Prophet model: {e}")
            return None
    
    def train_linear_model(self):
        """Train polynomial regression model as backup"""
        if not SKLEARN_AVAILABLE:
            return None
        
        try:
            # Prepare data
            df = self.historical_data.copy()
            df['days_since_start'] = (df['post_date'] - df['post_date'].min()).dt.days
            
            X = df[['days_since_start']].values
            y = df['average_rate'].values
            
            # Polynomial features (degree 2)
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            
            # Train model
            self.linear_model = LinearRegression()
            self.linear_model.fit(X_poly, y)
            self.poly_features = poly_features
            
            return self.linear_model
        
        except Exception as e:
            print(f"Error training linear model: {e}")
            return None
    
    def forecast_prophet(self, periods=365):
        """
        Forecast using Prophet model
        
        Args:
            periods: Number of days to forecast
        
        Returns:
            DataFrame with predictions
        """
        if self.prophet_model is None:
            self.train_prophet_model()
        
        if self.prophet_model is None:
            return None
        
        try:
            # Create future dataframe
            future = self.prophet_model.make_future_dataframe(periods=periods)
            
            # Make predictions
            forecast = self.prophet_model.predict(future)
            
            # Filter to forecast period only
            last_date = self.historical_data['post_date'].max()
            forecast_only = forecast[forecast['ds'] > last_date].copy()
            
            return forecast_only[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        
        except Exception as e:
            print(f"Error making Prophet forecast: {e}")
            return None
    
    def forecast_linear(self, periods=365):
        """
        Forecast using polynomial regression
        
        Args:
            periods: Number of days to forecast
        
        Returns:
            DataFrame with predictions
        """
        if self.linear_model is None:
            self.train_linear_model()
        
        if self.linear_model is None:
            return None
        
        try:
            # Get last date and create future dates
            last_date = self.historical_data['post_date'].max()
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=periods)
            
            # Calculate days since start
            start_date = self.historical_data['post_date'].min()
            days_since_start = [(date - start_date).days for date in future_dates]
            
            # Prepare features
            X_future = np.array(days_since_start).reshape(-1, 1)
            X_future_poly = self.poly_features.transform(X_future)
            
            # Make predictions
            predictions = self.linear_model.predict(X_future_poly)
            
            # Create DataFrame
            forecast_df = pd.DataFrame({
                'ds': future_dates,
                'yhat': predictions
            })
            
            return forecast_df
        
        except Exception as e:
            print(f"Error making linear forecast: {e}")
            return None
    
    def forecast_fallback(self, periods=365):
        """
        Simple fallback forecast using moving average and trend
        
        Args:
            periods: Number of days to forecast
        
        Returns:
            DataFrame with predictions
        """
        try:
            df = self.historical_data.copy()
            
            # Calculate trend (last 90 days)
            recent_data = df.tail(90)
            daily_change = (recent_data['average_rate'].iloc[-1] - recent_data['average_rate'].iloc[0]) / len(recent_data)
            
            # Get last date and rate
            last_date = df['post_date'].max()
            last_rate = df['average_rate'].iloc[-1]
            
            # Generate future dates and predictions
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=periods)
            predictions = [last_rate + (daily_change * (i + 1)) for i in range(periods)]
            
            forecast_df = pd.DataFrame({
                'ds': future_dates,
                'yhat': predictions
            })
            
            return forecast_df
        
        except Exception as e:
            print(f"Error in fallback forecast: {e}")
            return None
    
    def forecast_2026(self):
        """
        Forecast exchange rates for 2026
        
        Returns:
            Dictionary with predictions
        """
        # Load data if not already loaded
        if self.historical_data is None:
            self.load_data()
        
        # Calculate days to forecast (to end of 2026)
        last_date = self.historical_data['post_date'].max()
        target_date = datetime(2026, 12, 31)
        days_to_forecast = (target_date - last_date).days
        
        if days_to_forecast <= 0:
            days_to_forecast = 365  # Default to 1 year
        
        # Try Prophet first
        forecast = None
        method_used = None
        
        if PROPHET_AVAILABLE:
            forecast = self.forecast_prophet(days_to_forecast)
            method_used = 'Prophet (FB Time Series)'
        
        # Fallback to linear regression
        if forecast is None and SKLEARN_AVAILABLE:
            forecast = self.forecast_linear(days_to_forecast)
            method_used = 'Polynomial Regression'
        
        # Final fallback
        if forecast is None:
            forecast = self.forecast_fallback(days_to_forecast)
            method_used = 'Trend-based Forecast'
        
        if forecast is None:
            return None
        
        # Prepare results
        result = {
            'currency_code': self.currency_code,
            'currency_name': self.currency_name,
            'method': method_used,
            'forecast_start': forecast['ds'].min().strftime('%Y-%m-%d'),
            'forecast_end': forecast['ds'].max().strftime('%Y-%m-%d'),
            'predictions': []
        }
        
        # Monthly aggregates for 2026
        forecast['year'] = pd.to_datetime(forecast['ds']).dt.year
        forecast['month'] = pd.to_datetime(forecast['ds']).dt.month
        
        forecast_2026 = forecast[forecast['year'] == 2026]
        
        if not forecast_2026.empty:
            monthly_avg = forecast_2026.groupby('month')['yhat'].mean()
            
            for month in range(1, 13):
                if month in monthly_avg.index:
                    result['predictions'].append({
                        'month': month,
                        'month_name': datetime(2026, month, 1).strftime('%B'),
                        'predicted_rate': float(monthly_avg[month])
                    })
        
        # Overall 2026 statistics
        if not forecast_2026.empty:
            result['2026_statistics'] = {
                'min_rate': float(forecast_2026['yhat'].min()),
                'max_rate': float(forecast_2026['yhat'].max()),
                'mean_rate': float(forecast_2026['yhat'].mean()),
                'year_end_rate': float(forecast_2026['yhat'].iloc[-1])
            }
        
        # Add current rate for comparison
        result['current_rate'] = float(self.historical_data['average_rate'].iloc[-1])
        result['current_date'] = self.historical_data['post_date'].max().strftime('%Y-%m-%d')
        
        # Calculate projected change
        if 'year_end_rate' in result.get('2026_statistics', {}):
            year_end = result['2026_statistics']['year_end_rate']
            current = result['current_rate']
            result['projected_change'] = float(year_end - current)
            result['projected_change_percent'] = float(((year_end - current) / current) * 100)
        
        # Add full daily predictions for charting
        result['daily_forecast'] = {
            'dates': [d.strftime('%Y-%m-%d') for d in forecast['ds']],
            'rates': [float(r) for r in forecast['yhat']]
        }
        
        # Add confidence intervals if available (Prophet)
        if 'yhat_lower' in forecast.columns and 'yhat_upper' in forecast.columns:
            result['daily_forecast']['lower_bound'] = [float(r) for r in forecast['yhat_lower']]
            result['daily_forecast']['upper_bound'] = [float(r) for r in forecast['yhat_upper']]
        
        self.predictions = result
        return result


def forecast_2026(df, currency_code='USD'):
    """
    Standalone function to forecast 2026 exchange rates
    
    Args:
        df: DataFrame with historical currency data
        currency_code: Currency code (USD, EUR, CNY, TSH)
    
    Returns:
        Dictionary with forecast results
    """
    try:
        forecaster = CurrencyForecaster(currency_code)
        forecaster.historical_data = df
        return forecaster.forecast_2026()
    except Exception as e:
        return {'error': str(e)}


def forecast_all_currencies():
    """
    Forecast 2026 rates for all available currencies
    
    Returns:
        Dictionary with forecasts for all currencies
    """
    results = {}
    
    for code in AVAILABLE_CURRENCIES.keys():
        try:
            print(f"Forecasting {code}...")
            df = load_currency_data(code)
            if df is not None and not df.empty:
                forecast = forecast_2026(df, code)
                if forecast and 'error' not in forecast:
                    results[code] = forecast
        except Exception as e:
            print(f"Error forecasting {code}: {e}")
            continue
    
    return results


def get_currency_forecast_summary(currency_code='USD'):
    """
    Get a quick summary of currency forecast
    
    Args:
        currency_code: Currency code
    
    Returns:
        Dictionary with summary
    """
    try:
        forecaster = CurrencyForecaster(currency_code)
        forecast = forecaster.forecast_2026()
        
        if not forecast:
            return None
        
        summary = {
            'currency': f"{currency_code} ({AVAILABLE_CURRENCIES.get(currency_code, '')})",
            'current_rate': forecast['current_rate'],
            'projected_2026_avg': forecast['2026_statistics']['mean_rate'],
            'projected_change': forecast.get('projected_change_percent', 0),
            'trend': 'depreciating' if forecast.get('projected_change_percent', 0) > 0 else 'appreciating',
            'method': forecast['method']
        }
        
        return summary
    
    except Exception as e:
        print(f"Error generating summary for {currency_code}: {e}")
        return None


# Testing
if __name__ == '__main__':
    print("Testing Currency Forecasting Module...")
    print("=" * 60)
    
    # Test USD forecast
    print("\n1. USD Forecast for 2026:")
    try:
        forecaster = CurrencyForecaster('USD')
        forecast = forecaster.forecast_2026()
        
        if forecast:
            print(f"  Method: {forecast['method']}")
            print(f"  Current Rate: {forecast['current_rate']:.2f} RWF ({forecast['current_date']})")
            
            if '2026_statistics' in forecast:
                stats = forecast['2026_statistics']
                print(f"  2026 Projected Average: {stats['mean_rate']:.2f} RWF")
                print(f"  2026 Year-End: {stats['year_end_rate']:.2f} RWF")
                print(f"  Projected Change: {forecast.get('projected_change_percent', 0):.2f}%")
            
            print(f"\n  Monthly Predictions (sample):")
            for pred in forecast['predictions'][:3]:
                print(f"    {pred['month_name']} 2026: {pred['predicted_rate']:.2f} RWF")
    
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n2. Quick Summary for All Currencies:")
    for code in ['USD', 'EUR', 'CNY', 'TSH']:
        summary = get_currency_forecast_summary(code)
        if summary:
            print(f"  {summary['currency']}: {summary['projected_2026_avg']:.2f} RWF (Change: {summary['projected_change']:.2f}%)")

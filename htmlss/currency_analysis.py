"""
Currency Analysis Module
Loads and processes exchange rate data from CSV files
Provides statistical analysis and data preparation for visualization
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import json

# Currency data directory
CURRENCY_DIR = os.path.join(os.path.dirname(__file__), 'currency')

# Available currencies
AVAILABLE_CURRENCIES = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'CNY': 'Chinese Yuan',
    'TSH': 'Tanzanian Shilling'
}

def load_currency_data(currency_code='USD'):
    """
    Load exchange rate data from CSV file
    
    Args:
        currency_code: Currency code (USD, EUR, CNY, TSH)
    
    Returns:
        DataFrame with exchange rate data
    """
    try:
        file_path = os.path.join(CURRENCY_DIR, f'{currency_code.lower()}_table.csv')
        
        if not os.path.exists(file_path):
            print(f"Currency file not found: {file_path}")
            return None
        
        # Load CSV data
        df = pd.read_csv(file_path)
        
        # Convert post_date to datetime
        df['post_date'] = pd.to_datetime(df['post_date'], format='%m/%d/%Y')
        
        # Convert rates to float (remove commas if present)
        for col in ['buying_rate', 'average_rate', 'selling_rate']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').astype(float)
        
        # Sort by date
        df = df.sort_values('post_date')
        
        return df
    
    except Exception as e:
        print(f"Error loading currency data for {currency_code}: {e}")
        return None


def get_currency_data_by_period(currency_code='USD', start_date=None, end_date=None):
    """
    Get currency data for a specific period
    
    Args:
        currency_code: Currency code
        start_date: Start date (string or datetime)
        end_date: End date (string or datetime)
    
    Returns:
        Filtered DataFrame
    """
    df = load_currency_data(currency_code)
    
    if df is None:
        return None
    
    # Filter by date range
    if start_date:
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        df = df[df['post_date'] >= start_date]
    
    if end_date:
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        df = df[df['post_date'] <= end_date]
    
    return df


def calculate_currency_statistics(currency_code='USD', period_days=365):
    """
    Calculate statistical metrics for currency data
    
    Args:
        currency_code: Currency code
        period_days: Number of days to analyze
    
    Returns:
        Dictionary with statistics
    """
    df = load_currency_data(currency_code)
    
    if df is None or df.empty:
        return None
    
    # Get recent period
    end_date = df['post_date'].max()
    start_date = end_date - timedelta(days=period_days)
    period_df = df[df['post_date'] >= start_date]
    
    if period_df.empty:
        return None
    
    stats = {
        'currency_code': currency_code,
        'currency_name': AVAILABLE_CURRENCIES.get(currency_code, currency_code),
        'period_days': period_days,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        
        # Current rates
        'current_buying': float(period_df['buying_rate'].iloc[-1]),
        'current_average': float(period_df['average_rate'].iloc[-1]),
        'current_selling': float(period_df['selling_rate'].iloc[-1]),
        
        # Period statistics
        'min_rate': float(period_df['average_rate'].min()),
        'max_rate': float(period_df['average_rate'].max()),
        'mean_rate': float(period_df['average_rate'].mean()),
        'std_rate': float(period_df['average_rate'].std()),
        
        # Changes
        'period_change': float(period_df['average_rate'].iloc[-1] - period_df['average_rate'].iloc[0]),
        'period_change_percent': float(((period_df['average_rate'].iloc[-1] - period_df['average_rate'].iloc[0]) / period_df['average_rate'].iloc[0]) * 100),
        
        # Volatility
        'volatility': float(period_df['average_rate'].pct_change().std() * 100),
    }
    
    # Recent trend (last 30 days vs previous 30 days)
    if len(period_df) > 60:
        recent_30 = period_df.tail(30)['average_rate'].mean()
        previous_30 = period_df.tail(60).head(30)['average_rate'].mean()
        stats['trend'] = 'appreciating' if recent_30 < previous_30 else 'depreciating'
        stats['trend_strength'] = float(abs((recent_30 - previous_30) / previous_30) * 100)
    else:
        stats['trend'] = 'neutral'
        stats['trend_strength'] = 0.0
    
    return stats


def get_multi_currency_comparison(period_days=365):
    """
    Compare multiple currencies over a period
    
    Args:
        period_days: Number of days to analyze
    
    Returns:
        Dictionary with comparison data
    """
    comparison = {
        'period_days': period_days,
        'currencies': []
    }
    
    for code, name in AVAILABLE_CURRENCIES.items():
        stats = calculate_currency_statistics(code, period_days)
        if stats:
            comparison['currencies'].append(stats)
    
    return comparison


def prepare_chart_data(currency_code='USD', start_date=None, end_date=None):
    """
    Prepare data for Chart.js visualization
    
    Args:
        currency_code: Currency code
        start_date: Start date
        end_date: End date
    
    Returns:
        Dictionary with chart-ready data
    """
    df = get_currency_data_by_period(currency_code, start_date, end_date)
    
    if df is None or df.empty:
        return None
    
    # Convert to chart format
    chart_data = {
        'labels': df['post_date'].dt.strftime('%Y-%m-%d').tolist(),
        'buying_rate': df['buying_rate'].tolist(),
        'average_rate': df['average_rate'].tolist(),
        'selling_rate': df['selling_rate'].tolist(),
        'currency_code': currency_code,
        'currency_name': AVAILABLE_CURRENCIES.get(currency_code, currency_code)
    }
    
    return chart_data


def get_currency_spread_analysis(currency_code='USD', period_days=30):
    """
    Analyze the spread between buying and selling rates
    
    Args:
        currency_code: Currency code
        period_days: Number of days to analyze
    
    Returns:
        Dictionary with spread analysis
    """
    df = load_currency_data(currency_code)
    
    if df is None or df.empty:
        return None
    
    # Get recent period
    end_date = df['post_date'].max()
    start_date = end_date - timedelta(days=period_days)
    period_df = df[df['post_date'] >= start_date]
    
    # Calculate spread
    period_df['spread'] = period_df['selling_rate'] - period_df['buying_rate']
    period_df['spread_percent'] = (period_df['spread'] / period_df['average_rate']) * 100
    
    analysis = {
        'currency_code': currency_code,
        'average_spread': float(period_df['spread'].mean()),
        'average_spread_percent': float(period_df['spread_percent'].mean()),
        'min_spread': float(period_df['spread'].min()),
        'max_spread': float(period_df['spread'].max()),
        'current_spread': float(period_df['spread'].iloc[-1]),
        'spread_volatility': float(period_df['spread'].std())
    }
    
    return analysis


def get_year_over_year_comparison(currency_code='USD'):
    """
    Compare current year vs previous year exchange rates
    
    Args:
        currency_code: Currency code
    
    Returns:
        Dictionary with YoY comparison
    """
    df = load_currency_data(currency_code)
    
    if df is None or df.empty:
        return None
    
    current_date = df['post_date'].max()
    one_year_ago = current_date - timedelta(days=365)
    
    # Get rates
    current_rate = df[df['post_date'] == current_date]['average_rate'].iloc[0] if len(df[df['post_date'] == current_date]) > 0 else df['average_rate'].iloc[-1]
    
    # Find closest date to one year ago
    year_ago_df = df[df['post_date'] >= one_year_ago].head(1)
    if year_ago_df.empty:
        return None
    
    year_ago_rate = year_ago_df['average_rate'].iloc[0]
    
    comparison = {
        'currency_code': currency_code,
        'current_date': current_date.strftime('%Y-%m-%d'),
        'current_rate': float(current_rate),
        'year_ago_date': year_ago_df['post_date'].iloc[0].strftime('%Y-%m-%d'),
        'year_ago_rate': float(year_ago_rate),
        'yoy_change': float(current_rate - year_ago_rate),
        'yoy_change_percent': float(((current_rate - year_ago_rate) / year_ago_rate) * 100)
    }
    
    return comparison


def get_all_available_currencies():
    """
    Get list of available currencies with their file status
    
    Returns:
        List of dictionaries with currency info
    """
    currencies = []
    
    for code, name in AVAILABLE_CURRENCIES.items():
        file_path = os.path.join(CURRENCY_DIR, f'{code.lower()}_table.csv')
        available = os.path.exists(file_path)
        
        if available:
            df = load_currency_data(code)
            if df is not None and not df.empty:
                currencies.append({
                    'code': code,
                    'name': name,
                    'available': True,
                    'data_points': len(df),
                    'start_date': df['post_date'].min().strftime('%Y-%m-%d'),
                    'end_date': df['post_date'].max().strftime('%Y-%m-%d')
                })
            else:
                currencies.append({
                    'code': code,
                    'name': name,
                    'available': False
                })
        else:
            currencies.append({
                'code': code,
                'name': name,
                'available': False
            })
    
    return currencies


# Testing function
if __name__ == '__main__':
    print("Testing Currency Analysis Module...")
    print("\n1. Available Currencies:")
    currencies = get_all_available_currencies()
    for curr in currencies:
        print(f"  - {curr['code']} ({curr['name']}): {'Available' if curr['available'] else 'Not Available'}")
        if curr['available']:
            print(f"    Data points: {curr['data_points']}, Range: {curr['start_date']} to {curr['end_date']}")
    
    print("\n2. USD Statistics (Last 365 days):")
    stats = calculate_currency_statistics('USD', 365)
    if stats:
        print(f"  Current Rate: {stats['current_average']:.2f} RWF")
        print(f"  Year Change: {stats['period_change_percent']:.2f}%")
        print(f"  Trend: {stats['trend']} ({stats['trend_strength']:.2f}%)")
        print(f"  Volatility: {stats['volatility']:.2f}%")
    
    print("\n3. Currency Spread Analysis (USD):")
    spread = get_currency_spread_analysis('USD', 30)
    if spread:
        print(f"  Average Spread: {spread['average_spread']:.2f} RWF ({spread['average_spread_percent']:.2f}%)")
        print(f"  Current Spread: {spread['current_spread']:.2f} RWF")
    
    print("\n4. Year-over-Year Comparison (USD):")
    yoy = get_year_over_year_comparison('USD')
    if yoy:
        print(f"  Current: {yoy['current_rate']:.2f} RWF ({yoy['current_date']})")
        print(f"  Year Ago: {yoy['year_ago_rate']:.2f} RWF ({yoy['year_ago_date']})")
        print(f"  Change: {yoy['yoy_change_percent']:.2f}%")

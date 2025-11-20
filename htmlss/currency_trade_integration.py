"""
Currency-Trade Integration Module
Enhances currency predictions by incorporating trade balance data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from currency_analysis import load_currency_data, AVAILABLE_CURRENCIES
from db import get_db_connection

def get_trade_balance_data():
    """
    Fetch trade balance data from database
    
    Returns:
        DataFrame with period, exports, imports, trade_balance
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT period, exports, imports FROM exportss")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not data:
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=['period', 'exports', 'imports'])
        
        # Calculate trade balance (exports - imports)
        df['trade_balance'] = df['exports'] - df['imports']
        
        # Calculate trade balance as % of total trade
        df['total_trade'] = df['exports'] + df['imports']
        df['trade_balance_pct'] = (df['trade_balance'] / df['total_trade']) * 100
        
        # Convert period to datetime (assuming format like "2024Q1")
        df['year'] = df['period'].str.extract(r'(\d{4})').astype(int)
        df['quarter'] = df['period'].str.extract(r'Q(\d)').astype(int)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + 
                                      ((df['quarter'] - 1) * 3 + 1).astype(str) + '-01')
        
        return df.sort_values('date')
    
    except Exception as e:
        print(f"Error loading trade balance data: {e}")
        return None


def align_currency_with_trade(currency_code='USD'):
    """
    Align currency exchange rates with trade balance data
    
    Args:
        currency_code: Currency code
    
    Returns:
        DataFrame with both currency rates and trade metrics
    """
    # Load currency data
    currency_df = load_currency_data(currency_code)
    if currency_df is None:
        return None
    
    # Load trade balance data
    trade_df = get_trade_balance_data()
    if trade_df is None:
        return currency_df  # Return currency data only if trade data unavailable
    
    # Aggregate currency data by quarter to match trade data
    currency_df['year'] = currency_df['post_date'].dt.year
    currency_df['quarter'] = currency_df['post_date'].dt.quarter
    
    # Calculate average exchange rate per quarter
    currency_quarterly = currency_df.groupby(['year', 'quarter']).agg({
        'average_rate': 'mean',
        'buying_rate': 'mean',
        'selling_rate': 'mean',
        'post_date': 'max'
    }).reset_index()
    
    # Create period column for matching
    currency_quarterly['period'] = (currency_quarterly['year'].astype(str) + 
                                    'Q' + currency_quarterly['quarter'].astype(str))
    
    # Merge with trade data
    merged_df = pd.merge(currency_quarterly, 
                         trade_df[['period', 'exports', 'imports', 'trade_balance', 
                                   'trade_balance_pct', 'total_trade']], 
                         on='period', 
                         how='left')
    
    # Calculate correlations
    if len(merged_df) > 10:  # Need sufficient data for correlation
        merged_df['rate_change'] = merged_df['average_rate'].pct_change() * 100
        merged_df['trade_balance_change'] = merged_df['trade_balance'].pct_change() * 100
    
    return merged_df


def calculate_trade_impact_score(currency_code='USD', period_quarters=4):
    """
    Calculate how much trade balance impacts currency movement
    
    Args:
        currency_code: Currency code
        period_quarters: Number of quarters to analyze
    
    Returns:
        Dictionary with trade impact metrics
    """
    merged_df = align_currency_with_trade(currency_code)
    
    if merged_df is None or len(merged_df) < 2:
        return {
            'error': 'Insufficient data for trade impact analysis',
            'correlation': None
        }
    
    # Get recent period
    recent_df = merged_df.tail(period_quarters)
    
    # Calculate correlation between trade balance and exchange rate
    if len(recent_df) > 2 and 'trade_balance' in recent_df.columns:
        correlation = recent_df[['average_rate', 'trade_balance']].corr().iloc[0, 1]
    else:
        correlation = None
    
    # Calculate average trade metrics
    avg_trade_balance = recent_df['trade_balance'].mean() if 'trade_balance' in recent_df.columns else 0
    avg_exports = recent_df['exports'].mean() if 'exports' in recent_df.columns else 0
    avg_imports = recent_df['imports'].mean() if 'imports' in recent_df.columns else 0
    
    # Determine trade impact
    if correlation is not None:
        if abs(correlation) > 0.7:
            impact_level = 'High'
        elif abs(correlation) > 0.4:
            impact_level = 'Moderate'
        else:
            impact_level = 'Low'
    else:
        impact_level = 'Unknown'
    
    # Trade balance trend
    if 'trade_balance' in recent_df.columns and len(recent_df) > 1:
        latest_balance = recent_df['trade_balance'].iloc[-1]
        previous_balance = recent_df['trade_balance'].iloc[-2]
        
        # Handle NaN values
        if pd.isna(latest_balance):
            latest_balance = avg_trade_balance
        if pd.isna(previous_balance):
            previous_balance = avg_trade_balance
            
        balance_trend = 'Improving' if latest_balance > previous_balance else 'Declining'
    else:
        latest_balance = avg_trade_balance
        balance_trend = 'Neutral'
    
    return {
        'currency_code': currency_code,
        'currency_name': AVAILABLE_CURRENCIES.get(currency_code, currency_code),
        'correlation': float(correlation) if correlation is not None else None,
        'impact_level': impact_level,
        'period_quarters': period_quarters,
        
        # Trade metrics (in millions USD)
        'avg_exports': float(avg_exports),
        'avg_imports': float(avg_imports),
        'avg_trade_balance': float(avg_trade_balance),
        'latest_trade_balance': float(latest_balance),
        'trade_balance_trend': balance_trend,
        
        # Interpretation
        'interpretation': f"Trade balance shows {impact_level.lower()} correlation with {currency_code} exchange rate. "
                         f"Current trade balance is {balance_trend.lower()}, "
                         f"which may {'support' if balance_trend == 'Improving' else 'pressure'} the currency."
    }


def get_trade_adjusted_forecast(currency_code='USD', base_forecast=None, trade_adjustment_weight=0.3):
    """
    Adjust currency forecast based on trade balance trends
    
    Args:
        currency_code: Currency code
        base_forecast: Base forecast data from Prophet/regression
        trade_adjustment_weight: How much to weight trade data (0-1)
    
    Returns:
        Adjusted forecast with trade considerations
    """
    if base_forecast is None:
        return None
    
    # Get trade impact
    trade_impact = calculate_trade_impact_score(currency_code, period_quarters=8)
    
    if trade_impact.get('correlation') is None:
        # No adjustment if no correlation data
        base_forecast['trade_adjusted'] = False
        base_forecast['trade_impact'] = 'No trade data available for adjustment'
        return base_forecast
    
    # Calculate adjustment factor based on trade balance trend
    correlation = trade_impact['correlation']
    balance_trend = trade_impact['trade_balance_trend']
    
    # Adjustment logic:
    # - Negative correlation means: trade deficit → currency depreciates (rate increases)
    # - Positive correlation means: trade deficit → currency appreciates (rare, but possible)
    
    if balance_trend == 'Improving':
        # Improving trade balance (less deficit or more surplus)
        if correlation < 0:
            # Normal case: better trade balance → currency appreciates (rate decreases)
            adjustment_factor = -abs(correlation) * trade_adjustment_weight * 0.01
        else:
            adjustment_factor = abs(correlation) * trade_adjustment_weight * 0.01
    else:
        # Declining trade balance (worse deficit)
        if correlation < 0:
            # Normal case: worse trade balance → currency depreciates (rate increases)
            adjustment_factor = abs(correlation) * trade_adjustment_weight * 0.01
        else:
            adjustment_factor = -abs(correlation) * trade_adjustment_weight * 0.01
    
    # Apply adjustment to predictions
    if 'predictions' in base_forecast:
        for pred in base_forecast['predictions']:
            original_rate = pred['predicted_rate']
            adjusted_rate = original_rate * (1 + adjustment_factor)
            pred['trade_adjusted_rate'] = float(adjusted_rate)
            pred['trade_adjustment_pct'] = float(adjustment_factor * 100)
    
    # Update 2026 statistics
    if '2026_statistics' in base_forecast:
        stats = base_forecast['2026_statistics']
        for key in ['mean_rate', 'min_rate', 'max_rate', 'year_end_rate']:
            if key in stats:
                stats[f'{key}_trade_adjusted'] = float(stats[key] * (1 + adjustment_factor))
    
    # Add trade metadata
    base_forecast['trade_adjusted'] = True
    base_forecast['trade_adjustment_factor'] = float(adjustment_factor)
    base_forecast['trade_correlation'] = float(correlation)
    base_forecast['trade_impact'] = trade_impact
    base_forecast['adjustment_explanation'] = (
        f"Trade balance is {balance_trend.lower()}, with correlation of {correlation:.3f}. "
        f"Forecast adjusted by {adjustment_factor*100:.2f}% based on trade trends."
    )
    
    return base_forecast


def get_trade_currency_comparison():
    """
    Compare all currencies with their trade balance correlations
    
    Returns:
        List of currencies with trade impact scores
    """
    results = []
    
    for code in AVAILABLE_CURRENCIES.keys():
        impact = calculate_trade_impact_score(code, period_quarters=8)
        if impact and 'error' not in impact:
            results.append(impact)
    
    return results


# Testing
if __name__ == '__main__':
    print("Testing Currency-Trade Integration Module...")
    print("=" * 60)
    
    # Test 1: Load trade balance data
    print("\n1. Trade Balance Data:")
    trade_df = get_trade_balance_data()
    if trade_df is not None:
        print(f"   Loaded {len(trade_df)} quarters of trade data")
        print(f"   Latest period: {trade_df['period'].iloc[-1]}")
        print(f"   Latest trade balance: ${trade_df['trade_balance'].iloc[-1]:.2f}M")
    else:
        print("   No trade data available")
    
    # Test 2: Align USD with trade data
    print("\n2. USD-Trade Alignment:")
    merged_df = align_currency_with_trade('USD')
    if merged_df is not None:
        print(f"   Aligned {len(merged_df)} quarters")
        if 'trade_balance' in merged_df.columns:
            print(f"   Average exchange rate: {merged_df['average_rate'].mean():.2f} RWF")
            print(f"   Average trade balance: ${merged_df['trade_balance'].mean():.2f}M")
    
    # Test 3: Calculate trade impact
    print("\n3. Trade Impact on USD:")
    impact = calculate_trade_impact_score('USD', period_quarters=8)
    if impact and 'error' not in impact:
        print(f"   Correlation: {impact['correlation']:.3f}")
        print(f"   Impact Level: {impact['impact_level']}")
        print(f"   Trade Balance Trend: {impact['trade_balance_trend']}")
        print(f"   Interpretation: {impact['interpretation']}")
    
    # Test 4: Compare all currencies
    print("\n4. All Currencies Trade Impact:")
    comparison = get_trade_currency_comparison()
    for result in comparison:
        print(f"   {result['currency_code']}: Correlation={result['correlation']:.3f}, "
              f"Impact={result['impact_level']}")

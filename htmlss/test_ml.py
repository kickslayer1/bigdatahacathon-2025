#!/usr/bin/env python3
"""
Test script for ML prediction system
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_ml_system():
    try:
        from ml_predictions import generate_ml_predictions
        print("✅ ML module import successful")
        
        # Create test data
        test_data = []
        for i, year in enumerate(range(2020, 2026)):
            for q in range(1, 5):
                if year == 2025 and q > 2:
                    break
                test_data.append({
                    'quarter': f'{year}Q{q}',
                    'value': 1000000 + i * 4 * 50000 + q * 10000
                })
        
        print(f"Test data created: {len(test_data)} quarters")
        
        # Test ML predictions
        result = generate_ml_predictions(test_data, 'Gold')
        print("✅ ML prediction generation successful")
        print(f"Predictions: {len(result['predictions'])} periods")
        
        for pred in result['predictions']:
            print(f"  {pred['quarter']}: ${pred['predicted_value']:,} ({pred['confidence_level']} confidence)")
        
        if result['model_performance']:
            perf = result['model_performance']
            print(f"\nModel Performance:")
            print(f"  Accuracy: {perf['model_accuracy']}%")
            print(f"  R² Score: {perf['r2_score']}")
            print(f"  MAE: ${perf['mean_absolute_error']:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ml_system()
    if success:
        print("\n🎉 All ML systems working correctly!")
    else:
        print("\n❌ ML system has issues")
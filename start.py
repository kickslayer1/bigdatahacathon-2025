"""
Quick Start Script for Rwanda Trade Dashboard
"""
import os
import sys
from pathlib import Path

def main():
    print("🚀 Rwanda Trade Dashboard - Quick Start")
    print("=" * 50)
    
    # Set up paths
    current_dir = Path(__file__).parent
    htmlss_dir = current_dir / "htmlss"
    sys.path.insert(0, str(htmlss_dir))
    
    try:
        # Import and start the app directly
        print("📱 Starting application...")
        from app import app
        
        print("✅ Application loaded successfully!")
        print()
        print("🌐 Server starting on http://localhost:5000")
        print("📊 Main Dashboard: http://localhost:5000/")
        print("🌍 Global Trade: http://localhost:5000/htmlss/global_trade_2025.html")
        print("📈 Demand Prediction: http://localhost:5000/htmlss/demand_prediction_2026.html")
        print("🏠 Front Page: http://localhost:5000/htmlss/front_page.html")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the Flask app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Installing required packages...")
        
        import subprocess
        packages = ["mysql-connector-python", "flask", "numpy", "pandas", "scikit-learn"]
        
        for package in packages:
            try:
                print(f"📦 Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                    capture_output=True, text=True)
                print(f"✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
        
        # Try again
        try:
            from app import app
            print("✅ Dependencies installed! Starting application...")
            app.run(host='0.0.0.0', port=5000, debug=True)
        except Exception as e2:
            print(f"❌ Still having issues: {e2}")
            print("📝 Please check your database is running and accessible")
    
    except Exception as e:
        print(f"❌ Application error: {e}")
        print("📝 Please check your database configuration")

if __name__ == "__main__":
    main()
"""
Simple Deployment Script for Rwanda Trade Dashboard
"""
import os
import sys
import subprocess
from pathlib import Path

def install_package(package_name):
    """Install package using python -m pip"""
    try:
        print(f"📦 Installing {package_name}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package_name}: {e}")
        return False

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "mysql-connector-python",
        "flask",
        "numpy", 
        "pandas",
        "scikit-learn",
        "prophet"
    ]
    
    print("🔍 Checking dependencies...")
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "mysql-connector-python":
                import mysql.connector
            elif package == "flask":
                import flask
            elif package == "numpy":
                import numpy
            elif package == "pandas":
                import pandas
            elif package == "scikit-learn":
                import sklearn
            elif package == "prophet":
                import prophet
            print(f"✅ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"🔧 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            if not install_package(package):
                return False
    
    return True

def main():
    print("🚀 Rwanda Trade Dashboard Deployment")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path(__file__).parent
    htmlss_dir = current_dir / "htmlss"
    
    # Check if htmlss directory exists
    if not htmlss_dir.exists():
        print("❌ htmlss directory not found!")
        return False
    
    # Add htmlss to Python path
    sys.path.insert(0, str(htmlss_dir))
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency installation failed!")
        return False
    
    print("✅ All dependencies satisfied!")
    
    # Try to import and run the app
    try:
        print("📱 Importing application...")
        from app import app
        
        print("✅ Application imported successfully!")
        print()
        print("🌐 Starting server...")
        print("📊 Dashboard URL: http://localhost:5000")
        print("🔗 Global Trade: http://localhost:5000/htmlss/global_trade_2025.html")
        print("📈 Demand Prediction: http://localhost:5000/htmlss/demand_prediction_2026.html")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the application
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
        
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        print("📝 Please check your database configuration in htmlss/db.py")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
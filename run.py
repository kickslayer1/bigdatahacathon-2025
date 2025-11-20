"""
Production-ready deployment script for Rwanda Trade Dashboard
"""
import os
import sys
from pathlib import Path

# Add the htmlss directory to Python path for imports
current_dir = Path(__file__).parent
htmlss_dir = current_dir / "htmlss"
sys.path.insert(0, str(htmlss_dir))
sys.path.insert(0, str(current_dir))

print("🚀 Starting Rwanda Trade Dashboard...")

# Try to run your current working application
try:
    from app import app
    print("✅ Successfully imported application")
    print("🌐 Starting server on http://localhost:5000")
    print("� Dashboard will be available shortly...")
    
    # Start the application
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📝 Checking for database dependencies...")
    
    # Try to install missing dependencies
    try:
        import subprocess
        print("🔧 Installing missing database dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python", "pymysql"])
        
        # Try again
        from app import app
        print("✅ Dependencies installed, starting application...")
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
        
    except Exception as e2:
        print(f"❌ Could not resolve dependencies: {e2}")
        print("📝 Please check your database configuration")
        sys.exit(1)
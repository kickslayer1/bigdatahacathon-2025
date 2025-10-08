@echo off
echo 🚀 Rwanda Trade Dashboard - Quick Start Script
echo ====================================================

echo 📁 Navigating to application directory...
cd /d "C:\Users\USER\Documents\bigdatahacathon-2025\htmlss"

echo 🔍 Checking Python environment...
python --version

echo 📦 Installing dependencies if needed...
python -m pip install mysql-connector-python flask numpy pandas scikit-learn prophet matplotlib flask-cors werkzeug jinja2

echo ✅ Starting Rwanda Trade Dashboard...
echo 🌐 Your dashboard will be available at: http://localhost:5000
echo 📊 Press Ctrl+C to stop the server
echo ====================================================

python app.py

pause
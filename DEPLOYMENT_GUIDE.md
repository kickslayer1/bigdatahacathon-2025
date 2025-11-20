# 🚀 Rwanda Trade Dashboard - Deployment Guide

## Quick Start (Recommended)

### Option 1: Local Development Server
```bash
# Navigate to your project directory
cd C:\Users\USER\Documents\bigdatahacathon-2025

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies using python -m pip
python -m pip install mysql-connector-python flask numpy pandas scikit-learn prophet

# Start the application
python start.py
```

### Option 2: Direct Run (Current Working App)
```bash
# Navigate to htmlss directory
cd C:\Users\USER\Documents\bigdatahacathon-2025\htmlss

# Run the app directly
python app.py
```

## 🌐 Access Your Application

Once running, visit:
- **Main Gateway**: http://localhost:5000/
- **Global Trade Dashboard**: http://localhost:5000/htmlss/global_trade_2025.html
- **Demand Prediction**: http://localhost:5000/htmlss/demand_prediction_2026.html
- **Front Page**: http://localhost:5000/htmlss/front_page.html

## 🏗️ Production Deployment Options

### Option 1: Heroku (Easiest Cloud Deployment)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Deploy Commands**:
```bash
# Login to Heroku
heroku login

# Create app
heroku create rwanda-trade-dashboard

# Set environment variables
heroku config:set DATABASE_URL=your_database_url
heroku config:set SECRET_KEY=your_secret_key

# Deploy
git add .
git commit -m "Deploy Rwanda Trade Dashboard"
git push heroku main
```

### Option 2: Docker Deployment

1. **Build and Run**:
```bash
# Build Docker image
docker build -t rwanda-trade-dashboard .

# Run container
docker run -p 5000:5000 -e DATABASE_HOST=host.docker.internal rwanda-trade-dashboard
```

2. **Docker Compose (with MySQL)**:
```bash
# Start full stack
docker-compose up -d
```

### Option 3: DigitalOcean Droplet

1. **Create Ubuntu 22.04 Droplet** ($5/month)
2. **Setup Commands**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv mysql-server -y

# Clone your repository
git clone https://github.com/kickslayer1/bigdatahacathon-2025.git
cd bigdatahacathon-2025

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages using python -m pip
python -m pip install -r requirements.txt

# Configure MySQL
sudo mysql_secure_installation

# Create database
sudo mysql -u root -p
CREATE DATABASE bigdatahackaton;
# Import your database dump

# Run application
python start.py
```

### Option 4: AWS Elastic Beanstalk

1. **Install EB CLI**: `pip install awsebcli`
2. **Deploy**:
```bash
eb init rwanda-trade-dashboard
eb create production
eb deploy
```

## 🔧 Environment Configuration

Create `.env` file:
```bash
# Database Configuration
DATABASE_HOST=localhost
DATABASE_NAME=bigdatahackaton
DATABASE_USER=root
DATABASE_PASSWORD=your_password

# Application Settings
PORT=5000
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
```

## 📦 Required Dependencies

Install using `python -m pip`:
```bash
python -m pip install flask mysql-connector-python numpy pandas scikit-learn prophet flask-cors matplotlib werkzeug jinja2
```

## 🛠️ Troubleshooting

### Database Connection Issues
1. **Check MySQL is running**:
   - Windows: Services → MySQL80 → Start
   - Linux: `sudo systemctl start mysql`

2. **Verify database exists**:
```sql
SHOW DATABASES;
USE bigdatahackaton;
SHOW TABLES;
```

3. **Test connection**:
```python
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='kickslayer',
    database='bigdatahackaton'
)
print("✅ Database connected!")
```

### Package Installation Issues
1. **Use python -m pip** instead of just pip
2. **Update pip first**: `python -m pip install --upgrade pip`
3. **Use virtual environment**: Always activate `.venv`

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <process_id> /F

# Or use different port
export PORT=8000
python start.py
```

## 🚀 Sharing Your Application

### Method 1: ngrok (Quick Public Access)
```bash
# Install ngrok: https://ngrok.com/
ngrok http 5000

# Share the ngrok URL (e.g., https://abc123.ngrok.io)
```

### Method 2: GitHub + Heroku
1. **Push to GitHub**:
```bash
git add .
git commit -m "Rwanda Trade Dashboard"
git push origin main
```

2. **Deploy to Heroku from GitHub** (free tier available)

### Method 3: Render.com (Free Alternative to Heroku)
1. **Connect GitHub repository**
2. **Deploy with one click**
3. **Free tier includes SSL**

## 📊 Monitoring & Maintenance

### Health Checks
- Application: http://your-domain.com/health
- Database: Monitor connection pool
- Performance: Use application logs

### Backup Strategy
```bash
# Database backup
mysqldump -u root -p bigdatahackaton > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz .
```

## 🎯 Next Steps After Deployment

1. **SSL Certificate**: Use Let's Encrypt or CloudFlare
2. **Domain Name**: Register custom domain
3. **CDN**: Use CloudFlare for global performance
4. **Monitoring**: Set up uptime monitoring
5. **Analytics**: Add Google Analytics
6. **API Keys**: Secure external API integrations

## 📞 Support

If you need help:
1. Check application logs: `tail -f app.log`
2. Verify database connectivity
3. Ensure all dependencies are installed with `python -m pip`
4. Test locally before deploying to production

Your Rwanda Trade Dashboard is now ready for the world! 🌍
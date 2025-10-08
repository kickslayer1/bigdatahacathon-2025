#!/bin/bash

# Rwanda Trade Dashboard Deployment Script

set -e

echo "🚀 Starting deployment of Rwanda Trade Dashboard..."

# Configuration
APP_NAME="rwanda-trade-dashboard"
APP_DIR="/opt/$APP_NAME"
BACKUP_DIR="/opt/backups/$APP_NAME"
PYTHON_VERSION="3.11"

# Create backup
echo "📦 Creating backup..."
if [ -d "$APP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).tar.gz" -C "$APP_DIR" .
fi

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p "$APP_DIR"
sudo chown $USER:$USER "$APP_DIR"

# Copy application files
echo "📋 Copying application files..."
cp -r . "$APP_DIR/"
cd "$APP_DIR"

# Install Python and dependencies
echo "🐍 Setting up Python environment..."
python$PYTHON_VERSION -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Database setup
echo "🗄️ Setting up database..."
mysql -u root -p <<EOF
CREATE DATABASE IF NOT EXISTS bigdatahackaton;
USE bigdatahackaton;
SOURCE database_backup/database_schema.sql;
EOF

# Create configuration
echo "⚙️ Creating configuration..."
cat > .env <<EOF
FLASK_ENV=production
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=bigdatahackaton
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
RATE_LIMIT_PER_MINUTE=60
SESSION_TIMEOUT=3600
EOF

# Set permissions
echo "🔒 Setting permissions..."
sudo chown -R app:app "$APP_DIR"
chmod 600 .env

# Install systemd service
echo "🔧 Installing systemd service..."
sudo cp deploy/rwanda-trade-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rwanda-trade-dashboard
sudo systemctl start rwanda-trade-dashboard

# Install nginx configuration
echo "🌐 Configuring nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/rwanda-trade-dashboard
sudo ln -sf /etc/nginx/sites-available/rwanda-trade-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# SSL Certificate (using Let's Encrypt)
echo "🔐 Setting up SSL certificate..."
sudo certbot --nginx -d your-domain.com

echo "✅ Deployment completed successfully!"
echo "🌐 Application is running at: https://your-domain.com"
echo "📊 Monitor with: sudo systemctl status rwanda-trade-dashboard"
echo "📝 View logs with: sudo journalctl -u rwanda-trade-dashboard -f"
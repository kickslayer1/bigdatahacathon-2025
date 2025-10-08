"""
Deployment Configuration and Documentation
"""

import os
from pathlib import Path

# Docker configuration
DOCKERFILE_CONTENT = """
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    default-libmysqlclient-dev \\
    pkg-config \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \\
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
"""

DOCKER_COMPOSE_CONTENT = """
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_HOST=db
      - DATABASE_PORT=3306
      - DATABASE_NAME=bigdatahackaton
      - DATABASE_USER=root
      - DATABASE_PASSWORD=your_password
    depends_on:
      - db
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=your_password
      - MYSQL_DATABASE=bigdatahackaton
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database_backup:/docker-entrypoint-initdb.d
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  mysql_data:
"""

NGINX_CONFIG = """
events {
    worker_connections 1024;
}

http {
    upstream app {
        server web:5000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

        # Gzip compression
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # API rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Login rate limiting
        location /login {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Main application
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
"""

SYSTEMD_SERVICE = """
[Unit]
Description=Rwanda Trade Dashboard
After=network.target

[Service]
Type=notify
User=app
Group=app
WorkingDirectory=/opt/rwanda-trade-dashboard
Environment=PATH=/opt/rwanda-trade-dashboard/venv/bin
ExecStart=/opt/rwanda-trade-dashboard/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""

DEPLOYMENT_SCRIPT = """#!/bin/bash

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
"""

def create_deployment_files():
    """Create all deployment-related files"""
    
    deployment_files = {
        'Dockerfile': DOCKERFILE_CONTENT,
        'docker-compose.yml': DOCKER_COMPOSE_CONTENT,
        'nginx.conf': NGINX_CONFIG,
        'deploy/rwanda-trade-dashboard.service': SYSTEMD_SERVICE,
        'deploy/deploy.sh': DEPLOYMENT_SCRIPT
    }
    
    for file_path, content in deployment_files.items():
        # Create directory if needed
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        
        # Make deploy script executable
        if file_path.endswith('.sh'):
            os.chmod(file_path, 0o755)
    
    return deployment_files.keys()

if __name__ == "__main__":
    created_files = create_deployment_files()
    print("Created deployment files:")
    for file in created_files:
        print(f"  ✓ {file}")
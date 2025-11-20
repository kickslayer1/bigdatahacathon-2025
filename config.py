# Configuration Management System
import os
from typing import Dict, Any

class Config:
    """Centralized configuration management"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'kickslayer')
    DB_NAME = os.getenv('DB_NAME', 'bigdatahackaton')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # ML Configuration
    PROPHET_TIMEOUT = int(os.getenv('PROPHET_TIMEOUT', 30))
    ML_CACHE_ENABLED = os.getenv('ML_CACHE_ENABLED', 'True').lower() == 'true'
    
    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # Security
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 3600))  # 1 hour
    
    @classmethod
    def get_db_config(cls) -> Dict[str, Any]:
        """Get database configuration as dictionary"""
        return {
            'host': cls.DB_HOST,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD,
            'database': cls.DB_NAME,
            'port': cls.DB_PORT
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration settings"""
        required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"Missing required configuration: {var}")
        return True

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    # Use environment variables for sensitive data
    DB_PASSWORD = os.getenv('DB_PASSWORD')  # Must be set in production
    SECRET_KEY = os.getenv('SECRET_KEY')    # Must be set in production

class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DB_NAME = 'test_bigdatahackaton'

# Configuration factory
def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
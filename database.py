"""
Enhanced Database Layer with Connection Pooling and Error Handling
"""

import mysql.connector
from mysql.connector import pooling
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager
import logging
from typing import Optional, Dict, Any, List, Tuple
from config import get_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Enhanced database manager with connection pooling"""
    
    def __init__(self):
        self.config = get_config()
        self._pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize database connection pool"""
        try:
            pool_config = self.config.get_db_config()
            pool_config.update({
                'pool_name': 'rwanda_trade_pool',
                'pool_size': 10,
                'pool_reset_session': True,
                'autocommit': True
            })
            
            self._pool = pooling.MySQLConnectionPool(**pool_config)
            logger.info("Database connection pool initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = self._pool.get_connection()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()
    
    def execute_query(self, query: str, params: Optional[Tuple] = None, fetch: str = 'all') -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                
                if fetch == 'one':
                    return cursor.fetchone()
                elif fetch == 'many':
                    return cursor.fetchmany()
                else:
                    return cursor.fetchall()
                    
            finally:
                cursor.close()
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> int:
        """Execute an INSERT/UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.rowcount
            finally:
                cursor.close()
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information"""
        query = "DESCRIBE %s" % table_name  # Note: table name should be validated
        return self.execute_query(query)
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table exists"""
        query = """
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        result = self.execute_query(query, (self.config.DB_NAME, table_name), fetch='one')
        return result['count'] > 0

# Global database manager instance
db_manager = DatabaseManager()

# Authentication functions
def register_user(username: str, password: str) -> Tuple[bool, Optional[str]]:
    """Register a new user with enhanced validation"""
    try:
        # Check if username already exists
        existing_user = db_manager.execute_query(
            "SELECT id FROM users WHERE username = %s", 
            (username,), 
            fetch='one'
        )
        
        if existing_user:
            return False, "Username already exists."
        
        # Hash password and insert user
        hashed_password = generate_password_hash(password)
        affected_rows = db_manager.execute_update(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        
        if affected_rows > 0:
            logger.info(f"User {username} registered successfully")
            return True, None
        else:
            return False, "Failed to create user."
            
    except Exception as e:
        logger.error(f"Registration error for {username}: {e}")
        return False, "Registration failed due to system error."

def check_user(username: str, password: str) -> bool:
    """Authenticate user with enhanced security"""
    try:
        user = db_manager.execute_query(
            "SELECT password FROM users WHERE username = %s",
            (username,),
            fetch='one'
        )
        
        if user and check_password_hash(user['password'], password):
            logger.info(f"User {username} authenticated successfully")
            return True
        else:
            logger.warning(f"Failed authentication attempt for {username}")
            return False
            
    except Exception as e:
        logger.error(f"Authentication error for {username}: {e}")
        return False

# Legacy functions for backward compatibility
def get_db_connection():
    """Legacy function - use db_manager.get_connection() instead"""
    return db_manager._pool.get_connection()

# Data access functions
class CommodityDataAccess:
    """Data access layer for commodity data"""
    
    @staticmethod
    def get_export_commodities() -> List[str]:
        """Get list of export commodities"""
        try:
            if not db_manager.table_exists('export_commodities'):
                return ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
            
            results = db_manager.execute_query(
                "SELECT DISTINCT period FROM export_commodities WHERE period IS NOT NULL AND period != ''"
            )
            return [row['period'] for row in results]
            
        except Exception as e:
            logger.error(f"Error fetching export commodities: {e}")
            return ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
    
    @staticmethod
    def get_import_commodities() -> List[str]:
        """Get list of import commodities"""
        try:
            if not db_manager.table_exists('imports_commodities'):
                return ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
            
            results = db_manager.execute_query(
                "SELECT DISTINCT period FROM imports_commodities WHERE period IS NOT NULL AND period != ''"
            )
            return [row['period'] for row in results]
            
        except Exception as e:
            logger.error(f"Error fetching import commodities: {e}")
            return ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
    
    @staticmethod
    def get_commodity_timeline(table_name: str, commodity: str) -> Optional[Dict[str, Any]]:
        """Get commodity timeline data"""
        try:
            if not db_manager.table_exists(table_name):
                return None
            
            # Get the commodity data
            result = db_manager.execute_query(
                f"SELECT * FROM {table_name} WHERE period = %s",
                (commodity,),
                fetch='one'
            )
            
            if result:
                # Get column information
                schema = db_manager.get_table_schema(table_name)
                quarter_columns = [col['Field'] for col in schema if col['Field'] != 'period']
                
                return {
                    'data': result,
                    'quarters': quarter_columns
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching commodity timeline for {commodity}: {e}")
            return None
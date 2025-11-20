"""
Enhanced database configuration for Heroku deployment
"""
from werkzeug.security import generate_password_hash, check_password_hash
import os
import mysql.connector
from urllib.parse import urlparse

def get_db_connection():
    """Get database connection - works locally and on Heroku"""
    
    # Check for Heroku database URL (ClearDB or JawsDB)
    database_url = os.environ.get('CLEARDB_DATABASE_URL') or os.environ.get('JAWSDB_URL')
    
    if database_url:
        # Parse Heroku database URL
        url = urlparse(database_url)
        return mysql.connector.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],  # Remove leading slash
            port=url.port or 3306
        )
    else:
        # Local development configuration
        return mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', 'localhost'),
            user=os.environ.get('DATABASE_USER', 'root'),
            password=os.environ.get('DATABASE_PASSWORD', 'kickslayer'),
            database=os.environ.get('DATABASE_NAME', 'bigdatahackaton'),
            port=int(os.environ.get('DATABASE_PORT', 3306))
        )

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "Username already exists."
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()
    return True, None

def check_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and check_password_hash(result[0], password):
        return True
    return False
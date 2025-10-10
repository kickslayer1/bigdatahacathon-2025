from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from urllib.parse import urlparse

def get_db_connection():
    # Check for cloud database URL (Heroku ClearDB, PlanetScale, etc.)
    database_url = os.environ.get('CLEARDB_DATABASE_URL') or os.environ.get('DATABASE_URL')
    
    if database_url:
        # Parse cloud database URL
        url = urlparse(database_url)
        return mysql.connector.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],  # Remove leading slash
            port=url.port or 3306
        )
    else:
        # Local development fallback
        return mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', 'localhost'),
            user=os.environ.get('DATABASE_USER', 'root'),         
            password=os.environ.get('DATABASE_PASSWORD', 'kickslayer'),
            database=os.environ.get('DATABASE_NAME', 'bigdatahackaton')
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
# filepath: c:\Users\USER\Documents\bigdatahacathon-2025\htmlss\db.py
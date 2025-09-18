from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',              # <-- your MySQL username
        password='kickslayer', # <-- your MySQL password
        database='bigdatahackaton'
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
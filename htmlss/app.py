from flask import Flask, jsonify, request, send_from_directory, session
import os
from db import register_user, check_user, get_db_connection

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

# Serve the HTML page
@app.route('/')
def serve_gateway():
    return send_from_directory('.', 'gateway.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if check_user(username, password):
        session['username'] = username  # Store username in session
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    success, message = register_user(username, password)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': message})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'success': True})

@app.route('/check_session')
def check_session():
    if 'username' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    else:
        return jsonify({'logged_in': False})

# Endpoint to serve options for form (from 'dataset' table)
@app.route('/options')
def get_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT item FROM datasetx")  # updated table name
    items = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT time FROM datasetx")  # updated table name
    times = sorted([int(row[0]) for row in cursor.fetchall()])
    cursor.execute("SELECT DISTINCT amount FROM datasetx")  # updated table name
    amounts = sorted([int(row[0]) for row in cursor.fetchall()])
    cursor.close()
    conn.close()
    return jsonify({'items': items, 'times': times, 'amounts': amounts})

@app.route('/predict_amount', methods=['POST'])
def predict_amount():
    data = request.json
    item = data.get('item')
    year = int(data.get('year'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM datasetx WHERE item=%s AND time=%s", (item, year))  # updated table name
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        amount = int(result[0])
        return jsonify({'amount': amount})
    else:
        return jsonify({'amount': None, 'error': 'No data found for the selected item and year.'})
# Example: Endpoint to get data from 'datamap' table
@app.route('/datamap_options')
def datamap_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT item FROM datamap")
    items = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT time FROM datamap")
    times = sorted([int(row[0]) for row in cursor.fetchall()])
    cursor.execute("SELECT DISTINCT amount FROM datamap")
    amounts = sorted([int(row[0]) for row in cursor.fetchall()])
    cursor.close()
    conn.close()
    return jsonify({'items': items, 'times': times, 'amounts': amounts})

# Endpoint to get export commodities data
@app.route('/export_commodities_data')
def export_commodities_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM export_commodities")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    # Return as list of dicts
    return jsonify([dict(zip(columns, row)) for row in data])

# Endpoint to get trade data
@app.route('/trade20_25q2_data')
def trade20_25q2_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trade20_25q2")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in data])

# Endpoint to get exports data
@app.route('/exports_data')
def exports_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT period, exports, imports, `re-imports` FROM exportss")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in data])

@app.route('/exports_share_data')
def exports_share_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT country, share, value, change1, change2 FROM exports_share")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in data])

@app.route('/imports_share_data')
def imports_share_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT country, share, value, change1, change2 FROM imports_share")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in data])

# Serve static files (like JS)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/styles.css')
def serve_css():
    return send_from_directory('..', 'styles.css')

if __name__ == '__main__':
    app.run(debug=True)
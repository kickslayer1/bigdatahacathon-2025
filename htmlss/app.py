from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# In-memory user store for demonstration
users = {}

# Serve the HTML page
@app.route('/')
def serve_gateway():
    return send_from_directory('.', 'gateway.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username] == password:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists.'})
    users[username] = password
    return jsonify({'success': True})

# Endpoint to serve options for form
@app.route('/options')
def get_options():
    df = pd.read_csv('datasetx.csv')
    items = sorted(df['item'].unique())
    # Convert times and amounts to Python int
    times = sorted([int(t) for t in df['time'].unique()])
    amounts = sorted([int(a) for a in df['amount'].unique()])
    return jsonify({'items': items, 'times': times, 'amounts': amounts})

# Endpoint to get predicted amount for selected item and year
@app.route('/predict_amount', methods=['POST'])
def predict_amount():
    data = request.json
    item = data.get('item')
    year = int(data.get('year'))
    df = pd.read_csv('datasetx.csv')
    result = df[(df['item'] == item) & (df['time'] == year)]
    if not result.empty:
        amount = int(result.iloc[0]['amount'])
        return jsonify({'amount': amount})
    else:
        return jsonify({'amount': None, 'error': 'No data found for the selected item and year.'})

# Serve static files (like JS)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/styles.css')
def serve_css():
    return send_from_directory('..', 'styles.css')

if __name__ == '__main__':
    app.run(debug=True)
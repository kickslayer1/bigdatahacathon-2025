from flask import Flask, jsonify, request, send_from_directory, session, redirect, url_for
import os
import numpy as np
from db import register_user, check_user, get_db_connection
from ml_predictions import generate_ml_predictions

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/gateway.html')
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Serve the HTML page
@app.route('/')
def serve_gateway():
    return send_from_directory('.', 'gateway.html')

# Protected routes - redirect to gateway if not logged in
@app.route('/front_page.html')
def serve_front_page():
    if 'username' not in session:
        return redirect('/gateway.html')
    return send_from_directory('.', 'front_page.html')

@app.route('/global_trade_2025.html')
def serve_global_trade():
    if 'username' not in session:
        return redirect('/gateway.html')
    return send_from_directory('.', 'global_trade_2025.html')

@app.route('/demand_prediction_2026.html')
def serve_demand_prediction():
    if 'username' not in session:
        return redirect('/gateway.html')
    return send_from_directory('.', 'demand_prediction_2026.html')

@app.route('/policy_recommendation.html')
def serve_policy_recommendation():
    if 'username' not in session:
        return redirect('/gateway.html')
    return send_from_directory('.', 'policy_recommendation.html')

@app.route('/youth_sme_engagement.html')
def serve_youth_sme():
    if 'username' not in session:
        return redirect('/gateway.html')
    return send_from_directory('.', 'youth_sme_engagement.html')

@app.route('/referencing.html')
def serve_referencing():
    if 'username' not in session:
        return redirect('/gateway.html')
    return send_from_directory('.', 'referencing.html')

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

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.clear()  # Clear all session data
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/check_session')
def check_session():
    if 'username' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    else:
        return jsonify({'logged_in': False})

# Endpoint to serve options for form (from 'dataset' table) - PROTECTED
@app.route('/options')
def get_options():
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
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
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
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
# Example: Endpoint to get data from 'datamap' table - PROTECTED
@app.route('/datamap_options')
def datamap_options():
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
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

# Endpoint to get export commodities data - PROTECTED
@app.route('/export_commodities_data')
def export_commodities_data():
    if 'username' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM export_commodities")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    # Return as list of dicts
    return jsonify([dict(zip(columns, row)) for row in data])

# Endpoint to get distinct commodities for dropdown
@app.route('/commodity_options')
def commodity_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT period FROM export_commodities WHERE period IS NOT NULL AND period != ''")
        commodities = [row[0] for row in cursor.fetchall()]
        if not commodities:  # If no data found, provide default commodities
            commodities = ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
    except Exception as e:
        print(f"Database error: {e}")
        commodities = ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
    cursor.close()
    conn.close()
    return jsonify({'commodities': commodities})

# Endpoint to get distinct import commodities for dropdown
@app.route('/import_commodity_options')
def import_commodity_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT period FROM imports_commodities WHERE period IS NOT NULL AND period != ''")
        commodities = [row[0] for row in cursor.fetchall()]
        if not commodities:  # If no data found, provide default commodities
            commodities = ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
    except Exception as e:
        print(f"Database error: {e}")
        commodities = ['Gold', 'Coffee', 'Tea', 'Minerals', 'Health Suppliers', 'Tech Suppliers']
    cursor.close()
    conn.close()
    return jsonify({'commodities': commodities})

# Endpoint to get commodity timeline data with ML predictions
@app.route('/commodity_timeline/<commodity>')
def commodity_timeline(commodity):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Try to get actual data from database
    timeline_data = []
    try:
        cursor.execute("SELECT * FROM export_commodities WHERE period = %s", (commodity,))
        data = cursor.fetchone()
        
        if data:
            print(f"Found export data for {commodity}: {data[:5]}...")  # Show first few values
            
            # Get column names (quarters)
            cursor.execute("SHOW COLUMNS FROM export_commodities")
            columns = cursor.fetchall()
            quarter_columns = [col[0] for col in columns if col[0] != 'period']
            
            # Extract actual data for each quarter
            for i, quarter in enumerate(quarter_columns):
                if i + 1 < len(data):  # Skip the first column (period name)
                    value = data[i + 1]  # Get the value for this quarter
                    if value is not None:
                        # Convert to dollars (data is in millions)
                        value_in_dollars = int(float(value) * 1000000)
                        timeline_data.append({
                            'quarter': quarter,
                            'value': value_in_dollars,
                            'is_actual': True
                        })
            
            print(f"Extracted {len(timeline_data)} quarters of real data for {commodity}")
            
        else:
            print(f"No data found for commodity: {commodity}")
            # Return empty if no data found
            cursor.close()
            conn.close()
            return jsonify({'error': f'No data found for commodity: {commodity}'})
            
    except Exception as e:
        print(f"Database error for commodity {commodity}: {e}")
        cursor.close()
        conn.close()
        return jsonify({'error': f'Database error: {str(e)}'})
    
    # Generate ML predictions for 2025Q3 and 2025Q4 using real data
    try:
        ml_results = generate_ml_predictions(timeline_data, commodity)
        ml_predictions = ml_results['predictions']
        model_performance = ml_results['model_performance']
        models_used = ml_results['models_used']
        
        # Add ML predictions to timeline
        for pred in ml_predictions:
            timeline_data.append({
                'quarter': pred['quarter'],
                'value': pred['predicted_value'],
                'is_actual': False,
                'is_prediction': True,
                'confidence_level': pred['confidence_level'],
                'upper_bound': pred['upper_bound'],
                'lower_bound': pred['lower_bound'],
                'prophet_prediction': pred['prophet_prediction'],
                'linear_prediction': pred['linear_prediction']
            })
        
        prediction_info = {
            'model_performance': model_performance,
            'models_used': models_used,
            'ml_enabled': True,
            'data_source': 'Real database values'
        }
        
    except Exception as e:
        print(f"ML prediction error: {e}")
        # Fallback to simple predictions based on real data trend
        if len(timeline_data) >= 2:
            last_value = timeline_data[-1]['value']
            prev_value = timeline_data[-2]['value']
            growth_rate = (last_value - prev_value) / prev_value if prev_value > 0 else 0.05
            
            timeline_data.append({
                'quarter': '2025Q3',
                'value': int(last_value * (1 + growth_rate)),
                'is_actual': False,
                'is_prediction': True,
                'confidence_level': 'Medium',
                'fallback': True
            })
            
            timeline_data.append({
                'quarter': '2025Q4',
                'value': int(last_value * (1 + growth_rate * 1.5)),
                'is_actual': False,
                'is_prediction': True,
                'confidence_level': 'Medium',
                'fallback': True
            })
        
        prediction_info = {
            'ml_enabled': False,
            'fallback_used': True,
            'data_source': 'Real database values',
            'error': str(e)
        }
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'commodity': commodity,
        'timeline': timeline_data,
        'prediction_info': prediction_info
    })

# Endpoint to get import commodity timeline data with ML predictions
@app.route('/import_commodity_timeline/<commodity>')
def import_commodity_timeline(commodity):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Try to get actual data from database
    timeline_data = []
    try:
        cursor.execute("SELECT * FROM imports_commodities WHERE period = %s", (commodity,))
        data = cursor.fetchone()
        
        if data:
            print(f"Found import data for {commodity}: {data[:5]}...")  # Show first few values
            
            # Get column names (quarters)
            cursor.execute("SHOW COLUMNS FROM imports_commodities")
            columns = cursor.fetchall()
            quarter_columns = [col[0] for col in columns if col[0] != 'period']
            
            # Extract actual data for each quarter
            for i, quarter in enumerate(quarter_columns):
                if i + 1 < len(data):  # Skip the first column (period name)
                    value = data[i + 1]  # Get the value for this quarter
                    if value is not None:
                        # Convert to dollars (data is in millions)
                        value_in_dollars = int(float(value) * 1000000)
                        timeline_data.append({
                            'quarter': quarter,
                            'value': value_in_dollars,
                            'is_actual': True
                        })
            
            print(f"Extracted {len(timeline_data)} quarters of real import data for {commodity}")
            
        else:
            print(f"No import data found for commodity: {commodity}")
            # Return empty if no data found
            cursor.close()
            conn.close()
            return jsonify({'error': f'No import data found for commodity: {commodity}'})
            
    except Exception as e:
        print(f"Database error for import commodity {commodity}: {e}")
        cursor.close()
        conn.close()
        return jsonify({'error': f'Database error: {str(e)}'})
    
    # Generate ML predictions for 2025Q3 and 2025Q4 using real data
    try:
        ml_results = generate_ml_predictions(timeline_data, commodity)
        ml_predictions = ml_results['predictions']
        model_performance = ml_results['model_performance']
        models_used = ml_results['models_used']
        
        # Add ML predictions to timeline
        for pred in ml_predictions:
            timeline_data.append({
                'quarter': pred['quarter'],
                'value': pred['predicted_value'],
                'is_actual': False,
                'is_prediction': True,
                'confidence_level': pred['confidence_level'],
                'upper_bound': pred['upper_bound'],
                'lower_bound': pred['lower_bound'],
                'prophet_prediction': pred['prophet_prediction'],
                'linear_prediction': pred['linear_prediction']
            })
        
        prediction_info = {
            'model_performance': model_performance,
            'models_used': models_used,
            'ml_enabled': True,
            'data_source': 'Real database values'
        }
        
    except Exception as e:
        print(f"ML prediction error for imports: {e}")
        # Fallback to simple predictions based on real data trend
        if len(timeline_data) >= 2:
            last_value = timeline_data[-1]['value']
            prev_value = timeline_data[-2]['value']
            growth_rate = (last_value - prev_value) / prev_value if prev_value > 0 else 0.05
            
            timeline_data.append({
                'quarter': '2025Q3',
                'value': int(last_value * (1 + growth_rate)),
                'is_actual': False,
                'is_prediction': True,
                'confidence_level': 'Medium',
                'fallback': True
            })
            
            timeline_data.append({
                'quarter': '2025Q4',
                'value': int(last_value * (1 + growth_rate * 1.2)),
                'is_actual': False,
                'is_prediction': True,
                'confidence_level': 'Medium',
                'fallback': True
            })
        
        prediction_info = {
            'ml_enabled': False,
            'fallback_used': True,
            'data_source': 'Real database values',
            'error': str(e)
        }
    
    cursor.close()
    conn.close()
    
    return jsonify({
        'commodity': commodity,
        'timeline': timeline_data,
        'prediction_info': prediction_info
    })

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
    cursor.execute("SELECT country, share, value FROM exports_share")
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

# Serve static files (like JS) - but protect HTML files
@app.route('/<path:filename>')
def serve_static(filename):
    # Protect HTML files (except gateway, login, register)
    if filename.endswith('.html') and filename not in ['gateway.html', 'login.html', 'register.html']:
        if 'username' not in session:
            return redirect('/gateway.html')
    return send_from_directory('.', filename)

@app.route('/styles.css')
def serve_css():
    return send_from_directory('..', 'styles.css')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
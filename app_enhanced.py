"""
Enhanced Flask Application with Blueprints and Error Handling
"""

from flask import Flask, jsonify, request, send_from_directory, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging
from datetime import timedelta
import numpy as np

# Import our enhanced modules
from config import get_config
from database import db_manager, register_user, check_user, CommodityDataAccess
from ml_predictions import generate_ml_predictions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Configure session
    app.permanent_session_lifetime = timedelta(seconds=config.SESSION_TIMEOUT)
    
    # Initialize rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=[f"{config.RATE_LIMIT_PER_MINUTE} per minute"]
    )
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        try:
            # Test database connection
            with db_manager.get_connection() as conn:
                pass
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': pd.Timestamp.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }), 503
    
    # Authentication routes
    @app.route('/')
    def serve_gateway():
        return send_from_directory('.', 'gateway.html')
    
    @app.route('/login', methods=['POST'])
    @limiter.limit("5 per minute")  # Prevent brute force attacks
    def login():
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Username and password required'}), 400
            
            if check_user(username, password):
                session.permanent = True
                session['username'] = username
                logger.info(f"User {username} logged in successfully")
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return jsonify({'success': False, 'message': 'Login failed'}), 500
    
    @app.route('/register', methods=['POST'])
    @limiter.limit("3 per minute")  # Prevent spam registrations
    def register():
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Username and password required'}), 400
            
            if len(password) < 6:
                return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
            
            success, message = register_user(username, password)
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': message}), 400
                
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return jsonify({'success': False, 'message': 'Registration failed'}), 500
    
    @app.route('/logout')
    def logout():
        username = session.get('username')
        session.pop('username', None)
        if username:
            logger.info(f"User {username} logged out")
        return jsonify({'success': True})
    
    @app.route('/check_session')
    def check_session():
        if 'username' in session:
            return jsonify({'logged_in': True, 'username': session['username']})
        else:
            return jsonify({'logged_in': False})
    
    # Data endpoints
    @app.route('/options')
    def get_options():
        """Get options for prediction form"""
        try:
            data = db_manager.execute_query("SELECT DISTINCT item FROM datasetx")
            items = [row['item'] for row in data]
            
            data = db_manager.execute_query("SELECT DISTINCT time FROM datasetx")
            times = sorted([int(row['time']) for row in data])
            
            data = db_manager.execute_query("SELECT DISTINCT amount FROM datasetx")
            amounts = sorted([int(row['amount']) for row in data])
            
            return jsonify({'items': items, 'times': times, 'amounts': amounts})
            
        except Exception as e:
            logger.error(f"Error fetching options: {e}")
            return jsonify({'error': 'Failed to fetch options'}), 500
    
    @app.route('/predict_amount', methods=['POST'])
    def predict_amount():
        """Predict amount for given item and year"""
        try:
            data = request.json
            item = data.get('item')
            year = int(data.get('year'))
            
            result = db_manager.execute_query(
                "SELECT amount FROM datasetx WHERE item = %s AND time = %s",
                (item, year),
                fetch='one'
            )
            
            if result:
                return jsonify({'amount': int(result['amount'])})
            else:
                return jsonify({'amount': None, 'error': 'No data found for the selected item and year'})
                
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return jsonify({'error': 'Prediction failed'}), 500
    
    # Commodity endpoints
    @app.route('/commodity_options')
    def commodity_options():
        """Get available export commodities"""
        try:
            commodities = CommodityDataAccess.get_export_commodities()
            return jsonify({'commodities': commodities})
        except Exception as e:
            logger.error(f"Error fetching commodity options: {e}")
            return jsonify({'error': 'Failed to fetch commodities'}), 500
    
    @app.route('/import_commodity_options')
    def import_commodity_options():
        """Get available import commodities"""
        try:
            commodities = CommodityDataAccess.get_import_commodities()
            return jsonify({'commodities': commodities})
        except Exception as e:
            logger.error(f"Error fetching import commodity options: {e}")
            return jsonify({'error': 'Failed to fetch import commodities'}), 500
    
    @app.route('/commodity_timeline/<commodity>')
    def commodity_timeline(commodity):
        """Get export commodity timeline with ML predictions"""
        return _get_commodity_timeline('export_commodities', commodity, 'export')
    
    @app.route('/import_commodity_timeline/<commodity>')
    def import_commodity_timeline(commodity):
        """Get import commodity timeline with ML predictions"""
        return _get_commodity_timeline('imports_commodities', commodity, 'import')
    
    def _get_commodity_timeline(table_name: str, commodity: str, data_type: str):
        """Helper function for commodity timeline data"""
        try:
            # Get commodity data
            commodity_info = CommodityDataAccess.get_commodity_timeline(table_name, commodity)
            
            if not commodity_info:
                return jsonify({'error': f'No {data_type} data found for commodity: {commodity}'}), 404
            
            data = commodity_info['data']
            quarter_columns = commodity_info['quarters']
            
            # Extract timeline data
            timeline_data = []
            for quarter in quarter_columns:
                value = data.get(quarter)
                if value is not None:
                    # Convert to dollars (data is in millions)
                    value_in_dollars = int(float(value) * 1000000)
                    timeline_data.append({
                        'quarter': quarter,
                        'value': value_in_dollars,
                        'is_actual': True
                    })
            
            logger.info(f"Extracted {len(timeline_data)} quarters of real {data_type} data for {commodity}")
            
            # Generate ML predictions
            try:
                ml_results = generate_ml_predictions(timeline_data, commodity)
                
                # Add ML predictions to timeline
                for pred in ml_results['predictions']:
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
                    'model_performance': ml_results['model_performance'],
                    'models_used': ml_results['models_used'],
                    'ml_enabled': True,
                    'data_source': 'Real database values'
                }
                
            except Exception as e:
                logger.warning(f"ML prediction failed for {commodity}: {e}")
                
                # Fallback to simple predictions
                if len(timeline_data) >= 2:
                    last_value = timeline_data[-1]['value']
                    prev_value = timeline_data[-2]['value']
                    growth_rate = (last_value - prev_value) / prev_value if prev_value > 0 else 0.05
                    
                    timeline_data.extend([
                        {
                            'quarter': '2025Q3',
                            'value': int(last_value * (1 + growth_rate)),
                            'is_actual': False,
                            'is_prediction': True,
                            'confidence_level': 'Medium',
                            'fallback': True
                        },
                        {
                            'quarter': '2025Q4',
                            'value': int(last_value * (1 + growth_rate * 1.2)),
                            'is_actual': False,
                            'is_prediction': True,
                            'confidence_level': 'Medium',
                            'fallback': True
                        }
                    ])
                
                prediction_info = {
                    'ml_enabled': False,
                    'fallback_used': True,
                    'data_source': 'Real database values',
                    'error': str(e)
                }
            
            return jsonify({
                'commodity': commodity,
                'timeline': timeline_data,
                'prediction_info': prediction_info
            })
            
        except Exception as e:
            logger.error(f"Error in commodity timeline for {commodity}: {e}")
            return jsonify({'error': f'Failed to fetch {data_type} data'}), 500
    
    # Additional data endpoints
    @app.route('/exports_data')
    def exports_data():
        """Get exports data for charts"""
        try:
            data = db_manager.execute_query(
                "SELECT period, exports, imports, `re-imports` FROM exportss"
            )
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error fetching exports data: {e}")
            return jsonify({'error': 'Failed to fetch exports data'}), 500
    
    @app.route('/exports_share_data')
    def exports_share_data():
        """Get exports share data"""
        try:
            data = db_manager.execute_query(
                "SELECT country, share, value, change1, change2 FROM exports_share"
            )
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error fetching exports share data: {e}")
            return jsonify({'error': 'Failed to fetch exports share data'}), 500
    
    @app.route('/imports_share_data')
    def imports_share_data():
        """Get imports share data"""
        try:
            data = db_manager.execute_query(
                "SELECT country, share, value, change1, change2 FROM imports_share"
            )
            return jsonify(data)
        except Exception as e:
            logger.error(f"Error fetching imports share data: {e}")
            return jsonify({'error': 'Failed to fetch imports share data'}), 500
    
    # Static file serving
    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory('.', filename)
    
    @app.route('/styles.css')
    def serve_css():
        return send_from_directory('..', 'styles.css')
    
    return app

# Application factory
app = create_app()

if __name__ == '__main__':
    config = get_config()
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
# app.py - Final optimized version without duplicates
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
import sys
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# Import blueprints
from routes.market import market_bp
from routes.analysis import analysis_bp
from routes.user import user_bp

# Import configuration
from config import config

def create_app(config_name=None):
    """Application factory pattern for creating Flask app"""
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Determine configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    app.config.from_object(config[config_name])
    
    # Enhanced CORS configuration
    CORS(app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000", 
                 "http://localhost:5000", "http://127.0.0.1:5000",
                 "http://localhost:8080", "http://127.0.0.1:8080",
                 "http://localhost:58916", "http://127.0.0.1:58916"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "Accept"],
         supports_credentials=True)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register before/after request handlers
    register_request_handlers(app)
    
    return app

def setup_logging(app):
    """Setup application logging"""
    if not app.debug:
        # Production logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/agromoney.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Agromoney API startup')
    else:
        # Development logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

def register_blueprints(app):
    """Register all blueprints with the app"""
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis') 
    app.register_blueprint(user_bp, url_prefix='/api/user')

def register_error_handlers(app):
    """Register custom error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'message': 'The requested URL was not found on the server',
            'path': request.path
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An internal server error occurred'
        }), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 'Method not allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405

def register_request_handlers(app):
    """Register before/after request handlers"""
    
    @app.before_request
    def before_request():
        """Execute before each request"""
        app.logger.debug(f"Request: {request.method} {request.path}")
        
        # Handle preflight OPTIONS requests
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'preflight'})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response
    
    @app.after_request
    def after_request(response):
        """Execute after each request"""
        origin = request.headers.get('Origin', '*')
        
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept,Origin,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '86400')
        
        app.logger.debug(f"Response: {response.status_code} for {request.method} {request.path}")
        
        return response

# Create app instance
app = create_app()

@app.route('/')
def home():
    """Root endpoint with API information"""
    return jsonify({
        'success': True,
        'message': '🌱 Agromoney API - Madhya Pradesh Agriculture Market Analytics',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'features': {
            '10_year_analysis': True,
            'candle_stick_charts': True,
            'advanced_analytics': True,
            'marketplace': True,
            'price_alerts': True,
            'user_management': True
        },
        'endpoints': {
            'market_data': {
                'rates': '/api/market/rates?crop=Wheat&district=Indore',
                'historical': '/api/market/historical?crop=Wheat&years=10',
                'candle_data': '/api/market/candle-data?crop=Tomato&years=5&interval_days=7',
                'flexible_data': '/api/market/flexible-data?crop=Onion&years=0.5&interval_days=3',
                'crops_list': '/api/market/crops',
                'districts_list': '/api/market/districts'
            },
            'analysis': {
                'trends': '/api/analysis/trends?crop=Wheat&district=Indore',
                'weather_analysis': '/api/analysis/weather-analysis?crop=Wheat',
                'market_prediction': '/api/analysis/market-prediction?crop=Tomato',
                'crop_insights': '/api/analysis/crop-insights?crop=Wheat',
                'crop_recommendation': '/api/analysis/crop-recommendation?district=Indore&soil_type=loamy',
                'candle_data': '/api/analysis/candle-data?crop=Soybean&years=10&interval_days=30'
            },
            'user_management': {
                'register': '/api/user/register',
                'profile': '/api/user/profile/1',
                'create_listing': '/api/user/listings',
                'get_listings': '/api/user/listings?crop=Wheat',
                'create_alert': '/api/user/alerts',
                'get_alerts': '/api/user/alerts?user_id=1',
                'notifications': '/api/user/notifications?user_id=1',
                'buying_requests': '/api/user/buying-requests'
            }
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Agromoney API v2.0',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'features': {
            'market_data': 'active',
            'analysis': 'active', 
            'user_management': 'active',
            'candle_stick': 'active',
            '10_year_analytics': 'active',
            'marketplace': 'active'
        }
    })

@app.route('/api/docs')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        'success': True,
        'documentation': {
            'description': 'Agromoney API v2.0 - Advanced agriculture market analytics with 10-year data support',
            'base_url': 'http://localhost:5000/api',
            'data_analysis_periods': {
                'default': '10 years',
                'supported': ['1 year', '5 years', '10 years'],
                'recommended': '10 years for best accuracy'
            }
        }
    })

@app.route('/api/stats')
def api_stats():
    """API statistics endpoint"""
    return jsonify({
        'success': True,
        'statistics': {
            'crops': {
                'total': len(app.config['CROPS']),
                'categories': app.config['CROP_CATEGORIES'],
                'most_popular': ['Wheat', 'Soybean', 'Gram', 'Tomato', 'Onion']
            },
            'districts': {
                'total': len(app.config['MP_DISTRICTS']),
                'regions': app.config['MP_REGIONS'],
                'most_active': ['Indore', 'Bhopal', 'Ujjain', 'Gwalior', 'Jabalpur']
            }
        }
    })

@app.route('/api/features')
def features():
    """Features endpoint"""
    return jsonify({
        'success': True,
        'version': '2.0.0',
        'major_enhancements': {
            'data_analysis': {
                '10_year_support': 'Complete historical data for 10 years',
                'advanced_candlestick': 'OHLC data with multiple intervals',
                'extended_predictions': '2-5 year market forecasts'
            },
            'user_experience': {
                'reliability_scoring': 'User trust and transaction scoring',
                'enhanced_alerts': 'Smart price alerts with market context',
                'marketplace': 'Complete buying/selling platform'
            }
        }
    })

@app.route('/api/quick-start')
def quick_start():
    """Quick start guide for developers"""
    return jsonify({
        'success': True,
        'quick_start': {
            '1_getting_started': {
                'check_health': 'GET /api/health',
                'view_docs': 'GET /api/docs',
                'see_stats': 'GET /api/stats'
            },
            '2_market_data': {
                'list_crops': 'GET /api/market/crops',
                'list_districts': 'GET /api/market/districts',
                'get_prices': 'GET /api/market/rates?crop=Wheat&district=Indore',
                'historical_data': 'GET /api/market/historical?crop=Tomato&years=10'
            },
            '3_user_management': {
                'register_user': 'POST /api/user/register',
                'view_listings': 'GET /api/user/listings?crop=Wheat',
                'create_alert': 'POST /api/user/alerts'
            }
        }
    })

if __name__ == '__main__':
    print("🚀 Agromoney Backend Server v2.0 Starting...")
    print("📍 Access URLs: http://localhost:5000 | http://0.0.0.0:5000")
    print("🔧 CORS Enabled for Flutter Web")
    print("📊 Features: 10-Year Analytics, Candle Charts, Marketplace")
    print("👥 User Management: Registration, Listings, Alerts")
    print("-" * 60)
    
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=5000,
        threaded=True
    )
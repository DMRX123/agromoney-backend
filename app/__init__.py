"""
MP Mandi Price API - Main Application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register blueprints
    from app.routes import (
        auth_routes,
        price_routes,
        market_routes,
        notification_routes,
        weather_routes,
        admin_routes
    )

    app.register_blueprint(auth_routes.auth_bp, url_prefix='/api/auth')
    app.register_blueprint(price_routes.price_bp, url_prefix='/api/prices')
    app.register_blueprint(market_routes.market_bp, url_prefix='/api/marketplace')
    app.register_blueprint(notification_routes.notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(weather_routes.weather_bp, url_prefix='/api/weather')
    app.register_blueprint(admin_routes.admin_bp, url_prefix='/api/admin')

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'app': 'MP Mandi Price API',
            'version': '1.0.0',
            'status': 'running',
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints': {
                'docs': '/api/docs',
                'health': '/health',
                'auth': '/api/auth',
                'prices': '/api/prices',
                'marketplace': '/api/marketplace',
                'notifications': '/api/notifications',
                'weather': '/api/weather',
                'admin': '/api/admin'
            }
        })

    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected'
        })

    @app.route('/api/docs')
    def api_docs():
        return jsonify({
            'api_version': '1.0.0',
            'endpoints': {
                'auth': {
                    'register': {'method': 'POST', 'url': '/api/auth/register'},
                    'login': {'method': 'POST', 'url': '/api/auth/login'},
                    'logout': {'method': 'POST', 'url': '/api/auth/logout'},
                    'profile': {'method': 'GET', 'url': '/api/auth/profile'}
                },
                'prices': {
                    'get_prices': {'method': 'GET', 'url': '/api/prices'},
                    'price_trends': {'method': 'GET', 'url': '/api/prices/trends'},
                    'advanced_analysis': {'method': 'GET', 'url': '/api/prices/analysis'},
                    'crops': {'method': 'GET', 'url': '/api/prices/crops'},
                    'districts': {'method': 'GET', 'url': '/api/prices/districts'}
                },
                'marketplace': {
                    'listings': {'method': 'GET', 'url': '/api/marketplace'},
                    'create': {'method': 'POST', 'url': '/api/marketplace'},
                    'update': {'method': 'PUT', 'url': '/api/marketplace/{id}'},
                    'verify': {'method': 'POST', 'url': '/api/marketplace/{id}/verify'}
                },
                'notifications': {
                    'get_all': {'method': 'GET', 'url': '/api/notifications'},
                    'create': {'method': 'POST', 'url': '/api/notifications'},
                    'price_alert': {'method': 'POST', 'url': '/api/notifications/price-alert'}
                },
                'weather': {
                    'forecast': {'method': 'GET', 'url': '/api/weather/forecast'},
                    'crop_calendar': {'method': 'GET', 'url': '/api/weather/crop-calendar'},
                    'farming_tips': {'method': 'GET', 'url': '/api/weather/farming-tips'}
                },
                'admin': {
                    'dashboard': {'method': 'GET', 'url': '/api/admin/dashboard'},
                    'users': {'method': 'GET', 'url': '/api/admin/users'},
                    'sync': {'method': 'POST', 'url': '/api/admin/sync'}
                }
            }
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'message': 'Bad request'}), 400

    return app
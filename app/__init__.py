"""
Application factory
"""
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta
import redis
from app.config import Config, DevelopmentConfig, ProductionConfig

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object(DevelopmentConfig)

    app.config.from_prefixed_env()

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config.get('CORS_ORIGINS', '*'))

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        app.redis_client = redis.from_url(app.config.get('REDIS_URL', 'redis://localhost:6379/0'))
    except:
        app.redis_client = None
        logging.warning("Redis not available - caching disabled")

    from app.routes.auth_routes import auth_bp
    from app.routes.price_routes import price_bp
    from app.routes.market_routes import market_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.weather_routes import weather_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(price_bp, url_prefix='/api/prices')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'environment': app.config.get('ENVIRONMENT', 'development'),
            'database': 'connected' if db.engine else 'disconnected',
            'redis': 'connected' if app.redis_client else 'not_configured',
            'timestamp': datetime.utcnow().isoformat()
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Internal error: {error}')
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

    @app.before_request
    def log_request():
        if not request.path.startswith('/static'):
            app.logger.info(f'Request: {request.method} {request.path}')

    # ✅ Initialize database with tables and admin user
    from app.models import User, PriceData, MarketProduct, Notification
    init_db(app)

    return app


def init_db(app):
    """Initialize database with tables and admin user"""
    with app.app_context():
        # Create tables
        db.create_all()
        app.logger.info("✅ Database tables created/verified")
        
        # Create admin user if not exists
        admin = User.query.filter_by(phone='9999999999').first()
        if not admin:
            admin = User(
                name='Admin',
                phone='9999999999',
                email='admin@agromoney.in',
                district='Bhopal',
                language='english',
                is_admin=True,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            app.logger.info("✅ Admin user created (Phone: 9999999999, OTP: 123456)")
        else:
            app.logger.info("✅ Admin user already exists")


from app.services import AgmarknetService, WeatherService, NotificationService
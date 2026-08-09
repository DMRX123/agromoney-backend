"""
Routes package
"""
from app.routes import auth_routes
from app.routes import price_routes
from app.routes import market_routes
from app.routes import notification_routes
from app.routes import weather_routes
from app.routes import admin_routes

__all__ = [
    'auth_routes',
    'price_routes',
    'market_routes',
    'notification_routes',
    'weather_routes',
    'admin_routes'
]
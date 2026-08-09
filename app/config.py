"""
Application Configuration
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///mp_mandi.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # CORS - Allow all origins for development
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # For production, use specific origins
    # CORS_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']

    # API Keys
    AGMARKNET_API_KEY = os.environ.get(
        'AGMARKNET_API_KEY',
        '579b464db66ec23bdd00000108226f77121d47a861503b17ecc8c982'
    )
    AGMARKNET_BASE_URL = os.environ.get(
        'AGMARKNET_BASE_URL',
        'https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24'
    )
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')

    # MP Data
    MP_DISTRICTS = [
        "Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Rewa",
        "Satna", "Ratlam", "Dewas", "Shivpuri", "Chhindwara", "Morena",
        "Khargone", "Khandwa", "Vidisha", "Mandsaur", "Neemuch", "Dhar",
        "Hoshangabad", "Betul", "Seoni", "Balaghat", "Guna", "Shajapur",
        "Datia", "Tikamgarh", "Chhatarpur", "Panna", "Sidhi", "Singrauli",
        "Damoh", "Narsinghpur", "Sehore", "Raisen", "Rajgarh", "Agar Malwa",
        "Burhanpur", "Ashoknagar", "Alirajpur", "Jhabua", "Barwani"
    ]
    MAJOR_CROPS = [
        {"name": "Wheat", "hindi": "गेहूं", "category": "Cereal"},
        {"name": "Rice", "hindi": "धान", "category": "Cereal"},
        {"name": "Soybean", "hindi": "सोयाबीन", "category": "Oilseed"},
        {"name": "Gram", "hindi": "चना", "category": "Pulse"},
        {"name": "Mustard", "hindi": "सरसों", "category": "Oilseed"},
        {"name": "Maize", "hindi": "मक्का", "category": "Cereal"},
        {"name": "Lentil", "hindi": "मसूर", "category": "Pulse"},
        {"name": "Onion", "hindi": "प्याज", "category": "Vegetable"},
        {"name": "Tomato", "hindi": "टमाटर", "category": "Vegetable"},
        {"name": "Garlic", "hindi": "लहसुन", "category": "Vegetable"},
        {"name": "Coriander", "hindi": "धनिया", "category": "Spice"},
        {"name": "Peas", "hindi": "मटर", "category": "Vegetable"},
        {"name": "Fenugreek", "hindi": "मेथी", "category": "Vegetable"}
    ]

    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Pagination defaults
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # Cache
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

    # Notification types
    NOTIFICATION_TYPES = [
        'price_alert', 'weather_alert', 'market_update',
        'government_scheme', 'general', 'system'
    ]

    # Marketplace statuses
    MARKET_STATUSES = ['available', 'sold', 'reserved', 'removed', 'verified']


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # Allow all origins in development
    CORS_ORIGINS = ['*']


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # Use specific origins in production
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    # Filter out empty strings
    CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS if origin.strip()]


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    # Allow all origins in testing
    CORS_ORIGINS = ['*']
"""
Application configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # API Keys
    AGMARKNET_API_KEY = os.getenv('AGMARKNET_API_KEY', '579b464db66ec23bdd000001ee211f276db646244bfd9cb02ca250f9')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    
    # AGMARKNET API
    AGMARKNET_BASE_URL = 'https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24'
    AGMARKNET_RESOURCE_ID = '35985678-0d79-46b4-9ed6-6f13308a1d24'
    AGMARKNET_TIMEOUT = 60
    AGMARKNET_MAX_RECORDS = 5000
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mp_mandi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    JWT_REFRESH_TOKEN_EXPIRES = 86400 * 7
    
    # App
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # SMS
    SMS_API_KEY = os.getenv('SMS_API_KEY', '')
    SMS_SENDER_ID = os.getenv('SMS_SENDER_ID', 'AGROMNY')

class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENVIRONMENT = 'production'
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
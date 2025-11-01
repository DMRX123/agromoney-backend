import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Basic Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'agromoney-mp-secret-key-2024')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    
    # API Configuration
    AGMARKNET_API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    API_KEY = "579b464db66ec23bdd000001cdd3946b44ce486a72cee8c9c5063be5"
    API_TIMEOUT = 30
    API_MAX_RETRIES = 3
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///agromarket.db')
    
    # Caching Configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:5000", "http://127.0.0.1:5000",
        "http://localhost:8080", "http://127.0.0.1:8080",
        "http://localhost:58916", "http://127.0.0.1:58916",
    ]
    
    # Madhya Pradesh Districts (52)
    MP_DISTRICTS = [
        "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", "Barwani", "Betul", 
        "Bhind", "Bhopal", "Burhanpur", "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", 
        "Dhar", "Dindori", "Guna", "Gwalior", "Harda", "Hoshangabad", "Indore", "Jabalpur", 
        "Jhabua", "Katni", "Khandwa", "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur", 
        "Neemuch", "Niwari", "Panna", "Raisen", "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", 
        "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", "Shivpuri", "Sidhi", "Singrauli", 
        "Tikamgarh", "Ujjain", "Umaria", "Vidisha"
    ]
    
    # Major Crops in MP
    CROPS = [
        # Cereals
        "Wheat", "Rice", "Maize", "Jowar", "Bajra",
        # Pulses
        "Gram", "Lentil", "Pigeon Pea", "Black Gram", "Green Gram", "Cowpea",
        # Oilseeds
        "Soybean", "Mustard", "Groundnut", "Sunflower", "Sesame", "Linseed", "Castor",
        # Vegetables
        "Tomato", "Onion", "Potato", "Garlic", "Cabbage", "Cauliflower", "Brinjal",
        "Okra", "Peas", "Carrot", "Radish", "Cucumber", "Bitter Gourd", "Bottle Gourd", "Spinach",
        # Spices
        "Coriander", "Chilli", "Cumin", "Fenugreek", "Turmeric", "Ginger", "Coriander Seed",
        # Cash Crops
        "Cotton", "Sugarcane", "Tobacco", "Jute",
        # Fruits
        "Mango", "Banana", "Guava", "Orange", "Papaya", "Pomegranate", "Lemon",
        # Other
        "Honey", "Mushroom"
    ]
    
    # Crop Categories
    CROP_CATEGORIES = {
        "Cereals": ["Wheat", "Rice", "Maize", "Jowar", "Bajra"],
        "Pulses": ["Gram", "Lentil", "Pigeon Pea", "Black Gram", "Green Gram", "Cowpea"],
        "Oilseeds": ["Soybean", "Mustard", "Groundnut", "Sunflower", "Sesame", "Linseed", "Castor"],
        "Vegetables": ["Tomato", "Onion", "Potato", "Garlic", "Cabbage", "Cauliflower", "Brinjal", 
                      "Okra", "Peas", "Carrot", "Radish", "Cucumber", "Bitter Gourd", "Bottle Gourd", "Spinach"],
        "Spices": ["Coriander", "Chilli", "Cumin", "Fenugreek", "Turmeric", "Ginger", "Coriander Seed"],
        "Cash Crops": ["Cotton", "Sugarcane", "Tobacco", "Jute"],
        "Fruits": ["Mango", "Banana", "Guava", "Orange", "Papaya", "Pomegranate", "Lemon"],
        "Other": ["Honey", "Mushroom"]
    }
    
    # MP Regions
    MP_REGIONS = {
        "Malwa": ["Indore", "Ujjain", "Dewas", "Shajapur", "Ratlam", "Mandsaur", "Neemuch", "Agar Malwa", "Rajgarh"],
        "Nimar": ["Khandwa", "Khargone", "Barwani", "Burhanpur"],
        "Baghelkhand": ["Rewa", "Satna", "Sidhi", "Singrauli", "Umaria", "Shahdol", "Anuppur"],
        "Mahakoshal": ["Jabalpur", "Narsinghpur", "Mandla", "Dindori", "Balaghat", "Seoni", "Katni"],
        "Gird": ["Gwalior", "Bhind", "Morena", "Sheopur", "Datia"],
        "Bundelkhand": ["Sagar", "Damoh", "Chhatarpur", "Tikamgarh", "Panna", "Niwari", "Ashoknagar"],
        "Central": ["Bhopal", "Raisen", "Sehore", "Vidisha", "Hoshangabad", "Harda", "Betul", "Chhindwara"]
    }
    
    # Default Crop Prices (₹ per quintal)
    DEFAULT_CROP_PRICES = {
        # Cereals
        "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Jowar": 2600, "Bajra": 2400,
        # Pulses
        "Gram": 5200, "Lentil": 6000, "Pigeon Pea": 7000, "Black Gram": 6500, "Green Gram": 7000, "Cowpea": 4800,
        # Oilseeds
        "Soybean": 4800, "Mustard": 5200, "Groundnut": 6000, "Sunflower": 5200, "Sesame": 8000, "Linseed": 4800, "Castor": 5800,
        # Vegetables
        "Tomato": 1500, "Onion": 2000, "Potato": 1800, "Garlic": 4500, "Cabbage": 1200, "Cauliflower": 1500, "Brinjal": 2000,
        "Okra": 3000, "Peas": 3500, "Carrot": 2200, "Radish": 1500, "Cucumber": 1800, "Bitter Gourd": 2500, "Bottle Gourd": 1600, "Spinach": 1200,
        # Spices
        "Coriander": 6500, "Chilli": 5500, "Cumin": 10000, "Fenugreek": 5000, "Turmeric": 7500, "Ginger": 6500, "Coriander Seed": 7500,
        # Cash Crops
        "Cotton": 7000, "Sugarcane": 3500, "Tobacco": 10000, "Jute": 4200,
        # Fruits
        "Mango": 4500, "Banana": 2200, "Guava": 3000, "Orange": 3500, "Papaya": 1800, "Pomegranate": 5500, "Lemon": 3000,
        # Other
        "Honey": 12000, "Mushroom": 15000
    }
    
    # Market Data Settings (10-Year Support)
    DEFAULT_DATA_DAYS = 30
    MAX_DATA_POINTS = 1000
    HISTORICAL_YEARS = 10
    MAX_HISTORICAL_YEARS = 10
    SUPPORTED_YEARS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Candle Stick Intervals
    CANDLE_INTERVALS = [1, 3, 5, 7, 10, 15, 30, 60, 90, 180, 365]
    DEFAULT_CANDLE_INTERVAL = 30
    
    # Analysis Configuration
    ANALYSIS_PERIODS = ['1_year', '5_years', '10_years']
    DEFAULT_ANALYSIS_PERIOD = '10_years'
    
    # User & Marketplace Settings
    MAX_LISTINGS_PER_USER = 20
    MAX_PRICE_ALERTS_PER_USER = 15
    LISTING_EXPIRY_DAYS = 30
    ALERT_CHECK_INTERVAL = 3600
    
    # Feature Flags
    FEATURE_FLAGS = {
        '10_year_analytics': True,
        'candle_stick_charts': True,
        'marketplace': True,
        'price_alerts': True,
        'user_reliability_scoring': True,
        'advanced_predictions': True,
        'seasonal_analysis': True,
        'volatility_tracking': True
    }


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    DATABASE_URL = os.getenv('DEV_DATABASE_URL', 'sqlite:///dev_agromarket.db')
    LOG_LEVEL = 'DEBUG'
    CACHE_DEFAULT_TIMEOUT = 60


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/agromarket')
    LOG_LEVEL = 'WARNING'
    CACHE_DEFAULT_TIMEOUT = 600
    RATE_LIMITING_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'
    LOG_LEVEL = 'CRITICAL'
    CACHE_DEFAULT_TIMEOUT = 0
    AGMARKNET_API_URL = None


# Configuration Dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Validate Configuration
def validate_config():
    """Validate configuration settings"""
    required_env_vars = ['SECRET_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {missing_vars}")
    
    if Config.HISTORICAL_YEARS > Config.MAX_HISTORICAL_YEARS:
        raise ValueError(f"HISTORICAL_YEARS cannot exceed MAX_HISTORICAL_YEARS")
    
    return True

# Validate on import
try:
    validate_config()
    print("✅ Configuration validated successfully")
except Exception as e:
    print(f"❌ Configuration validation failed: {e}")
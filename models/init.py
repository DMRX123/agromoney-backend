# Models package initialization
from .market_models import (
    MarketData, 
    HistoricalPrice, 
    CandleStickData, 
    CropAnalysis,
    TrendAnalysis,
    MarketPrediction,
    CropInsights,
    CropRecommendation,
    PriceAlert,
    MarketAnalysisReport,
    User,
    SellingListing,
    BuyingRequest,
    MarketTransaction,
    UserPreference,
    MarketInsight,
    MarketplaceManager
)

__all__ = [
    # Market data models
    'MarketData',
    'HistoricalPrice', 
    'CandleStickData',
    'CropAnalysis',
    'TrendAnalysis',
    'MarketPrediction',
    'CropInsights',
    'CropRecommendation',
    'MarketAnalysisReport',
    
    # User and marketplace models
    'User',
    'SellingListing',
    'PriceAlert',
    'BuyingRequest',
    'MarketTransaction',
    'UserPreference',
    'MarketInsight',
    'MarketplaceManager'
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'AgroMoney Team'
__description__ = 'Agricultural Market Data and User Management Models'

# Import all models for easier access
try:
    from .market_models import *
except ImportError as e:
    print(f"Warning: Could not import models: {e}")

# Convenience imports for common use cases
market_models = [
    MarketData, HistoricalPrice, CandleStickData, CropAnalysis,
    TrendAnalysis, MarketPrediction, CropInsights, CropRecommendation,
    MarketAnalysisReport
]

user_models = [
    User, SellingListing, PriceAlert, BuyingRequest,
    MarketTransaction, UserPreference, MarketInsight, MarketplaceManager
]

def get_model_classes():
    """Return all model classes in the package"""
    return market_models + user_models

def get_market_models():
    """Return only market-related model classes"""
    return market_models

def get_user_models():
    """Return only user-related model classes"""
    return user_models

# Model categories for documentation
MODEL_CATEGORIES = {
    'market_data': ['MarketData', 'HistoricalPrice', 'CandleStickData'],
    'analysis': ['CropAnalysis', 'TrendAnalysis', 'MarketPrediction', 'CropInsights', 'MarketAnalysisReport'],
    'recommendations': ['CropRecommendation'],
    'user_management': ['User', 'UserPreference'],
    'marketplace': ['SellingListing', 'BuyingRequest', 'PriceAlert', 'MarketTransaction', 'MarketplaceManager'],
    'insights': ['MarketInsight']
}

def get_models_by_category(category: str):
    """Get model classes by category"""
    model_names = MODEL_CATEGORIES.get(category, [])
    return [globals()[name] for name in model_names if name in globals()]
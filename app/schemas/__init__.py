"""
Pydantic/Validation schemas
"""
from app.schemas.schemas import (
    # User schemas
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,

    # Price schemas
    PriceDataBase,
    PriceDataResponse,
    PriceTrendResponse,
    PriceAnalysisResponse,

    # Market schemas
    MarketProductBase,
    MarketProductCreate,
    MarketProductUpdate,
    MarketProductResponse,

    # Notification schemas
    NotificationBase,
    NotificationCreate,
    NotificationResponse,

    # Common schemas
    PaginationParams,
    ApiResponse,
    ErrorResponse
)

__all__ = [
    'UserBase',
    'UserCreate',
    'UserLogin',
    'UserResponse',
    'UserUpdate',
    'PriceDataBase',
    'PriceDataResponse',
    'PriceTrendResponse',
    'PriceAnalysisResponse',
    'MarketProductBase',
    'MarketProductCreate',
    'MarketProductUpdate',
    'MarketProductResponse',
    'NotificationBase',
    'NotificationCreate',
    'NotificationResponse',
    'PaginationParams',
    'ApiResponse',
    'ErrorResponse'
]
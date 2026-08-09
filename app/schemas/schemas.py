"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, validator


# ============ User Schemas ============

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., pattern=r'^[6-9]\d{9}$')
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    district: Optional[str] = Field(None, max_length=100)
    village: Optional[str] = Field(None, max_length=100)
    land_area: Optional[float] = Field(None, ge=0)
    soil_type: Optional[str] = Field(None, max_length=100)
    language: str = Field('hindi', pattern='^(hindi|english)$')
    crops_grown: Optional[List[str]] = []


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    phone: str = Field(..., pattern=r'^[6-9]\d{9}$')
    password: Optional[str] = None
    otp: Optional[str] = Field(None, pattern=r'^\d{6}$')


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    village: Optional[str] = Field(None, max_length=100)
    land_area: Optional[float] = Field(None, ge=0)
    soil_type: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, pattern='^(hindi|english)$')
    crops_grown: Optional[List[str]] = []


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    district: Optional[str]
    village: Optional[str]
    land_area: Optional[float]
    soil_type: Optional[str]
    language: str
    crops_grown: List[str]
    is_admin: bool
    created_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


# ============ Price Schemas ============

class PriceDataBase(BaseModel):
    district: str = Field(..., max_length=100)
    mandi: str = Field(..., max_length=100)
    crop: str = Field(..., max_length=100)
    variety: Optional[str] = None
    grade: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    modal_price: float = Field(..., ge=0)
    arrival_date: Optional[datetime] = None

    @validator('max_price')
    def validate_max_price(cls, v, values):
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('Max price cannot be less than min price')
        return v


class PriceDataResponse(PriceDataBase):
    id: int
    recorded_date: Optional[datetime]

    class Config:
        from_attributes = True


class PriceTrendResponse(BaseModel):
    date: str
    min_price: float
    max_price: float
    modal_price: float
    volume: int
    count: int


class PriceAnalysisResponse(BaseModel):
    crop: str
    district: Optional[str]
    period_days: int
    current_price: float
    start_price: float
    percent_change: float
    trend: str
    volatility: float
    moving_average_7: float
    moving_average_30: float
    support_level: float
    resistance_level: float
    data_points: int
    recommendation: dict


# ============ Market Product Schemas ============

class MarketProductBase(BaseModel):
    crop: str = Field(..., max_length=100)
    variety: Optional[str] = None
    quantity: float = Field(..., gt=0)
    unit: str = Field('quintal', max_length=20)
    price_per_unit: Optional[float] = Field(None, ge=0)
    district: Optional[str] = Field(None, max_length=100)
    mandi: Optional[str] = Field(None, max_length=100)
    village: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    description_hindi: Optional[str] = None
    contact_number: str = Field(..., pattern=r'^[6-9]\d{9}$')
    image_url: Optional[str] = None


class MarketProductCreate(MarketProductBase):
    user_id: int


class MarketProductUpdate(BaseModel):
    quantity: Optional[float] = Field(None, gt=0)
    price_per_unit: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    description_hindi: Optional[str] = None
    contact_number: Optional[str] = Field(None, pattern=r'^[6-9]\d{9}$')
    image_url: Optional[str] = None
    status: Optional[str] = Field(None, pattern='^(available|sold|reserved|removed)$')


class MarketProductResponse(MarketProductBase):
    id: int
    user_id: int
    status: str
    is_verified: bool
    verified_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============ Notification Schemas ============

class NotificationBase(BaseModel):
    title: str = Field(..., max_length=200)
    title_hindi: Optional[str] = None
    message: str = Field(..., max_length=1000)
    message_hindi: Optional[str] = None
    notification_type: str = Field('general', pattern='^(price_alert|weather_alert|market_update|government_scheme|general|system)$')
    target_district: Optional[str] = None
    target_crop: Optional[str] = None
    target_role: Optional[str] = Field('all', pattern='^(all|farmer|admin)$')


class NotificationCreate(NotificationBase):
    user_id: Optional[int] = None


class NotificationResponse(NotificationBase):
    id: int
    user_id: Optional[int]
    is_read: bool
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Common Schemas ============

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: str = Field('desc', pattern='^(asc|desc)$')


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    pages: Optional[int] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    errors: Optional[dict] = None
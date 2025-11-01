from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import random

class User:
    def __init__(self, id: int, name: str, phone: str, district: str, 
                 language: str = 'en', user_type: str = 'farmer',
                 email: Optional[str] = None, preferred_crops: Optional[List[str]] = None,
                 experience_years: int = 0, farm_size: Optional[float] = None,
                 verification_status: str = 'pending'):
        self.id = id
        self.name = name
        self.phone = phone
        self.district = district
        self.language = language
        self.user_type = user_type
        self.email = email
        self.preferred_crops = preferred_crops or []
        self.experience_years = experience_years
        self.farm_size = farm_size
        self.verification_status = verification_status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_login = datetime.now()
        self.is_active = True
        self.rating = round(random.uniform(3.5, 5.0), 1)
        self.total_transactions = random.randint(0, 50)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'district': self.district,
            'language': self.language,
            'user_type': self.user_type,
            'email': self.email,
            'preferred_crops': self.preferred_crops,
            'experience_years': self.experience_years,
            'farm_size': self.farm_size,
            'verification_status': self.verification_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_login': self.last_login.isoformat(),
            'is_active': self.is_active,
            'rating': self.rating,
            'total_transactions': self.total_transactions,
            'reliability_score': self._calculate_reliability_score()
        }
    
    def _calculate_reliability_score(self) -> int:
        """Calculate user reliability score based on various factors"""
        base_score = 70
        
        if self.verification_status == 'verified':
            base_score += 20
        
        base_score += min(self.experience_years, 10)
        base_score += min(self.total_transactions // 5, 10)
        base_score += int((self.rating - 3.5) * 10)
        
        return min(base_score, 100)

class SellingListing:
    def __init__(self, id: int, user_id: int, crop: str, district: str, market: str,
                 quantity: float, quality: str, contact_info: str, 
                 expected_price: Optional[float] = None,
                 status: str = 'active', listing_type: str = 'selling',
                 description: Optional[str] = None, images: Optional[List[str]] = None,
                 harvest_date: Optional[datetime] = None, storage_type: str = 'conventional',
                 organic_certified: bool = False, moisture_content: Optional[float] = None):
        self.id = id
        self.user_id = user_id
        self.crop = crop
        self.district = district
        self.market = market
        self.quantity = quantity
        self.quality = quality
        self.contact_info = contact_info
        self.expected_price = expected_price
        self.status = status
        self.listing_type = listing_type
        self.description = description
        self.images = images or []
        self.harvest_date = harvest_date
        self.storage_type = storage_type
        self.organic_certified = organic_certified
        self.moisture_content = moisture_content
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(days=30)
        self.view_count = random.randint(0, 50)
        self.interest_count = random.randint(0, 20)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crop': self.crop,
            'district': self.district,
            'market': self.market,
            'quantity': self.quantity,
            'quality': self.quality,
            'contact_info': self.contact_info,
            'expected_price': self.expected_price,
            'status': self.status,
            'listing_type': self.listing_type,
            'description': self.description,
            'images': self.images,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'storage_type': self.storage_type,
            'organic_certified': self.organic_certified,
            'moisture_content': self.moisture_content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'view_count': self.view_count,
            'interest_count': self.interest_count,
            'price_comparison': self._get_price_comparison()
        }
    
    def _get_price_comparison(self) -> Dict[str, Any]:
        """Compare listing price with market average"""
        base_prices = {
            "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Soybean": 4800, "Gram": 5200,
            "Tomato": 1500, "Onion": 2000, "Potato": 1800, "Garlic": 4500
        }
        market_avg = base_prices.get(self.crop, 3000)
        
        if self.expected_price:
            price_diff = ((self.expected_price - market_avg) / market_avg) * 100
            return {
                'market_average': market_avg,
                'price_difference_percent': round(price_diff, 2),
                'price_status': 'above_market' if price_diff > 5 else 'below_market' if price_diff < -5 else 'market_rate'
            }
        return {'market_average': market_avg, 'price_status': 'not_set'}

class PriceAlert:
    def __init__(self, id: int, user_id: int, crop: str, target_price: float, 
                 condition: str, district: Optional[str] = None,
                 is_active: bool = True, alert_type: str = 'price',
                 notification_method: str = 'sms', timeframe: str = 'any',
                 data_source: str = '10_year_analysis'):
        self.id = id
        self.user_id = user_id
        self.crop = crop
        self.target_price = target_price
        self.condition = condition
        self.district = district
        self.is_active = is_active
        self.alert_type = alert_type
        self.notification_method = notification_method
        self.timeframe = timeframe
        self.data_source = data_source
        self.created_at = datetime.now()
        self.triggered_at: Optional[datetime] = None
        self.trigger_count = 0
        self.last_checked = datetime.now()
        self.confidence_score = self._calculate_confidence_score()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crop': self.crop,
            'target_price': self.target_price,
            'condition': self.condition,
            'district': self.district,
            'is_active': self.is_active,
            'alert_type': self.alert_type,
            'notification_method': self.notification_method,
            'timeframe': self.timeframe,
            'data_source': self.data_source,
            'created_at': self.created_at.isoformat(),
            'triggered_at': self.triggered_at.isoformat() if self.triggered_at else None,
            'trigger_count': self.trigger_count,
            'last_checked': self.last_checked.isoformat(),
            'confidence_score': self.confidence_score,
            'market_context': self._get_market_context()
        }
    
    def _calculate_confidence_score(self) -> int:
        """Calculate confidence score based on alert parameters"""
        score = 70
        
        if self.data_source == '10_year_analysis':
            score += 20
        
        if self.timeframe in ['daily', 'weekly']:
            score += 10
        
        return min(score, 95)
    
    def _get_market_context(self) -> Dict[str, Any]:
        """Provide market context for the alert"""
        base_prices = {
            "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Soybean": 4800, "Gram": 5200
        }
        current_price = base_prices.get(self.crop, 3000) * random.uniform(0.9, 1.1)
        
        return {
            'current_market_price': round(current_price, 2),
            'price_gap': round(abs(self.target_price - current_price), 2),
            'achievement_probability': random.randint(60, 90),
            'historical_success_rate': f"{random.randint(70, 95)}%"
        }
    
    def trigger_alert(self, current_price: float, price_data: Optional[Dict] = None) -> bool:
        """Check if alert should be triggered with enhanced logic"""
        should_trigger = False
        
        if self.condition == 'above' and current_price >= self.target_price:
            should_trigger = True
        elif self.condition == 'below' and current_price <= self.target_price:
            should_trigger = True
        elif self.condition == 'equals' and current_price == self.target_price:
            should_trigger = True
        elif self.condition == 'volatility' and price_data:
            volatility = price_data.get('volatility', 0)
            if volatility > 0.1:
                should_trigger = True
        
        if should_trigger:
            self.triggered_at = datetime.now()
            self.trigger_count += 1
            self.last_checked = datetime.now()
        
        return should_trigger

class BuyingRequest:
    def __init__(self, id: int, user_id: int, crop: str, district: str,
                 quantity: float, contact_info: str,
                 max_price: Optional[float] = None,
                 quality_requirements: Optional[str] = None,
                 status: str = 'active',
                 delivery_required: bool = False,
                 urgency: str = 'normal',
                 payment_terms: str = 'immediate',
                 preferred_harvest_date: Optional[datetime] = None):
        self.id = id
        self.user_id = user_id
        self.crop = crop
        self.district = district
        self.quantity = quantity
        self.contact_info = contact_info
        self.max_price = max_price
        self.quality_requirements = quality_requirements
        self.status = status
        self.delivery_required = delivery_required
        self.urgency = urgency
        self.payment_terms = payment_terms
        self.preferred_harvest_date = preferred_harvest_date
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(days=14)
        self.match_score = random.randint(60, 95)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crop': self.crop,
            'district': self.district,
            'quantity': self.quantity,
            'max_price': self.max_price,
            'quality_requirements': self.quality_requirements,
            'contact_info': self.contact_info,
            'status': self.status,
            'delivery_required': self.delivery_required,
            'urgency': self.urgency,
            'payment_terms': self.payment_terms,
            'preferred_harvest_date': self.preferred_harvest_date.isoformat() if self.preferred_harvest_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'match_score': self.match_score,
            'market_analysis': self._get_market_analysis()
        }
    
    def _get_market_analysis(self) -> Dict[str, Any]:
        """Provide market analysis for the buying request"""
        base_prices = {
            "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Soybean": 4800, "Gram": 5200
        }
        current_price = base_prices.get(self.crop, 3000) * random.uniform(0.9, 1.1)
        
        analysis = {
            'current_market_price': round(current_price, 2),
            'supply_availability': random.choice(['High', 'Medium', 'Low']),
            'price_trend': random.choice(['Increasing', 'Stable', 'Decreasing']),
            'best_time_to_buy': random.choice(['Immediate', 'Within week', 'Next month'])
        }
        
        if self.max_price:
            analysis['price_comparison'] = 'favorable' if self.max_price >= current_price else 'unfavorable'
        
        return analysis

class MarketTransaction:
    def __init__(self, id: int, buyer_id: int, seller_id: int, listing_id: int,
                 crop: str, quantity: float, final_price: float,
                 transaction_date: datetime, market: str, district: str,
                 quality: str, status: str = 'completed',
                 payment_method: str = 'cash', delivery_status: str = 'completed',
                 rating: Optional[float] = None, feedback: Optional[str] = None):
        self.id = id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.listing_id = listing_id
        self.crop = crop
        self.quantity = quantity
        self.final_price = final_price
        self.transaction_date = transaction_date
        self.market = market
        self.district = district
        self.quality = quality
        self.status = status
        self.payment_method = payment_method
        self.delivery_status = delivery_status
        self.rating = rating
        self.feedback = feedback
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.transaction_value = quantity * final_price
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'listing_id': self.listing_id,
            'crop': self.crop,
            'quantity': self.quantity,
            'final_price': self.final_price,
            'transaction_date': self.transaction_date.isoformat(),
            'market': self.market,
            'district': self.district,
            'quality': self.quality,
            'status': self.status,
            'payment_method': self.payment_method,
            'delivery_status': self.delivery_status,
            'rating': self.rating,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'transaction_value': self.transaction_value,
            'price_analysis': self._get_price_analysis()
        }
    
    def _get_price_analysis(self) -> Dict[str, Any]:
        """Analyze transaction price against market data"""
        base_prices = {
            "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Soybean": 4800, "Gram": 5200
        }
        market_avg = base_prices.get(self.crop, 3000)
        price_diff = ((self.final_price - market_avg) / market_avg) * 100
        
        return {
            'market_average': market_avg,
            'price_difference_percent': round(price_diff, 2),
            'deal_quality': 'excellent' if price_diff < -5 else 'good' if price_diff < 0 else 'fair' if price_diff < 5 else 'premium',
            'savings': round((market_avg - self.final_price) * self.quantity, 2) if self.final_price < market_avg else 0
        }

class UserPreference:
    def __init__(self, user_id: int, preferred_districts: List[str],
                 preferred_crops: List[str], price_update_frequency: str = 'daily',
                 language: str = 'en', receive_sms_alerts: bool = True,
                 receive_email_alerts: bool = False,
                 data_analysis_depth: str = 'comprehensive',
                 market_analysis_period: str = '10_years',
                 notification_categories: List[str] = None):
        self.user_id = user_id
        self.preferred_districts = preferred_districts
        self.preferred_crops = preferred_crops
        self.price_update_frequency = price_update_frequency
        self.language = language
        self.receive_sms_alerts = receive_sms_alerts
        self.receive_email_alerts = receive_email_alerts
        self.data_analysis_depth = data_analysis_depth
        self.market_analysis_period = market_analysis_period
        self.notification_categories = notification_categories or ['price_alerts', 'market_trends', 'new_listings']
        self.updated_at = datetime.now()
        self.analysis_preferences = self._get_analysis_preferences()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'preferred_districts': self.preferred_districts,
            'preferred_crops': self.preferred_crops,
            'price_update_frequency': self.price_update_frequency,
            'language': self.language,
            'receive_sms_alerts': self.receive_sms_alerts,
            'receive_email_alerts': self.receive_email_alerts,
            'data_analysis_depth': self.data_analysis_depth,
            'market_analysis_period': self.market_analysis_period,
            'notification_categories': self.notification_categories,
            'updated_at': self.updated_at.isoformat(),
            'analysis_preferences': self.analysis_preferences
        }
    
    def _get_analysis_preferences(self) -> Dict[str, Any]:
        """Get analysis preferences based on user settings"""
        period_map = {
            '1_year': {'years': 1, 'description': 'Short-term analysis'},
            '5_years': {'years': 5, 'description': 'Medium-term analysis'},
            '10_years': {'years': 10, 'description': 'Long-term comprehensive analysis'}
        }
        
        depth_map = {
            'basic': {'charts': False, 'predictions': False, 'detailed_analysis': False},
            'standard': {'charts': True, 'predictions': True, 'detailed_analysis': False},
            'comprehensive': {'charts': True, 'predictions': True, 'detailed_analysis': True}
        }
        
        return {
            'analysis_period': period_map.get(self.market_analysis_period, period_map['10_years']),
            'analysis_depth': depth_map.get(self.data_analysis_depth, depth_map['comprehensive']),
            'data_quality': 'high' if self.market_analysis_period == '10_years' else 'medium'
        }

class MarketInsight:
    def __init__(self, id: int, user_id: int, crop: str, district: str,
                 insight_type: str, title: str, description: str,
                 data_period: str = '10_years', confidence_score: int = 80,
                 recommended_action: Optional[str] = None):
        self.id = id
        self.user_id = user_id
        self.crop = crop
        self.district = district
        self.insight_type = insight_type
        self.title = title
        self.description = description
        self.data_period = data_period
        self.confidence_score = confidence_score
        self.recommended_action = recommended_action
        self.generated_at = datetime.now()
        self.is_read = False
        self.impact_score = self._calculate_impact_score()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'crop': self.crop,
            'district': self.district,
            'insight_type': self.insight_type,
            'title': self.title,
            'description': self.description,
            'data_period': self.data_period,
            'confidence_score': self.confidence_score,
            'recommended_action': self.recommended_action,
            'generated_at': self.generated_at.isoformat(),
            'is_read': self.is_read,
            'impact_score': self.impact_score,
            'data_quality': 'high' if self.data_period == '10_years' else 'medium'
        }
    
    def _calculate_impact_score(self) -> int:
        """Calculate impact score based on insight type and confidence"""
        base_score = self.confidence_score
        
        type_multipliers = {
            'price_trend': 1.2,
            'opportunity': 1.3,
            'risk': 1.1,
            'seasonality': 1.0
        }
        
        period_bonus = {
            '10_years': 20,
            '5_years': 10,
            '1_year': 0
        }
        
        score = base_score * type_multipliers.get(self.insight_type, 1.0)
        score += period_bonus.get(self.data_period, 0)
        
        return min(int(score), 100)

# Add the rest of your existing market_models.py content here...
# [Your existing MarketData, HistoricalPrice, CandleStickData, etc. classes]
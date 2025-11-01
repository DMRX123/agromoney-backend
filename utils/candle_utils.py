from datetime import datetime, timedelta
import random
from typing import Dict, Any, List

class CandleUtils:
    """Common utilities for candle stick data generation"""
    
    @staticmethod
    def generate_candle_data(crop: str, district: str, years: float = 1.0,
                           interval_days: int = 1) -> List[Dict[str, Any]]:
        """Generate candle stick data for any crop and period"""
        
        base_prices = {
            "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Soybean": 4800, "Gram": 5200,
            "Tomato": 1500, "Onion": 2000, "Potato": 1800, "Garlic": 4500, "Coriander": 6500,
            "Cumin": 10000, "Cotton": 7000, "Sugarcane": 3500, "Mango": 4500, "Banana": 2200,
            "Chilli": 5500, "Mustard": 5200, "Groundnut": 6000
        }
        
        base_price = base_prices.get(crop, 3000)
        data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        
        # Safety limit for data points
        max_points = 1000
        total_days = years * 365
        estimated_points = total_days / interval_days
        
        if estimated_points > max_points:
            adjusted_interval = max(1, int(total_days / max_points))
            interval_days = adjusted_interval
        
        current_date = start_date
        point_count = 0
        
        while current_date <= end_date and point_count < max_points:
            price_data = CandleUtils.calculate_ohlc_price(base_price, current_date, start_date, crop, interval_days)
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'timestamp': current_date.isoformat(),
                'open': price_data['open'],
                'high': price_data['high'],
                'low': price_data['low'],
                'close': price_data['close'],
                'volume': random.randint(100, 5000),
                'commodity': crop,
                'district': district,
                'interval_days': interval_days,
                'color': 'green' if price_data['close'] >= price_data['open'] else 'red',
                'trend': 'bullish' if price_data['close'] > price_data['open'] else 'bearish' if price_data['close'] < price_data['open'] else 'neutral'
            })
            
            current_date += timedelta(days=interval_days)
            point_count += 1
        
        return data
    
    @staticmethod
    def calculate_ohlc_price(base_price: float, current_date: datetime, start_date: datetime, 
                           crop: str, interval_days: int) -> Dict[str, float]:
        """Calculate OHLC prices with realistic market behavior"""
        
        month = current_date.month
        
        # Seasonal variations
        seasonal_factor = CandleUtils.get_seasonal_factor(crop, month)
        
        # Long-term trend for 10 years (inflation + market growth)
        years_passed = (current_date - start_date).days / 365
        trend_factor = 1.0 + (0.06 * years_passed)
        
        # Short-term random fluctuations
        random_factor = random.uniform(0.95, 1.05)
        
        # Base value calculation
        base_value = base_price * seasonal_factor * trend_factor * random_factor
        
        # Market volatility based on crop type
        if crop in ["Tomato", "Onion", "Potato"]:
            volatility = 0.15
        elif crop in ["Wheat", "Rice", "Maize"]:
            volatility = 0.08
        else:
            volatility = 0.10
        
        # Adjust volatility based on interval
        interval_volatility = volatility * (interval_days ** 0.5)
        
        # Generate OHLC prices
        open_price = base_value
        period_change = random.uniform(-interval_volatility, interval_volatility)
        close_price = open_price * (1 + period_change)
        
        # High and Low within the period
        intra_period_volatility = interval_volatility * 0.8
        high_price = max(open_price, close_price) * (1 + random.uniform(0, intra_period_volatility))
        low_price = min(open_price, close_price) * (1 - random.uniform(0, intra_period_volatility))
        
        # Ensure logical OHLC relationship
        high_price = max(open_price, close_price, high_price)
        low_price = min(open_price, close_price, low_price)
        
        # Add realistic patterns based on trends
        if close_price > open_price:
            # Bullish pattern
            low_price = open_price + (low_price - open_price) * 0.7
            high_price = close_price + (high_price - close_price) * 0.3
        elif close_price < open_price:
            # Bearish pattern
            high_price = open_price - (open_price - high_price) * 0.7
            low_price = close_price - (close_price - low_price) * 0.3
        
        return {
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2)
        }
    
    @staticmethod
    def get_seasonal_factor(crop: str, month: int) -> float:
        """Get seasonal price factor for candle stick data"""
        
        # Rabi crops (Oct-Mar)
        if crop in ["Wheat", "Gram", "Mustard", "Barley"]:
            if month in [3, 4, 5]:  # March-May (harvest season)
                return 1.0 - random.uniform(0.1, 0.2)
            elif month in [10, 11, 12]:  # Oct-Dec (sowing season)
                return 1.0 + random.uniform(0.05, 0.15)
            else:
                return 1.0 + random.uniform(-0.05, 0.05)
        
        # Kharif crops (Jun-Sep)
        elif crop in ["Rice", "Soybean", "Maize", "Cotton"]:
            if month in [9, 10, 11]:  # Sep-Nov (harvest season)
                return 1.0 - random.uniform(0.1, 0.25)
            elif month in [6, 7, 8]:  # Jun-Aug (growing season)
                return 1.0 + random.uniform(0.05, 0.15)
            else:
                return 1.0 + random.uniform(-0.05, 0.05)
        
        # Vegetables - highly seasonal
        elif crop in ["Tomato", "Onion", "Potato"]:
            return 1.0 + random.uniform(-0.3, 0.4)
        
        # Fruits - seasonal patterns
        elif crop in ["Mango", "Orange", "Banana"]:
            if crop == "Mango" and month in [4, 5, 6]:
                return 1.0 - random.uniform(0.1, 0.3)
            elif crop == "Orange" and month in [12, 1, 2]:
                return 1.0 - random.uniform(0.1, 0.2)
            else:
                return 1.0 + random.uniform(0.1, 0.3)
        
        # Default seasonal pattern
        else:
            return 1.0 + random.uniform(-0.1, 0.1)
    
    @staticmethod
    def generate_flexible_historical_data(crop: str, district: str, years: float, 
                                       interval_days: int) -> List[Dict[str, Any]]:
        """Generate historical data with flexible intervals"""
        return CandleUtils.generate_candle_data(crop, district, years, interval_days)